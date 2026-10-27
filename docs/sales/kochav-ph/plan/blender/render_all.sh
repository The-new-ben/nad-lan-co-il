#!/bin/sh
# final renders, 2400 px wide, Cycles CPU
B="/c/Program Files/Blender Foundation/Blender 5.2/blender.exe"; PL="C:/Users/777/nad-lan/nad-lan-co-il/docs/sales/kochav-ph/plan"
for v in dollhouse topdown terrace; do
  s=128; [ "$v" = "terrace" ] && s=144
  echo "== $v start $(date +%H:%M:%S)"
  "$B" -b --python "$PL/blender/plan3d.py" -- --view $v --samples $s --scale 100 2>&1 | grep -E "RENDERED|Error|Traceback"
  echo "== $v end $(date +%H:%M:%S)"
done
