#!/usr/bin/env python3
"""Build a deterministic self-contained installable software-factory skill ZIP."""
import argparse
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FOLDER = "software-factory"
STAMP = (2026, 10, 9, 0, 0, 0)

def source_files(root=ROOT):
    sources = [("SKILL.md", root / ".agents/skills/software-factory/SKILL.md"),
               ("AGENTS.md", root / "AGENTS.md")]
    for directory in ("references", "templates", "scripts"):
        for file in sorted((root / directory).iterdir()):
            if file.is_file() and file.suffix in {".md", ".json", ".py", ".txt"}:
                sources.append((directory + "/" + file.name, file))
    return sources

def build(output: Path, root=ROOT):
    sources = source_files(root)
    names = set()
    for name, file in sources:
        if not file.is_file() or file.is_symlink() or not file.resolve().is_relative_to(root.resolve()):
            raise ValueError("Missing, unsafe or escaped asset: " + name)
        if name in names:
            raise ValueError("Duplicate asset: " + name)
        names.add(name)
    mandatory = {"SKILL.md", "references/operating-protocol.md",
                 "references/screen-design.md", "scripts/claims.py",
                 "templates/PROJECT-CHARTER.md"}
    if not mandatory.issubset(names):
        raise ValueError("Required skill assets missing")
    skill = (root / ".agents/skills/software-factory/SKILL.md").read_text(encoding="utf-8")
    if not re.search(r"(?m)^name: software-factory$", skill) or not re.search(r"(?m)^description: Use when", skill):
        raise ValueError("Invalid skill name or activation description")
    skill = skill.replace(
        "Reference paths are relative to this repository root, not the skill directory. Locate the project root before reading them.",
        "References and scripts are relative to this SKILL.md directory. Project docs belong in the target repository."
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, file in sorted(sources):
            info = zipfile.ZipInfo(FOLDER + "/" + name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            content = skill.encode("utf-8") if name == "SKILL.md" else file.read_bytes()
            archive.writestr(info, content, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return len(sources)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist/software-factory-skill.zip")
    args = parser.parse_args()
    count = build(args.output.resolve())
    print(f"Packaged {count} files into {args.output.resolve()}; installation NOT performed")

if __name__ == "__main__":
    main()
