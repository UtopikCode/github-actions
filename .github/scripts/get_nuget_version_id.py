#!/usr/bin/env python3
import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find GitHub NuGet package version id from API response"
    )
    parser.add_argument("version", help="Package version to locate")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 1

    items = data if isinstance(data, list) else []
    for item in items:
        if item.get("name") == args.version:
            print(item.get("id") or "")
            return 0

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
