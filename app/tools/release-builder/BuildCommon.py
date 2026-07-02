#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


PROJECT_NAME = "HardTruck2-KingOfTheRoad"
APP_NAME = "OxiGames-HardTruck2-Patcher"

APP = Path(__file__).resolve().parents[2]

PATCHER_GUI = APP / "tools" / "patcher" / "gui.py"
PATCHES_DIR = APP / "patches"
RELEASE_DIR = APP / "release"

LICENSE = APP.parent / "LICENSE"
ROOT_README = APP.parent / "README.md"

RELEASE_README = RELEASE_DIR / "PackageREADME.md"
RELEASE_LICENSE = RELEASE_DIR / "LICENSE"


def main() -> int:
    if len(sys.argv) != 2:
        print("[ERROR] Usage: BuildCommon.py <linux|windows>")
        return 1

    platform = sys.argv[1].lower()

    if platform not in {"linux", "windows"}:
        print(f"[ERROR] Unsupported platform: {platform}")
        return 1

    build_release(platform)
    return 0


def build_release(platform: str) -> None:
    target_dir = RELEASE_DIR / platform_name(platform)
    work_dir = target_dir / "work"
    package_dir = work_dir / package_name(platform)

    clean(target_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    binary = build_binary(platform, work_dir)
    copy_release_files(binary, package_dir)
    create_zip(platform, target_dir, package_dir)

    print("[OK] Release package generated.")


def clean(target_dir: Path) -> None:
    if target_dir.exists():
        for child in target_dir.iterdir():
            if child.name == ".gitkeep":
                continue

            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()


def build_binary(platform: str, work_dir: Path) -> Path:
    binary_name = APP_NAME + (".exe" if platform == "windows" else "")
    dist_dir = work_dir / "dist"
    build_dir = work_dir / "build"

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name",
        binary_name,
        "--distpath",
        str(dist_dir),
        "--workpath",
        str(build_dir),
        str(PATCHER_GUI),
    ]

    print("[INFO] Running PyInstaller...")
    subprocess.run(command, cwd=APP, check=True)

    binary = dist_dir / binary_name

    if not binary.exists():
        raise RuntimeError(f"Binary was not created: {binary}")

    return binary


def copy_release_files(binary: Path, package_dir: Path) -> None:
    shutil.copy2(binary, package_dir / binary.name)

    if RELEASE_README.exists():
        shutil.copy2(RELEASE_README, package_dir / "README.md")

    if RELEASE_LICENSE.exists():
        shutil.copy2(RELEASE_LICENSE, package_dir / "LICENSE")

    if LICENSE.exists():
        shutil.copy2(LICENSE, package_dir / "LICENSE")

    if ROOT_README.exists():
        shutil.copy2(ROOT_README, package_dir / "README.md")

    shutil.copytree(PATCHES_DIR, package_dir / "patches")


def create_zip(platform: str, target_dir: Path, package_dir: Path) -> None:
    archive_name = f"{package_name(platform)}.zip"
    archive_path = target_dir / archive_name

    if archive_path.exists():
        archive_path.unlink()

    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in package_dir.rglob("*"):
            archive.write(item, item.relative_to(package_dir.parent))

    print(f"[OK] Archive: {archive_path}")


def platform_name(platform: str) -> str:
    if platform == "linux":
        return "Linux"

    if platform == "windows":
        return "Windows"

    raise RuntimeError(f"Unsupported platform: {platform}")


def package_name(platform: str) -> str:
    suffix = "linux-x64" if platform == "linux" else "windows-x64"
    return f"{PROJECT_NAME}-{suffix}"


if __name__ == "__main__":
    raise SystemExit(main())