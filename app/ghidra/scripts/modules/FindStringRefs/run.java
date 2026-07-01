package modules.FindStringRefs;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import lib.FileUtils;
import lib.Logger;

import java.io.File;

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "FindStringRefs";
    private static final String DEFAULT_NEEDLE = "avi subsystem error";

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();

            log.section("Find String References");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Search text", options.needle);
            log.keyValue("Ignore case", options.ignoreCase);
            log.keyValue("Exact match", options.exactMatch);

            int matchedStrings = 0;
            int matchedReferences = 0;

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

                ReferenceIterator references = currentProgram
                    .getReferenceManager()
                    .getReferencesTo(stringAddress);

                boolean hasReferences = false;

                while (references.hasNext()) {
                    Reference reference = references.next();

                    hasReferences = true;
                    matchedReferences++;

                    log.raw(
                        "  REF: "
                            + reference.getFromAddress()
                            + " -> "
                            + stringAddress
                            + " type="
                            + reference.getReferenceType()
                    );
                }

                if (!hasReferences) {
                    log.raw("  REF: none");
                }
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Matched strings", matchedStrings);
            log.keyValue("Matched references", matchedReferences);
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

                if ("--exact".equals(arg)) {
                    options.exactMatch = true;
                    continue;
                }

                if (needleBuilder.length() > 0) {
                    needleBuilder.append(" ");
                }

                needleBuilder.append(arg);
            }

            options.needle = needleBuilder.toString().trim();
        }

        if (options.needle == null || options.needle.isEmpty()) {
            options.needle = askString(
                "Find String References",
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

        if (options.exactMatch) {
            return haystack.equals(needle);
        }

        return haystack.contains(needle);
    }

    private static class ScriptOptions {
        private String needle;
        private boolean ignoreCase = false;
        private boolean exactMatch = false;
    }
}