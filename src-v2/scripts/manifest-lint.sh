#!/usr/bin/env bash
# Manifest lint — the portability check for src-v2/flows/*.md.
# See src-v2/PLAN.md § Verification § Manifest lint (portability claim).
#
# A flow manifest must be readable by a tool that isn't Copilot. This is a
# grep-level check, not a real second-adapter test — it fails the slice if
# the manifest contains syntax that only makes sense to one tool.
#
# Usage: src-v2/scripts/manifest-lint.sh
# Exit code: 0 = pass, 1 = violations found.

set -euo pipefail
cd "$(dirname "$0")/.."  # src-v2/

FAIL=0

echo "== Manifest lint: src-v2/flows/*.md =="

for f in flows/*.md; do
  echo "-- $f"

  # 1. No @-mention invocation syntax (e.g. "@architect", "@backend-engineer")
  #    used as an actual invocation, as opposed to prose *mentioning* the
  #    convention (which is allowed and expected in these docs).
  if grep -nE '(^|[^`])@[a-zA-Z][a-zA-Z0-9_-]*([^`a-zA-Z0-9_-]|$)' "$f" \
      | grep -vE 'no `@|no @agent|without `@`' >/dev/null; then
    echo "   FAIL: possible @-mention invocation syntax:"
    grep -nE '(^|[^`])@[a-zA-Z][a-zA-Z0-9_-]*([^`a-zA-Z0-9_-]|$)' "$f" \
      | grep -vE 'no `@|no @agent|without `@`' | sed 's/^/     /'
    FAIL=1
  fi

  # 2. No tool-specific tool names (Copilot/Claude Code/Cursor internal
  #    tool identifiers leaking into a phase contract).
  if grep -nE 'create_file|replace_string_in_file|str_replace_editor|mcp__' "$f" >/dev/null; then
    echo "   FAIL: tool-specific tool name found:"
    grep -nE 'create_file|replace_string_in_file|str_replace_editor|mcp__' "$f" | sed 's/^/     /'
    FAIL=1
  fi

  echo "   ok"
done

if [ "$FAIL" -ne 0 ]; then
  echo
  echo "Manifest lint FAILED — see violations above."
  exit 1
fi

echo
echo "Manifest lint PASSED — flows/*.md contain no tool-specific syntax found by this check."
