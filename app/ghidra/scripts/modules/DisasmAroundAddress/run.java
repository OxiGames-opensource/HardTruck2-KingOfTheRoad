package modules.DisasmAroundAddress;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Instruction;

import lib.FileUtils;
import lib.Logger;

import java.io.File;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Print disassembled instructions starting from a specified address.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "DisasmAroundAddress";
    private static final String DEFAULT_START_ADDRESS = "00527c20";
    private static final String DEFAULT_INSTRUCTION_COUNT = "300";

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();

            Address requestedStartAddress = parseTargetAddress(options.startAddressText);
            int requestedInstructionCount = parseNumber(options.instructionCountText);

            if (requestedInstructionCount <= 0) {
                throw new IllegalArgumentException(
                    "Instruction count must be greater than zero: " + options.instructionCountText
                );
            }

            Instruction firstInstruction = currentProgram
                .getListing()
                .getInstructionAt(requestedStartAddress);

            if (firstInstruction == null) {
                firstInstruction = currentProgram
                    .getListing()
                    .getInstructionAfter(requestedStartAddress);
            }

            log.section("Disassemble Around Address");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Requested start address", requestedStartAddress);
            log.keyValue("Requested instructions", requestedInstructionCount);

            if (firstInstruction == null) {
                log.warn("No instruction found at or after requested address.");
                log.emptyLine();
                log.section("Summary");
                log.keyValue("Requested start address", requestedStartAddress);
                log.keyValue("Printed instructions", 0);
                return;
            }

            log.keyValue("First instruction address", firstInstruction.getAddress());
            log.emptyLine();

            Instruction instruction = firstInstruction;
            int printedInstructions = 0;

            while (instruction != null && printedInstructions < requestedInstructionCount) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                log.raw(String.format(
                    "%s  %s",
                    instruction.getAddress(),
                    instruction.toString()
                ));

                instruction = currentProgram
                    .getListing()
                    .getInstructionAfter(instruction.getAddress());

                printedInstructions++;
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Requested start address", requestedStartAddress);
            log.keyValue("First instruction address", firstInstruction.getAddress());
            log.keyValue("Requested instructions", requestedInstructionCount);
            log.keyValue("Printed instructions", printedInstructions);
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
            options.instructionCountText = args[1];
        }

        if (options.startAddressText == null || options.startAddressText.trim().isEmpty()) {
            options.startAddressText = askString(
                "Disassemble Around Address",
                "Start address:",
                DEFAULT_START_ADDRESS
            );
        }

        if (options.instructionCountText == null || options.instructionCountText.trim().isEmpty()) {
            options.instructionCountText = askString(
                "Disassemble Around Address",
                "Instruction count:",
                DEFAULT_INSTRUCTION_COUNT
            );
        }

        if (options.startAddressText == null || options.startAddressText.trim().isEmpty()) {
            options.startAddressText = DEFAULT_START_ADDRESS;
        }

        if (options.instructionCountText == null || options.instructionCountText.trim().isEmpty()) {
            options.instructionCountText = DEFAULT_INSTRUCTION_COUNT;
        }

        options.startAddressText = options.startAddressText.trim();
        options.instructionCountText = options.instructionCountText.trim();

        return options;
    }

    private Address parseTargetAddress(String addressText) {
        String normalized = addressText.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            normalized = normalized.substring(2);
        }

        return toAddr(normalized);
    }

    private int parseNumber(String value) {
        String normalized = value.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            return Integer.parseInt(normalized.substring(2), 16);
        }

        return Integer.parseInt(normalized, 10);
    }

    private static class ScriptOptions {
        private String startAddressText;
        private String instructionCountText;
    }
}
