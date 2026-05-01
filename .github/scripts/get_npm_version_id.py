#!/usr/bin/env python3
import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Find GitHub npm package version id from package metadata")
    parser.add_argument("name", help="Package name")
    parser.add_argument("version", help="Package version")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 1

    if not isinstance(payload, list):
        payload = []

    for item in payload:
        metadata = item.get("metadata", {}) or {}
        pkg_name = metadata.get("package_name") or item.get("name")
        pkg_version = metadata.get("version") or metadata.get("package_version")
        if pkg_name == args.name and pkg_version == args.version:
            print(item.get("id") or "")
            return 0

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
