#!/usr/bin/env python3
from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from core import (
    PatcherError,
    apply_patches,
    default_patches_dir,
    get_status,
    load_all_patches,
    restore_original,
    rollback_patches,
)


class PatcherGui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("OxiGames - Hard Truck 2 Patcher")
        self.geometry("760x500")
        self.minsize(720, 460)

        self.patches_dir = default_patches_dir()
        self.patches = load_all_patches(self.patches_dir)

        self.game_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Choose king.exe or the game directory.")

        self.patch_vars: dict[str, tk.BooleanVar] = {}
        self.patch_statuses: dict[str, str] = {}
        self.patch_status_labels: dict[str, ttk.Label] = {}

        self.build_ui()
        self.render_patches()

    def build_ui(self) -> None:
        root = ttk.Frame(self, padding=16)
        root.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            root,
            text="OxiGames - Hard Truck 2: King of the Road",
            font=("TkDefaultFont", 14, "bold"),
        )
        title.pack(anchor=tk.W)

        subtitle = ttk.Label(
            root,
            text="Compatibility patcher for legally obtained copies of the game.",
        )
        subtitle.pack(anchor=tk.W, pady=(2, 14))

        game_frame = ttk.LabelFrame(root, text="Game executable", padding=10)
        game_frame.pack(fill=tk.X)

        game_entry = ttk.Entry(game_frame, textvariable=self.game_path_var)
        game_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        browse_button = ttk.Button(game_frame, text="Browse...", command=self.browse_game)
        browse_button.pack(side=tk.LEFT, padx=(8, 0))

        refresh_button = ttk.Button(game_frame, text="Refresh", command=self.refresh_status)
        refresh_button.pack(side=tk.LEFT, padx=(8, 0))

        patches_frame = ttk.LabelFrame(root, text="Patches", padding=10)
        patches_frame.pack(fill=tk.BOTH, expand=True, pady=(14, 0))

        hint = ttk.Label(
            patches_frame,
            text="Checked means the patch should be applied. Unchecked means the patch should be rolled back.",
        )
        hint.pack(anchor=tk.W, pady=(0, 8))

        self.patches_container = ttk.Frame(patches_frame)
        self.patches_container.pack(fill=tk.BOTH, expand=True)

        actions_frame = ttk.Frame(root)
        actions_frame.pack(fill=tk.X, pady=(14, 0))

        apply_button = ttk.Button(actions_frame, text="Apply changes", command=self.apply_changes)
        apply_button.pack(side=tk.LEFT)

        restore_button = ttk.Button(actions_frame, text="Restore original", command=self.restore_original)
        restore_button.pack(side=tk.LEFT, padx=(8, 0))

        exit_button = ttk.Button(actions_frame, text="Exit", command=self.destroy)
        exit_button.pack(side=tk.RIGHT)

        status_frame = ttk.LabelFrame(root, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(14, 0))

        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)

    def render_patches(self) -> None:
        for child in self.patches_container.winfo_children():
            child.destroy()

        if not self.patches:
            ttk.Label(self.patches_container, text="No patches found.").pack(anchor=tk.W)
            return

        for patch in self.patches:
            row = ttk.Frame(self.patches_container)
            row.pack(fill=tk.X, pady=4)

            var = tk.BooleanVar(value=False)
            self.patch_vars[patch.patch_id] = var
            self.patch_statuses[patch.patch_id] = "unknown"

            checkbox = ttk.Checkbutton(
                row,
                text=patch.title,
                variable=var,
            )
            checkbox.pack(side=tk.LEFT)

            patch_id_label = ttk.Label(row, text=f"({patch.patch_id})")
            patch_id_label.pack(side=tk.LEFT, padx=(8, 0))

            status_label = ttk.Label(row, text="not checked", width=16)
            status_label.pack(side=tk.RIGHT)

            self.patch_status_labels[patch.patch_id] = status_label

    def browse_game(self) -> None:
        selected_file = filedialog.askopenfilename(
            title="Select king.exe",
            filetypes=[
                ("Game executable", "king.exe"),
                ("Executable files", "*.exe"),
                ("All files", "*.*"),
            ],
        )

        if selected_file:
            self.game_path_var.set(selected_file)
            self.refresh_status()
            return

        selected_dir = filedialog.askdirectory(
            title="Or select game directory",
        )

        if selected_dir:
            self.game_path_var.set(selected_dir)
            self.refresh_status()

    def selected_game_path(self) -> Path:
        value = self.game_path_var.get().strip()

        if not value:
            raise PatcherError("Game executable or game directory is not selected.")

        return Path(value).expanduser().resolve()

    def patches_by_id(self):
        return {patch.patch_id: patch for patch in self.patches}

    def refresh_status(self) -> None:
        try:
            game_path = self.selected_game_path()
            statuses = get_status(game_path, self.patches)

            for status in statuses:
                label = self.patch_status_labels.get(status.patch_id)
                var = self.patch_vars.get(status.patch_id)

                self.patch_statuses[status.patch_id] = status.status

                if label is not None:
                    label.configure(text=status.status)

                if var is not None:
                    if status.status == "patched":
                        var.set(True)
                    elif status.status == "original":
                        var.set(False)
                    else:
                        var.set(False)

            self.status_var.set("Status refreshed.")
        except Exception as exc:
            self.status_var.set(str(exc))
            messagebox.showerror("OxiGames Patcher", str(exc))

    def apply_changes(self) -> None:
        try:
            game_path = self.selected_game_path()
            by_id = self.patches_by_id()

            patches_to_apply = []
            patches_to_rollback = []
            unknown = []

            for patch_id, var in self.patch_vars.items():
                current_status = self.patch_statuses.get(patch_id, "unknown")
                desired_applied = var.get()
                patch = by_id[patch_id]

                if current_status == "unknown":
                    unknown.append(patch_id)
                    continue

                if desired_applied and current_status == "original":
                    patches_to_apply.append(patch)
                    continue

                if not desired_applied and current_status == "patched":
                    patches_to_rollback.append(patch)
                    continue

            messages = []

            if patches_to_apply:
                apply_results = apply_patches(game_path, patches_to_apply)
                messages.extend(
                    f"{result.patch_id}: {result.message}"
                    for result in apply_results
                )

            if patches_to_rollback:
                rollback_results = rollback_patches(game_path, patches_to_rollback)
                messages.extend(
                    f"{result.patch_id}: {result.message}"
                    for result in rollback_results
                )

            if unknown:
                messages.append(
                    "Skipped unknown patch states: " + ", ".join(unknown)
                )

            if not messages:
                messages.append("No changes required.")

            self.refresh_status()
            self.status_var.set("Changes applied.")
            messagebox.showinfo("OxiGames Patcher", "\n".join(messages))
        except Exception as exc:
            self.status_var.set(str(exc))
            messagebox.showerror("OxiGames Patcher", str(exc))

    def restore_original(self) -> None:
        if not messagebox.askyesno(
            "OxiGames Patcher",
            "Restore the original executable from backup?\n\nThis restores the whole file, not individual patches.",
        ):
            return

        try:
            results = restore_original(self.selected_game_path(), self.patches)
            self.refresh_status()

            message = "\n".join(
                f"{result.target.name}: {result.message}"
                for result in results
            )
            self.status_var.set("Original file restore finished.")
            messagebox.showinfo("OxiGames Patcher", message or "Nothing restored.")
        except Exception as exc:
            self.status_var.set(str(exc))
            messagebox.showerror("OxiGames Patcher", str(exc))


def main() -> int:
    app = PatcherGui()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
