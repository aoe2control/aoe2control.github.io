#!/usr/bin/env python3
"""Validate executable examples embedded in the MkDocs Markdown sources."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


FENCE_START = re.compile(r"^```([^\s`]*)\s*$")
FENCE_END = re.compile(r"^```\s*$")
GLOBAL_CALL = re.compile(r"(?<![.:\w])([A-Z][A-Za-z0-9_]*)\s*\(")
DEFINED_FUNCTION = re.compile(r"\bfunction\s+([A-Z][A-Za-z0-9_]*)\s*\(")
TABLE_CALL = re.compile(r"\b(Settings|IPC)\.([A-Za-z_][A-Za-z0-9_]*)\s*\(")
METHOD_CALL = re.compile(r":([A-Z][A-Za-z0-9_]*)\s*\(")
CONSTRUCTOR_CALL = re.compile(r"\b([A-Z][A-Za-z0-9_]*):new\s*\(")
ENUM_VALUE = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\.([A-Za-z_][A-Za-z0-9_]*)\b")


@dataclass(frozen=True)
class CodeBlock:
    path: Path
    line: int
    language: str
    source: str

    @property
    def location(self) -> str:
        return f"{self.path.as_posix()}:{self.line}"


def extract_blocks(docs_root: Path) -> list[CodeBlock]:
    blocks: list[CodeBlock] = []
    for path in sorted(docs_root.rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        language: str | None = None
        start_line = 0
        body: list[str] = []
        for index, line in enumerate(lines, start=1):
            if language is None:
                match = FENCE_START.fullmatch(line)
                if match:
                    language = match.group(1).lower()
                    start_line = index + 1
                    body = []
                continue
            if FENCE_END.fullmatch(line):
                blocks.append(CodeBlock(path, start_line, language, "\n".join(body) + "\n"))
                language = None
                body = []
                continue
            body.append(line)
        if language is not None:
            raise ValueError(f"{path.as_posix()}:{start_line - 1}: unterminated code fence")
    return blocks


def validate_lua(block: CodeBlock, compiler: Path) -> str | None:
    with tempfile.TemporaryDirectory(prefix="aoe2control-doc-example-") as temp_directory:
        source_path = Path(temp_directory) / "example.lua"
        source_path.write_text(block.source, encoding="utf-8")
        if compiler.name.lower().startswith("luac"):
            command = [str(compiler), "-p", str(source_path)]
        else:
            command = [str(compiler), str(source_path)]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            return None
        detail = (result.stderr or result.stdout).strip()
        return detail or f"Lua compiler exited with {result.returncode}"


def validate_powershell(block: CodeBlock, executable: Path) -> str | None:
    with tempfile.TemporaryDirectory(prefix="aoe2control-doc-example-") as temp_directory:
        temp_path = Path(temp_directory)
        source_path = temp_path / "example.ps1"
        parser_path = temp_path / "parse-example.ps1"
        source_path.write_text(block.source, encoding="utf-8")
        parser_path.write_text(
            """param([string]$SourcePath)
$tokens = $null
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
    $SourcePath,
    [ref]$tokens,
    [ref]$errors
) | Out-Null
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { [Console]::Error.WriteLine($_.Message) }
    exit 1
}
""",
            encoding="utf-8",
        )
        result = subprocess.run(
            [
                str(executable),
                "-NoLogo",
                "-NoProfile",
                "-NonInteractive",
                "-File",
                str(parser_path),
                str(source_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return None
        detail = (result.stderr or result.stdout).strip()
        return detail or f"PowerShell parser exited with {result.returncode}"


def load_enum_members(paths: list[Path]) -> dict[str, set[str]]:
    members: dict[str, set[str]] = {}
    pattern = re.compile(r"\benum\s+class\s+(\w+)\s*(?::[^\{]+)?\{(.*?)\};", re.DOTALL)
    for path in paths:
        source = re.sub(r"//.*?$|/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.MULTILINE | re.DOTALL)
        for match in pattern.finditer(source):
            enum_name, body = match.groups()
            enum_members = members.setdefault(enum_name, set())
            for entry in body.split(","):
                member = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)", entry)
                if member:
                    enum_members.add(member.group(1))
    return members


def validate_contract(
    block: CodeBlock,
    manifest: dict[str, object],
    enum_members: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    global_functions = set(manifest["globalFunctions"])
    lifecycle_callbacks = set(manifest["lifecycleCallbacks"])
    usertypes = manifest["usertypes"]
    tables = manifest["tables"]
    enum_names = set(manifest["enums"])

    defined_functions = set(DEFINED_FUNCTION.findall(block.source))
    constructors = {
        name for name, value in usertypes.items()
        if int(value.get("constructors", 0)) > 0
    }
    permitted_globals = global_functions | lifecycle_callbacks | constructors | defined_functions
    for name in sorted(set(GLOBAL_CALL.findall(block.source)) - permitted_globals):
        errors.append(f"unknown Lua global function or constructor '{name}'")

    for table_name, member_name in sorted(set(TABLE_CALL.findall(block.source))):
        if member_name not in tables.get(table_name, {}):
            errors.append(f"unknown Lua table function '{table_name}.{member_name}'")

    known_methods = {
        member
        for usertype in usertypes.values()
        for member in usertype.get("members", {})
    }
    for method_name in sorted(set(METHOD_CALL.findall(block.source)) - known_methods):
        errors.append(f"unknown Lua userdata method '{method_name}'")

    for constructor_name in sorted(set(CONSTRUCTOR_CALL.findall(block.source)) - constructors):
        errors.append(f"unknown or non-constructible Lua userdata '{constructor_name}'")

    for enum_name, member_name in sorted(set(ENUM_VALUE.findall(block.source))):
        if enum_name not in enum_names:
            if enum_name not in tables:
                errors.append(f"unknown Lua enum table '{enum_name}'")
        elif enum_name in enum_members and member_name not in enum_members[enum_name]:
            errors.append(f"unknown Lua enum value '{enum_name}.{member_name}'")

    return errors


def resolve_compiler(argument: str | None) -> Path | None:
    if argument:
        candidate = Path(argument).resolve()
        if not candidate.is_file():
            raise FileNotFoundError(f"Lua compiler not found: {candidate}")
        return candidate
    for name in ("luac5.4", "luac54", "luac"):
        resolved = shutil.which(name)
        if resolved:
            return Path(resolved)
    return None


def resolve_powershell(argument: str | None) -> Path | None:
    if argument:
        candidate = Path(argument).resolve()
        if not candidate.is_file():
            raise FileNotFoundError(f"PowerShell executable not found: {candidate}")
        return candidate
    resolved = shutil.which("pwsh")
    return Path(resolved) if resolved else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs", type=Path, default=Path("docs"))
    parser.add_argument("--lua-compiler")
    parser.add_argument("--powershell")
    parser.add_argument("--lua-api-manifest", type=Path)
    parser.add_argument("--lua-enum-source", action="append", type=Path, default=[])
    args = parser.parse_args()

    compiler = resolve_compiler(args.lua_compiler)
    if compiler is None:
        print("A Lua 5.4 compiler is required (use --lua-compiler).", file=sys.stderr)
        return 2
    powershell = resolve_powershell(args.powershell)
    if powershell is None:
        print("PowerShell is required (use --powershell).", file=sys.stderr)
        return 2

    manifest = None
    if args.lua_api_manifest:
        manifest = json.loads(args.lua_api_manifest.read_text(encoding="utf-8"))
    enum_members = load_enum_members(args.lua_enum_source)

    blocks = extract_blocks(args.docs)
    counts: dict[str, int] = {}
    failures: list[str] = []
    for block in blocks:
        counts[block.language] = counts.get(block.language, 0) + 1
        try:
            if block.language == "lua":
                lua_error = validate_lua(block, compiler)
                if lua_error:
                    failures.append(f"{block.location}: {lua_error}")
                if manifest is not None:
                    failures.extend(
                        f"{block.location}: {message}"
                        for message in validate_contract(block, manifest, enum_members)
                    )
            elif block.language == "python":
                ast.parse(block.source, filename=block.location)
            elif block.language == "json":
                json.loads(block.source)
            elif block.language in {"powershell", "ps1"}:
                powershell_error = validate_powershell(block, powershell)
                if powershell_error:
                    failures.append(f"{block.location}: {powershell_error}")
        except (SyntaxError, ValueError, json.JSONDecodeError) as error:
            failures.append(f"{block.location}: {error}")

    if failures:
        print("Documentation example validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    checked = ", ".join(
        f"{counts.get(language, 0)} {language}"
        for language in ("lua", "python", "json", "powershell")
    )
    contract_suffix = " with Lua API contract checks" if manifest is not None else ""
    print(f"Validated {checked} documentation examples{contract_suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
