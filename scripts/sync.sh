#!/usr/bin/env bash
# sync.sh — every agent runs this BEFORE any work. 5 seconds. Prints ground truth.
# No-op if anything fails (read-only), so it cannot break a session.

set -u

cd "$(dirname "$0")/.." 2>/dev/null || exit 0

echo "════ NadLan agent sync · $(date -u '+%Y-%m-%d %H:%M UTC') ════"

# 1. git ground truth
git fetch -q origin main 2>/dev/null || true
MAIN_SHA=$(git rev-parse --short origin/main 2>/dev/null || echo "unknown")
MAIN_VER=$(git show origin/main:plugins/nadlan-config/nadlan-config.php 2>/dev/null | grep -m1 -oE 'Version: [0-9.]+' || echo "Version: unknown")
echo "  main HEAD          : $MAIN_SHA"
echo "  plugin version (git): $MAIN_VER"

# 2. live ground truth (best-effort, never fail)
LIVE=$(curl -s --max-time 6 https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck 2>/dev/null \
  | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('version','?'))" 2>/dev/null || echo "?")
echo "  live plugin version: $LIVE"
if [ -n "$LIVE" ] && [ "$LIVE" != "?" ]; then
  GIT_V=$(echo "$MAIN_VER" | grep -oE '[0-9.]+' | head -1)
  if [ "$GIT_V" = "$LIVE" ]; then
    echo "  in-sync            : YES ✓"
  else
    echo "  in-sync            : NO — main=$GIT_V live=$LIVE — next action is DEPLOY, not new code"
  fi
fi

# 3. local working state
LOCAL_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)
DIRTY=$(git status --short 2>/dev/null | wc -l)
echo "  local branch       : $LOCAL_BRANCH"
echo "  local uncommitted  : $DIRTY file(s)"

# 4. point to STATE.md for the rest
echo ""
echo "  → Read STATE.md for the full picture. Read it BEFORE coding."
echo "  → Read skills/MASTER-SKILL.md for the index of all rules."
echo ""
echo "  pre-push hook installed? (verify ZIP/version/language before push):"
HOOKS_PATH=$(git config core.hooksPath 2>/dev/null || echo "")
if [ "$HOOKS_PATH" = ".githooks" ]; then
  echo "    ✓ yes — pushes are auto-verified"
else
  echo "    ✗ NO — run once: git config core.hooksPath .githooks"
fi
echo "════════════════════════════════════════════════════════"
