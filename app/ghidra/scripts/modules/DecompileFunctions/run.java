package modules.DecompileFunctions;

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

import lib.FileUtils;
import lib.Logger;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Decompile one or more functions containing specified addresses.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "DecompileFunctions";
    private static final String DEFAULT_ADDRESS = "005279e0";
    private static final String DEFAULT_OUTPUT_MODE = "c";
    private static final int DECOMPILE_TIMEOUT_SECONDS = 60;

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);
        DecompInterface decompiler = new DecompInterface();

        try {
            ScriptOptions options = parseOptions();

            decompiler.openProgram(currentProgram);

            log.section("Decompile Functions");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Output mode", options.outputMode);
            log.keyValue("Requested addresses", options.addressTexts.size());

            int functionsFound = 0;
            int functionsDecompiled = 0;
            int failed = 0;

            for (String addressText : options.addressTexts) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                Address address = parseTargetAddress(addressText);
                Function function = getFunctionContaining(address);

                log.emptyLine();
                log.section("Function");
                log.keyValue("Requested address", address);

                if (function == null) {
                    failed++;
                    log.warn("No function found for requested address.");
                    continue;
                }

                functionsFound++;

                log.keyValue("Function", function.getName());
                log.keyValue("Function entry", function.getEntryPoint());
                log.keyValue("Output mode", options.outputMode);

                DecompileResults results = decompiler.decompileFunction(
                    function,
                    DECOMPILE_TIMEOUT_SECONDS,
                    monitor
                );

                if (!results.decompileCompleted()) {
                    failed++;
                    log.error("Decompile failed: " + results.getErrorMessage());
                    continue;
                }

                functionsDecompiled++;

                if ("signature".equals(options.outputMode)) {
                    log.emptyLine();
                    log.raw(results.getDecompiledFunction().getSignature());
                    continue;
                }

                log.emptyLine();
                log.raw(results.getDecompiledFunction().getC());
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Requested addresses", options.addressTexts.size());
            log.keyValue("Functions found", functionsFound);
            log.keyValue("Functions decompiled", functionsDecompiled);
            log.keyValue("Failed", failed);
            log.ok("Done.");
        } finally {
            decompiler.dispose();
            log.close();
        }
    }

    private ScriptOptions parseOptions() throws Exception {
        ScriptOptions options = new ScriptOptions();

        String[] args = getScriptArgs();

        if (args != null) {
            for (String arg : args) {
                if (arg == null || arg.trim().isEmpty()) {
                    continue;
                }

                String trimmed = arg.trim();

                if (trimmed.startsWith("--output=")) {
                    options.outputMode = normalizeOutputMode(trimmed.substring("--output=".length()));
                    continue;
                }

                options.addressTexts.add(trimmed);
            }
        }

        if (options.addressTexts.isEmpty()) {
            String addressText = askString(
                "Decompile Functions",
                "Address:",
                DEFAULT_ADDRESS
            );

            if (addressText == null || addressText.trim().isEmpty()) {
                addressText = DEFAULT_ADDRESS;
            }

            options.addressTexts.add(addressText.trim());
        }

        if (options.outputMode == null || options.outputMode.trim().isEmpty()) {
            options.outputMode = DEFAULT_OUTPUT_MODE;
        }

        options.outputMode = normalizeOutputMode(options.outputMode);

        return options;
    }

    private String normalizeOutputMode(String outputMode) {
        String normalized = outputMode.trim().toLowerCase();

        if ("c".equals(normalized)) {
            return normalized;
        }

        if ("signature".equals(normalized)) {
            return normalized;
        }

        throw new IllegalArgumentException(
            "Unsupported output mode: " + outputMode + ". Supported modes: c, signature."
        );
    }

    private Address parseTargetAddress(String addressText) {
        String normalized = addressText.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            normalized = normalized.substring(2);
        }

        return toAddr(normalized);
    }

    private static class ScriptOptions {
        private final List<String> addressTexts = new ArrayList<String>();
        private String outputMode = DEFAULT_OUTPUT_MODE;
    }
}
