package modules.FindMultipleStrings;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Data;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

import lib.FileUtils;
import lib.Logger;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

/*
 * OxiGames - Hard Truck 2: King of the Road
 *
 * Purpose:
 * Search for multiple strings and report their addresses and references.
 *
 * This script is intended for use with a legally purchased copy of the game.
 * It does not include or distribute original game files.
 */

public class run extends GhidraScript {
    private static final String SCRIPT_NAME = "FindMultipleStrings";
    private static final String DEFAULT_SEARCH_TEXT = "avi subsystem error";

    @Override
    public void run() throws Exception {
        File scriptDirectory = new File("ghidra/scripts/modules/" + SCRIPT_NAME);
        File resultDirectory = FileUtils.resolveResultDirectory(scriptDirectory);

        Logger log = new Logger(this, resultDirectory);

        try {
            ScriptOptions options = parseOptions();

            log.section("Find Multiple Strings");
            log.keyValue("Script", SCRIPT_NAME);
            log.keyValue("Search strings", options.searchTexts.size());
            log.keyValue("Ignore case", options.ignoreCase);

            int matchedStrings = 0;
            int referencesFound = 0;

            for (String searchText : options.searchTexts) {
                if (monitor.isCancelled()) {
                    log.warn("Script cancelled.");
                    return;
                }

                log.emptyLine();
                log.section("Search");
                log.keyValue("Text", searchText);

                int matchesForSearch = 0;
                int referencesForSearch = 0;

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

                    String actualText = value.toString();

                    if (!matches(actualText, searchText, options.ignoreCase)) {
                        continue;
                    }

                    matchesForSearch++;
                    matchedStrings++;

                    Address stringAddress = data.getAddress();

                    log.emptyLine();
                    log.raw("STRING: " + stringAddress + " = " + actualText);

                    ReferenceIterator references = currentProgram
                        .getReferenceManager()
                        .getReferencesTo(stringAddress);

                    List<Reference> referenceList = new ArrayList<Reference>();

                    while (references.hasNext()) {
                        referenceList.add(references.next());
                    }

                    referencesForSearch += referenceList.size();
                    referencesFound += referenceList.size();

                    log.keyValue("XREF count", referenceList.size());

                    for (Reference reference : referenceList) {
                        log.raw(
                            "  XREF: "
                                + reference.getFromAddress()
                                + " type="
                                + reference.getReferenceType()
                        );
                    }
                }

                if (matchesForSearch == 0) {
                    log.raw("No matches.");
                }

                log.emptyLine();
                log.keyValue("Matches for search", matchesForSearch);
                log.keyValue("References for search", referencesForSearch);
            }

            log.emptyLine();
            log.section("Summary");
            log.keyValue("Search strings", options.searchTexts.size());
            log.keyValue("Matched strings", matchedStrings);
            log.keyValue("References found", referencesFound);
            log.ok("Done.");
        } finally {
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

                if ("--ignore-case".equals(trimmed)) {
                    options.ignoreCase = true;
                    continue;
                }

                if (trimmed.startsWith("--file=")) {
                    options.filePath = trimmed.substring("--file=".length()).trim();
                    continue;
                }

                options.searchTexts.add(trimmed);
            }
        }

        if (options.filePath != null && !options.filePath.isEmpty()) {
            options.searchTexts.addAll(loadSearchTextsFromFile(options.filePath));
        }

        if (options.searchTexts.isEmpty()) {
            String searchText = askString(
                "Find Multiple Strings",
                "Search text:",
                DEFAULT_SEARCH_TEXT
            );

            if (searchText == null || searchText.trim().isEmpty()) {
                searchText = DEFAULT_SEARCH_TEXT;
            }

            options.searchTexts.add(searchText.trim());
        }

        return options;
    }

    private List<String> loadSearchTextsFromFile(String filePath) throws Exception {
        List<String> lines = new ArrayList<String>();
        File file = new File(filePath);

        if (!file.exists()) {
            throw new IllegalStateException("Search file does not exist: " + file.getAbsolutePath());
        }

        if (!file.isFile()) {
            throw new IllegalStateException("Search file is not a file: " + file.getAbsolutePath());
        }

        BufferedReader reader = new BufferedReader(new FileReader(file));

        try {
            String line;

            while ((line = reader.readLine()) != null) {
                String trimmed = line.trim();

                if (trimmed.isEmpty()) {
                    continue;
                }

                if (trimmed.startsWith("#")) {
                    continue;
                }

                lines.add(trimmed);
            }
        } finally {
            reader.close();
        }

        return lines;
    }

    private boolean matches(String actualText, String searchText, boolean ignoreCase) {
        if (ignoreCase) {
            return actualText.toLowerCase().contains(searchText.toLowerCase());
        }

        return actualText.contains(searchText);
    }

    private static class ScriptOptions {
        private final List<String> searchTexts = new ArrayList<String>();
        private boolean ignoreCase = false;
        private String filePath;
    }
}
