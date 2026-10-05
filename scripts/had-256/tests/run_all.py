"""Runs the HAD-256 suites one after the other on the benches (they reset the AFTER site, so never two at once).

    python run_all.py                      # everything
    python run_all.py test_media test_rate # some
Needs: node scripts/had-256/local/start.mjs after  (127.0.0.1:9401)  and  ... before  (127.0.0.1:9411).
"""
import subprocess
import sys
import time

ALL = ['smoke_slice1', 'test_security', 'test_rate', 'test_photos', 'test_media', 'test_privacy_tabs', 'test_journey', 'engine_after', 'test_engine before', 'before_after before', 'before_after after', 'test_layout']

want = sys.argv[1:] or ALL
for name in want:
    parts = name.split()
    t0 = time.time()
    print('=== %s' % name, flush=True)
    r = subprocess.run([sys.executable, '-u', parts[0] + '.py'] + parts[1:], env=dict(__import__('os').environ, PYTHONIOENCODING='utf-8'))
    print('=== %s exit %d in %ds' % (name, r.returncode, time.time() - t0), flush=True)
