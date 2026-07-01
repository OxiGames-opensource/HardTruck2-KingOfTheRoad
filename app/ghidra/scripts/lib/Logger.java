package lib;

import ghidra.app.script.GhidraScript;

import java.io.BufferedWriter;
import java.io.Closeable;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;

public class Logger implements Closeable {
    private static final String LOG_FILE_DATE_FORMAT = "yyyy-MM-dd_HH-mm-ss";

    private final GhidraScript script;
    private final File resultDirectory;
    private final File logFile;
    private final PrintWriter writer;

    public Logger(GhidraScript script, File resultDirectory) throws Exception {
        if (script == null) {
            throw new IllegalArgumentException("Ghidra script instance is required.");
        }

        if (resultDirectory == null) {
            throw new IllegalArgumentException("Result directory is required.");
        }

        this.script = script;
        this.resultDirectory = resultDirectory;

        ensureResultDirectoryExists(this.resultDirectory);

        this.logFile = new File(this.resultDirectory, createLogFileName());
        this.writer = new PrintWriter(
            new BufferedWriter(
                new OutputStreamWriter(
                    new FileOutputStream(this.logFile, false),
                    StandardCharsets.UTF_8
                )
            )
        );

        info("Log file: " + this.logFile.getAbsolutePath());
    }

    public File getResultDirectory() {
        return resultDirectory;
    }

    public File getLogFile() {
        return logFile;
    }

    public void section(String title) {
        println("");
        println("=== " + title + " ===");
    }

    public void info(String message) {
        println("[INFO] " + safeMessage(message));
    }

    public void ok(String message) {
        println("[OK] " + safeMessage(message));
    }

    public void warn(String message) {
        println("[WARN] " + safeMessage(message));
    }

    public void error(String message) {
        println("[ERROR] " + safeMessage(message));
    }

    public void raw(String message) {
        println(safeMessage(message));
    }

    public void keyValue(String key, Object value) {
        println(safeMessage(key) + ": " + String.valueOf(value));
    }

    public void emptyLine() {
        println("");
    }

    private void println(String message) {
        String line = safeMessage(message);

        script.println(line);

        writer.println(line);
        writer.flush();
    }

    private static void ensureResultDirectoryExists(File directory) throws Exception {
        if (directory.exists()) {
            if (!directory.isDirectory()) {
                throw new IllegalStateException(
                    "Result path exists but is not a directory: " + directory.getAbsolutePath()
                );
            }

            return;
        }

        if (!directory.mkdirs()) {
            throw new IllegalStateException(
                "Failed to create result directory: " + directory.getAbsolutePath()
            );
        }
    }

    private static String createLogFileName() {
        String timestamp = new SimpleDateFormat(LOG_FILE_DATE_FORMAT).format(new Date());

        return timestamp + ".log";
    }

    private static String safeMessage(String message) {
        if (message == null) {
            return "";
        }

        return message;
    }

    @Override
    public void close() {
        writer.flush();
        writer.close();
    }
}