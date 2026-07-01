package lib;

import java.io.File;
import java.io.IOException;

public class FileUtils {
    private FileUtils() {
    }

    public static File requireDirectory(File directory, String label) {
        if (directory == null) {
            throw new IllegalArgumentException(label + " is required.");
        }

        if (!directory.exists()) {
            throw new IllegalStateException(
                label + " does not exist: " + directory.getAbsolutePath()
            );
        }

        if (!directory.isDirectory()) {
            throw new IllegalStateException(
                label + " is not a directory: " + directory.getAbsolutePath()
            );
        }

        return directory;
    }

    public static File ensureDirectory(File directory, String label) {
        if (directory == null) {
            throw new IllegalArgumentException(label + " is required.");
        }

        if (directory.exists()) {
            if (!directory.isDirectory()) {
                throw new IllegalStateException(
                    label + " exists but is not a directory: " + directory.getAbsolutePath()
                );
            }

            return directory;
        }

        if (!directory.mkdirs()) {
            throw new IllegalStateException(
                "Failed to create " + label + ": " + directory.getAbsolutePath()
            );
        }

        return directory;
    }

    public static File resolveResultDirectory(File scriptDirectory) {
        requireDirectory(scriptDirectory, "Script directory");

        return ensureDirectory(new File(scriptDirectory, "result"), "Result directory");
    }

    public static String canonicalPath(File file) {
        if (file == null) {
            return "";
        }

        try {
            return file.getCanonicalPath();
        } catch (IOException exception) {
            return file.getAbsolutePath();
        }
    }
}