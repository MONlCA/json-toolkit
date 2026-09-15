#!/usr/bin/env python3
"""JSON Toolkit: validate, format, inspect, and query JSON from the terminal."""

import argparse
import json
import sys
from pathlib import Path


def load_json(source):
    if source == "-":
        text = sys.stdin.read()
    else:
        text = Path(source).read_text(encoding="utf-8")
    return json.loads(text)


def get_path(data, path):
    current = data
    if not path:
        return current

    for part in path.split("."):
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                raise KeyError(f"invalid list index: {part}") from None
        elif isinstance(current, dict):
            if part not in current:
                raise KeyError(f"key not found: {part}")
            current = current[part]
        else:
            raise KeyError(f"cannot traverse into: {part}")
    return current


def collect_stats(value, depth=0):
    stats = {"objects": 0, "arrays": 0, "keys": 0, "values": 0, "max_depth": depth}

    def walk(item, level):
        stats["max_depth"] = max(stats["max_depth"], level)
        if isinstance(item, dict):
            stats["objects"] += 1
            stats["keys"] += len(item)
            for child in item.values():
                walk(child, level + 1)
        elif isinstance(item, list):
            stats["arrays"] += 1
            for child in item:
                walk(child, level + 1)
        else:
            stats["values"] += 1

    walk(value, depth)
    return stats


def print_value(value):
    if isinstance(value, (dict, list)):
        print(json.dumps(value, indent=2, ensure_ascii=False))
    elif value is None:
        print("null")
    elif isinstance(value, bool):
        print(str(value).lower())
    else:
        print(value)


def main():
    parser = argparse.ArgumentParser(description="Validate, format, inspect, and query JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("validate", "pretty", "minify", "stats"):
        sub = subparsers.add_parser(command)
        sub.add_argument("source", help="JSON file path, or - for stdin")

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("source", help="JSON file path, or - for stdin")
    get_parser.add_argument("path", help="dot path such as user.profile.email or users.0.name")

    args = parser.parse_args()

    try:
        data = load_json(args.source)
    except FileNotFoundError:
        parser.error(f"file not found: {args.source}")
    except OSError as exc:
        parser.error(str(exc))
    except json.JSONDecodeError as exc:
        print(f"INVALID JSON: line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        raise SystemExit(1)

    if args.command == "validate":
        print("VALID JSON")
    elif args.command == "pretty":
        print(json.dumps(data, indent=2, ensure_ascii=False))
    elif args.command == "minify":
        print(json.dumps(data, separators=(",", ":"), ensure_ascii=False))
    elif args.command == "get":
        try:
            print_value(get_path(data, args.path))
        except KeyError as exc:
            print(f"PATH ERROR: {exc.args[0]}", file=sys.stderr)
            raise SystemExit(1)
    elif args.command == "stats":
        stats = collect_stats(data)
        print("JSON STATS")
        print("─" * 32)
        print(f"Root type   {type(data).__name__}")
        print(f"Objects     {stats['objects']}")
        print(f"Arrays      {stats['arrays']}")
        print(f"Keys        {stats['keys']}")
        print(f"Values      {stats['values']}")
        print(f"Max depth   {stats['max_depth']}")


if __name__ == "__main__":
    main()
