package modules.TraceStringCallers;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;

import lib.FileUtils;
import lib.Logger;

import java.io.File;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Find strings matching a user-provided text fragment, trace references to those strings,
 * identify containing functions, and list callers of those functions.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "TraceStringCallers";
    private static final String DEFAULT_NEEDLE = "Your computer does not have graphic accelerator";

    @Override
    protected void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();

            log.section("Trace String Callers");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Search text", options.needle);
            log.keyValue("Ignore case", options.ignoreCase);

            int matchedStrings = 0;
            int stringReferences = 0;
            int functionsFound = 0;
            int callersFound = 0;

            for (Data data : currentProgram.getListing().getDefinedData(true)) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                if (!data.hasStringValue()) {
                    continue;
                }

                Object value = data.getValue();

                if (value == null) {
                    continue;
                }

                String text = value.toString();

                if (!matches(text, options)) {
                    continue;
                }

                matchedStrings++;

                Address stringAddress = data.getAddress();

                log.emptyLine();
                log.raw("STRING: " + stringAddress + " = " + text);

                Reference[] referencesToString = getReferencesTo(stringAddress);

                if (referencesToString.length == 0) {
                    log.raw("  XREF: none");
                    continue;
                }

                for (Reference reference : referencesToString) {
                    if (monitor.isCancelled()) {
                        log.warn("Script cancelled.");
                        return;
                    }

                    stringReferences++;

                    Address fromAddress = reference.getFromAddress();
                    Function function = getFunctionContaining(fromAddress);

                    log.emptyLine();
                    log.raw("XREF FROM: " + fromAddress);
                    log.keyValue("Reference type", reference.getReferenceType());

                    if (function == null) {
                        log.keyValue("Function", "none");
                        continue;
                    }

                    functionsFound++;

                    log.keyValue("Function", function.getName());
                    log.keyValue("Function entry", function.getEntryPoint());

                    Reference[] callers = getReferencesTo(function.getEntryPoint());

                    if (callers.length == 0) {
                        log.raw("  CALLER: none");
                        continue;
                    }

                    for (Reference callerReference : callers) {
                        if (monitor.isCancelled()) {
                            log.warn("Script cancelled.");
                            return;
                        }

                        callersFound++;

                        Address callerAddress = callerReference.getFromAddress();
                        Function callerFunction = getFunctionContaining(callerAddress);

                        log.raw("  CALLER XREF: " + callerAddress);
                        log.raw("    Type: " + callerReference.getReferenceType());

                        if (callerFunction == null) {
                            log.raw("    Function: none");
                        } else {
                            log.raw("    Function: " + callerFunction.getName());
                            log.raw("    Function entry: " + callerFunction.getEntryPoint());
                        }
                    }
                }
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Matched strings", matchedStrings);
            log.keyValue("String references", stringReferences);
            log.keyValue("Containing functions", functionsFound);
            log.keyValue("Callers found", callersFound);
            log.ok("Done.");
        } finally {
            log.close();
        }
    }

    private ScriptOptions parseOptions() throws Exception {
        ScriptOptions options = new ScriptOptions();

        String[] args = getScriptArgs();

        if (args != null && args.length > 0) {
            StringBuilder needleBuilder = new StringBuilder();

            for (String arg : args) {
                if ("--ignore-case".equals(arg)) {
                    options.ignoreCase = true;
                    continue;
                }

                if (needleBuilder.length() > 0) {
                    needleBuilder.append(" ");
                }

                needleBuilder.append(arg);
            }

            options.needle = needleBuilder.toString().trim();
        }

        if (options.needle == null || options.needle.trim().isEmpty()) {
            options.needle = askString(
                "Trace String Callers",
                "String fragment to search for:",
                DEFAULT_NEEDLE
            );
        }

        if (options.needle == null || options.needle.trim().isEmpty()) {
            options.needle = DEFAULT_NEEDLE;
        }

        options.needle = options.needle.trim();

        return options;
    }

    private boolean matches(String text, ScriptOptions options) {
        String haystack = text;
        String needle = options.needle;

        if (options.ignoreCase) {
            haystack = haystack.toLowerCase();
            needle = needle.toLowerCase();
        }

        return haystack.contains(needle);
    }

    private static class ScriptOptions {
        private String needle;
        private boolean ignoreCase = false;
    }
}
