#!/bin/bash
# PreToolUse hook (matcher mcp__.*). Exit 2 blocks the call and shows stderr to the agent.
# Mail, Drive and meeting content can carry prompt injection: this hook is the mechanical
# limit on what an injected instruction can make a connector do (contracts §7.8).
# Always blocked: anything that sends, shares, deletes or hides data (send, reply, forward,
#   share, trash, delete, spam, request access, publish, submit).
# Automated runs (env BRAIN_AUTOMATED=1 or marker .claude/automated-run): read-only tools only
#   (search, list, get, read, query, describe, fetch, analyze, ping).
INPUT=$(cat)
if command -v jq >/dev/null 2>&1; then
  TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // empty')
else
  TOOL=$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_name",""))')
fi
case "$TOOL" in mcp__*) ;; *) exit 0 ;; esac
SESSION_TOOL=0; case "$TOOL" in mcp__claude-code-remote__*) SESSION_TOOL=1 ;; esac   # session/scheduling tools: not data connectors
NAME=$(printf '%s' "${TOOL#mcp__*__}" | tr '[:upper:]' '[:lower:]')   # tool name without the server prefix
if [ "$SESSION_TOOL" = 0 ] && printf '%s' "$NAME" | grep -Eq '(^|_)(send|reply|forward|share|trash|untrash|delete|spam|unspam|request_access|publish|submit)(_|$)'; then
  echo "Blocked by the brain's connector guard: $TOOL sends, shares or deletes data. Brain skills never do this; if the user wants it, they do it themselves in the app." >&2
  exit 2
fi
AUTO="$BRAIN_AUTOMATED"
[ -f "${CLAUDE_PROJECT_DIR:-.}/.claude/automated-run" ] && AUTO=1
if [ "$AUTO" = "1" ] && ! printf '%s' "$NAME" | grep -Eq '^(search|list|get|read|query|describe|fetch|analyze|ping)(_|$)'; then
  echo "Blocked by the brain's connector guard: automated runs use read-only connector tools only ($TOOL is not one). Put what you wanted to do in the report." >&2
  exit 2
fi
exit 0
