#!/usr/bin/env python3
"""Synchronize Mongolian translations into mn.json.

This script copies values from the Gemini-translated Mongol.json file into the
React client's mn.json file whenever the translation key exists in both files.
Keys that do not exist in Mongol.json keep their English fallback value.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, Tuple

JsonDict = Dict[str, str]


def resolve_paths(script_path: Path) -> Tuple[Path, Path, Path]:
    """Return default paths for source, target, and reference files."""

    repo_root = script_path.resolve().parent.parent
    source_default = repo_root.parent / "Mongol.json"
    target_default = repo_root / "frontend" / "src" / "languages" / "mn.json"
    reference_default = repo_root / "frontend" / "src" / "languages" / "en.json"
    return source_default, target_default, reference_default


def load_json(path: Path) -> JsonDict:
    """Load JSON data from *path* and exit with a readable message on failure."""

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        sys.exit(f"[ERROR] File not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(
            "[ERROR] Failed to parse JSON from {path}: line {line}, column {col}".format(
                path=path, line=exc.lineno, col=exc.colno
            )
        )
    if not isinstance(data, dict):
        sys.exit(f"[ERROR] Expected an object at the top level of {path}.")
    return data  # type: ignore[return-value]


def write_json(path: Path, payload: JsonDict) -> None:
    """Write JSON data to *path* using UTF-8 without escaping non-ASCII."""

    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def sync_translations(source: JsonDict, reference: JsonDict) -> Tuple[JsonDict, int, int]:
    """Return a new mn.json mapping plus stats for replaced and fallback keys."""

    replaced = 0
    fallback = 0
    merged: JsonDict = {}

    for key, value in reference.items():
        if key in source:
            merged[key] = source[key]
            replaced += 1
        else:
            merged[key] = value
            fallback += 1
    return merged, replaced, fallback


def main() -> int:
    script_path = Path(__file__)
    default_source, default_target, default_reference = resolve_paths(script_path)

    parser = argparse.ArgumentParser(
        description=(
            "Copy translations from Mongol.json into mn.json for keys that exist in "
            "both files."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=default_source,
        help=f"Path to Mongol.json (default: {default_source})",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=default_target,
        help=f"Path to mn.json (default: {default_target})",
    )
    parser.add_argument(
        "--reference",
        type=Path,
        default=default_reference,
        help="Reference English JSON containing the canonical key order.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned changes without writing mn.json.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create a *.bak copy of the current mn.json before writing.",
    )
    args = parser.parse_args()

    source = load_json(args.source)
    reference = load_json(args.reference)
    target_before = load_json(args.target)

    merged, replaced, fallback = sync_translations(source, reference)

    source_only = sorted(set(source.keys()) - set(reference.keys()))
    missing_in_source = sorted(set(reference.keys()) - set(source.keys()))

    print("===== Translation Sync Summary =====")
    print(f"Source file:    {args.source} ({len(source)} keys)")
    print(f"Reference file: {args.reference} ({len(reference)} keys)")
    print(f"Target file:    {args.target} ({len(target_before)} keys)")
    print(f"Keys replaced with Mongolian text: {replaced}")
    print(f"Keys keeping English fallback:    {fallback}")
    if missing_in_source:
        print(f"Keys missing in Mongol.json:     {len(missing_in_source)}")
    if source_only:
        print(f"Extra keys ignored from source:   {len(source_only)}")

    if args.dry_run:
        print("Dry-run mode enabled; no files were written.")
        return 0

    if not args.no_backup:
        backup_path = args.target.with_suffix(args.target.suffix + ".bak")
        shutil.copyfile(args.target, backup_path)
        print(f"Backup written to {backup_path}")

    write_json(args.target, merged)
    print(f"Updated translations written to {args.target}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
