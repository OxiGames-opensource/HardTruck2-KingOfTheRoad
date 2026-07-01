package modules.FindRefsToAddress;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import lib.FileUtils;
import lib.Logger;

import java.io.File;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Find all references to a specified address.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "FindRefsToAddress";
    private static final String DEFAULT_TARGET_ADDRESS = "005279e0";

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();
            Address targetAddress = parseTargetAddress(options.targetAddressText);

            log.section("Find References To Address");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Target address", targetAddress);

            int referencesFound = 0;

            ReferenceIterator references = currentProgram
                .getReferenceManager()
                .getReferencesTo(targetAddress);

            while (references.hasNext()) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                Reference reference = references.next();
                referencesFound++;

                Address fromAddress = reference.getFromAddress();
                Function function = getFunctionContaining(fromAddress);

                log.emptyLine();
                log.raw("REF: " + fromAddress + " -> " + targetAddress);
                log.keyValue("Type", reference.getReferenceType());
                log.keyValue("Function", function != null ? function.getName() : "none");
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Target address", targetAddress);
            log.keyValue("References found", referencesFound);
            log.ok("Done.");
        } finally {
            log.close();
        }
    }

    private ScriptOptions parseOptions() throws Exception {
        ScriptOptions options = new ScriptOptions();

        String[] args = getScriptArgs();

        if (args != null && args.length > 0) {
            options.targetAddressText = args[0];
        }

        if (options.targetAddressText == null || options.targetAddressText.trim().isEmpty()) {
            options.targetAddressText = askString(
                "Find References To Address",
                "Target address:",
                DEFAULT_TARGET_ADDRESS
            );
        }

        if (options.targetAddressText == null || options.targetAddressText.trim().isEmpty()) {
            options.targetAddressText = DEFAULT_TARGET_ADDRESS;
        }

        options.targetAddressText = options.targetAddressText.trim();

        return options;
    }

    private Address parseTargetAddress(String addressText) {
        String normalized = addressText.trim();

        if (normalized.startsWith("0x") || normalized.startsWith("0X")) {
            normalized = normalized.substring(2);
        }

        return toAddr(normalized);
    }

    private static class ScriptOptions {
        private String targetAddressText;
    }
}