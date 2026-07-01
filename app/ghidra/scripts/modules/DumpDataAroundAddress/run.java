package modules.DumpDataAroundAddress;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;

import lib.FileUtils;
import lib.Logger;

import java.io.File;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Dump raw bytes around a specified address in hexadecimal and ASCII form.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "DumpDataAroundAddress";
    private static final String DEFAULT_START_ADDRESS = "00676680";
    private static final String DEFAULT_LENGTH = "0x220";
    private static final int BYTES_PER_LINE = 16;

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();
            Address startAddress = parseTargetAddress(options.startAddressText);
            int length = parseLength(options.lengthText);

            if (length <= 0) {
                throw new IllegalArgumentException("Length must be greater than zero.");
            }

            log.section("Dump Data Around Address");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Start address", startAddress);
            log.keyValue("Length", formatLength(length));
            log.keyValue("Bytes per line", BYTES_PER_LINE);
            log.emptyLine();

            int linesDumped = 0;

            for (int offset = 0; offset < length; offset += BYTES_PER_LINE) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                Address lineAddress = startAddress.add(offset);
                int lineLength = Math.min(BYTES_PER_LINE, length - offset);

                log.raw(formatDumpLine(lineAddress, lineLength));
                linesDumped++;
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Start address", startAddress);
            log.keyValue("Bytes dumped", length);
            log.keyValue("Lines dumped", linesDumped);
            log.ok("Done.");
        } finally {
            log.close();
        }
    }

    private ScriptOptions parseOptions() throws Exception {
        ScriptOptions options = new ScriptOptions();
        String[] args = getScriptArgs();

        if (args != null && args.length > 0) {
            options.startAddressText = args[0];
        }

        if (args != null && args.length > 1) {
            options.lengthText = args[1];
        }

        if (options.startAddressText == null || options.startAddressText.trim().isEmpty()) {
            options.startAddressText = askString(
                "Dump Data Around Address",
                "Start address:",
                DEFAULT_START_ADDRESS
            );
        }

        if (options.lengthText == null || options.lengthText.trim().isEmpty()) {
            options.lengthText = askString(
                "Dump Data Around Address",
                "Length in bytes, decimal or hex:",
                DEFAULT_LENGTH
            );
        }

        if (options.startAddressText == null || options.startAddressText.trim().isEmpty()) {
            options.startAddressText = DEFAULT_START_ADDRESS;
        }

        if (options.lengthText == null || options.lengthText.trim().isEmpty()) {
            options.lengthText = DEFAULT_LENGTH;
        }

        options.startAddressText = options.startAddressText.trim();
        options.lengthText = options.lengthText.trim();

        return options;
    }

    private Address parseTargetAddress(String addressText) {
        String normalized = addressText.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            normalized = normalized.substring(2);
        }

        return toAddr(normalized);
    }

    private int parseLength(String lengthText) {
        String normalized = lengthText.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            return Integer.parseInt(normalized.substring(2), 16);
        }

        return Integer.parseInt(normalized, 10);
    }

    private String formatLength(int length) {
        return "0x" + Integer.toHexString(length) + " (" + length + " bytes)";
    }

    private String formatDumpLine(Address lineAddress, int lineLength) throws Exception {
        StringBuilder hex = new StringBuilder();
        StringBuilder ascii = new StringBuilder();

        for (int index = 0; index < BYTES_PER_LINE; index++) {
            if (index < lineLength) {
                byte value = getByte(lineAddress.add(index));
                int unsignedValue = value & 0xff;

                hex.append(String.format("%02x ", unsignedValue));
                ascii.append(toPrintableAscii(unsignedValue));
            } else {
                hex.append("   ");
                ascii.append(" ");
            }
        }

        return lineAddress + "  " + hex + " " + ascii;
    }

    private char toPrintableAscii(int value) {
        if (value >= 32 && value <= 126) {
            return (char) value;
        }

        return '.';
    }

    private static class ScriptOptions {
        private String startAddressText;
        private String lengthText;
    }
}
