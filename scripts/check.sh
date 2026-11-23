#!/bin/sh
# Check the plugin end to end, without touching your own Claude Code or Codex setup.
#
#   scripts/check.sh            structure + every install path that is available here
#   scripts/check.sh --links    also check every https link in the README and skills
#
# What it runs:
#   1. scripts/validate.py: the Claude Code and Codex file formats (offline).
#   2. claude plugin validate, plus a marketplace add and install in a throwaway
#      Claude Code config (if `claude` is installed).
#   3. A marketplace add and install in a throwaway Codex home, then
#      `codex debug prompt-input` to confirm each skill reaches the model's prompt.
#      No Codex sign-in or token is needed (if `codex` is installed).
#   4. `npx skills add --list` to confirm skills.sh finds each skill (if `npx` is installed).
# Steps whose tool is missing are reported as SKIP, not as passed.
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d "${TMPDIR:-/tmp}/catalex-plugins-check.XXXXXX")
trap 'rm -rf "$TMP"' EXIT
FAIL=0
pass() { printf 'PASS  %s\n' "$1"; }
fail() { printf 'FAIL  %s\n' "$1"; FAIL=1; }
skip() { printf 'SKIP  %s\n' "$1"; }

SKILLS=$(cd "$ROOT/plugins/catalex/skills" && ls)

# 1. Formats
if python3 -I "$ROOT/scripts/validate.py" "$@" >"$TMP/validate.log" 2>&1; then
  pass "file formats ($(tail -1 "$TMP/validate.log"))"
else
  cat "$TMP/validate.log"; fail "file formats"
fi

# 2. Claude Code
if command -v claude >/dev/null 2>&1; then
  if claude plugin validate "$ROOT" >"$TMP/c1.log" 2>&1 && claude plugin validate "$ROOT/plugins/catalex" >>"$TMP/c1.log" 2>&1; then
    pass "claude plugin validate (catalog and plugin)"
  else
    cat "$TMP/c1.log"; fail "claude plugin validate"
  fi
  mkdir -p "$TMP/claude"
  if CLAUDE_CONFIG_DIR="$TMP/claude" claude plugin marketplace add "$ROOT" >"$TMP/c2.log" 2>&1 \
    && CLAUDE_CONFIG_DIR="$TMP/claude" claude plugin install catalex@catalex >>"$TMP/c2.log" 2>&1 \
    && CLAUDE_CONFIG_DIR="$TMP/claude" claude plugin list 2>&1 | grep -q 'catalex@catalex'; then
    pass "Claude Code installs catalex@catalex"
  else
    cat "$TMP/c2.log"; fail "Claude Code install"
  fi
else
  skip "Claude Code (claude not installed)"
fi

# 3. Codex
if command -v codex >/dev/null 2>&1; then
  export CODEX_HOME="$TMP/codex"; mkdir -p "$CODEX_HOME" "$TMP/agent"
  if codex plugin marketplace add "$ROOT" >"$TMP/x1.log" 2>&1 \
    && codex plugin add catalex@catalex >>"$TMP/x1.log" 2>&1; then
    pass "Codex installs catalex@catalex ($(codex --version 2>/dev/null))"
    (cd "$TMP/agent" && codex debug prompt-input "hello" >"$TMP/prompt.json" 2>"$TMP/x2.log")
    for s in $SKILLS; do
      # Codex lists plugin skills as "- catalex:<skill>: <description> (file: .../SKILL.md)"
      if grep -q -- "- catalex:$s: " "$TMP/prompt.json"; then
        pass "Codex shows skill $s to the model"
      else
        cat "$TMP/x2.log"; fail "Codex does not show skill $s to the model"
      fi
    done
  else
    cat "$TMP/x1.log"; fail "Codex install"
  fi
  unset CODEX_HOME
else
  skip "Codex (codex not installed)"
fi

# 4. skills.sh
if command -v npx >/dev/null 2>&1; then
  (cd "$TMP" && npx -y skills add "$ROOT" --list >"$TMP/s.log" 2>&1)
  for s in $SKILLS; do
    if grep -q "$s" "$TMP/s.log"; then pass "skills.sh finds $s"; else cat "$TMP/s.log"; fail "skills.sh does not find $s"; fi
  done
else
  skip "skills.sh (npx not installed)"
fi

[ "$FAIL" -eq 0 ] && echo "All checks passed." || echo "Some checks failed."
exit "$FAIL"
