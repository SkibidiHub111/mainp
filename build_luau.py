#!/usr/bin/env python3
"""Build the patched Luau runtime and luau-ast CLI for this project."""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys
import tempfile


ROOT = pathlib.Path(__file__).resolve().parent
BIN = ROOT / "bin"
LUAU_TAG = os.environ.get("LUAU_TAG", "0.739")
LUAU_REPO = "https://github.com/luau-lang/luau.git"


def run(*args: str, cwd: pathlib.Path | None = None) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def patch_vector_metatable(source: pathlib.Path) -> None:
    target = source / "VM" / "src" / "lveclib.cpp"
    text = target.read_text(encoding="utf-8")
    needle = "    lua_setreadonly(L, -1, true);\n"
    replacement = (
        "    // Writable for the offline Roblox Vector3 compatibility model.\n"
        "    // The deobfuscator never exposes this runtime to untrusted hosts.\n"
    )
    if needle not in text:
        raise RuntimeError("Luau source changed: vector metatable patch did not match")
    target.write_text(text.replace(needle, replacement, 1), encoding="utf-8")


def main() -> int:
    for tool in ("git", "cmake"):
        if shutil.which(tool) is None:
            print(f"Missing build tool: {tool}", file=sys.stderr)
            return 2

    generator = ["-G", "Ninja"] if shutil.which("ninja") else []
    jobs = os.environ.get("JOBS", str(max(1, min(4, os.cpu_count() or 1))))

    with tempfile.TemporaryDirectory(prefix="luau-build-") as td:
        source = pathlib.Path(td) / "luau"
        build = pathlib.Path(td) / "build"
        run("git", "clone", "--depth", "1", "--branch", LUAU_TAG, LUAU_REPO, str(source))
        patch_vector_metatable(source)
        run(
            "cmake", "-S", str(source), "-B", str(build), *generator,
            "-DCMAKE_BUILD_TYPE=Release",
            "-DLUAU_BUILD_TESTS=OFF",
            "-DLUAU_BUILD_WEB=OFF",
        )
        run(
            "cmake", "--build", str(build),
            "--target", "Luau.Repl.CLI", "Luau.Ast.CLI",
            "--parallel", jobs,
        )

        suffix = ".exe" if os.name == "nt" else ""
        BIN.mkdir(parents=True, exist_ok=True)
        for name in ("luau", "luau-ast"):
            built = build / (name + suffix)
            if not built.exists():
                raise FileNotFoundError(f"Build succeeded but {built} was not produced")
            dest = BIN / (name + suffix)
            shutil.copy2(built, dest)
            dest.chmod(dest.stat().st_mode | 0o111)
            print(f"Installed {dest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
