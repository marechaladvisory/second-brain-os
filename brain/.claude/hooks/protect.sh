#!/bin/bash
# PreToolUse hook (Edit|Write). Exit 2 blocks the call and shows stderr to the agent.
# raw/ and archive/ are always read-only; context/, AGENTS.md, CLAUDE.md and .claude/ are read-only in automated runs
# (what every session loads first must not be rewritten from mail or Drive content without the user)
# (env BRAIN_AUTOMATED=1, or marker file .claude/automated-run created by brain-daily/brain-lint).
INPUT=$(cat)
if command -v jq >/dev/null 2>&1; then
  FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')
else
  FILE=$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))')
fi
AUTO="$BRAIN_AUTOMATED"
[ -f "${CLAUDE_PROJECT_DIR:-.}/.claude/automated-run" ] && AUTO=1
case "$FILE" in
  */raw/*|*/archive/*)
    echo "raw/ and archive/ are read-only. Write to the compiled note instead." >&2; exit 2 ;;
  */context/*|*/AGENTS.md|*/CLAUDE.md|*/.claude/*)
    if [ "$AUTO" = "1" ]; then
      echo "context/, AGENTS.md, CLAUDE.md and .claude/ are human-owned during automated runs. Propose the change in your report instead. (No routine running? delete .claude/automated-run.)" >&2; exit 2
    fi ;;
esac
exit 0
