# JSON Toolkit 🧰

A small, dependency-free Python CLI for working with JSON during API troubleshooting and development.

Validate JSON, pretty-print it, minify it, inspect its structure, or pull a nested value with a dot path.

## Commands

```bash
python3 json_toolkit.py validate sample.json
python3 json_toolkit.py pretty sample.json
python3 json_toolkit.py minify sample.json
python3 json_toolkit.py get sample.json user.profile.email
python3 json_toolkit.py get sample.json services.0.latency_ms
python3 json_toolkit.py stats sample.json
```

## Pipe JSON from stdin

Use `-` instead of a filename:

```bash
echo '{"status":"ok","code":200}' | python3 json_toolkit.py pretty -
```

```bash
echo '{"user":{"id":42}}' | python3 json_toolkit.py get - user.id
```

## Invalid JSON

Instead of a Python traceback, JSON Toolkit reports where parsing failed:

```text
INVALID JSON: line 4, column 2: Expecting ',' delimiter
```

## Stats

The `stats` command gives a quick structural overview:

```text
JSON STATS
────────────────────────────────
Root type   dict
Objects     6
Arrays      2
Keys        15
Values      10
Max depth   4
```

## Features

- JSON validation with useful parse errors
- Pretty printing
- Compact/minified output
- Nested object lookup with dot paths
- Array indexing such as `users.0.name`
- Structural statistics
- stdin/pipe support
- Unicode-safe output
- No third-party dependencies

## Tests

```bash
python3 -m unittest -v
```

## Why this exists

JSON is everywhere in API requests, responses, webhooks, configuration, and support cases. This utility keeps the most common inspection tasks in one small command-line tool.

## Roadmap

- Set or delete a value by path
- Search keys recursively
- Compare two JSON files
- Sort object keys
- Flatten nested JSON
- Output selected values as CSV

## License

MIT
