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

    items = []
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        if isinstance(payload.get("package_versions"), list):
            items = payload["package_versions"]
        elif isinstance(payload.get("data"), list):
            items = payload["data"]
        elif isinstance(payload.get("versions"), list):
            items = payload["versions"]
        else:
            items = []

    def normalize_package_name(package_name: str) -> str:
        if package_name.startswith("@") and "/" in package_name:
            return package_name.split("/", 1)[1]
        return package_name

    normalized_args_name = normalize_package_name(args.name)

    for item in items:
        metadata = item.get("metadata", {}) or {}
        item_pkg_name = metadata.get("package_name") or item.get("package_name")
        item_pkg_version = (
            metadata.get("version")
            or metadata.get("package_version")
            or item.get("version")
            or item.get("package_version")
            or item.get("name")
        )

        version_match = item_pkg_version == args.version
        if item_pkg_name is not None:
            normalized_item_pkg_name = normalize_package_name(str(item_pkg_name))
            name_match = (
                item_pkg_name == args.name
                or normalized_item_pkg_name == normalized_args_name
            )
            if name_match and version_match:
                print(item.get("id") or "")
                return 0
        elif version_match:
            print(item.get("id") or "")
            return 0

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
