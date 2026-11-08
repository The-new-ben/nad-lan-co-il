"""Isolated official portable runtime and device query; never loads a model."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'.runtime/llama-vulkan-b12189'
URL = 'https://github.com/ggml-org/llama.cpp/releases/download/b12189/llama-b12189-bin-win-vulkan-x64.zip'
SHA = '9d56405579492423833cdde94cf46cae15d38333f585f3957cafebfc6fb0e182'
BYTES = 37706485
OUT.mkdir(exist_ok=True)
archive = OUT/'release.zip'
# Release metadata fixes a38MB archive. Reserve200MB for extraction plus2GiB untouched.
if shutil.disk_usage(OUT).free < 2*2**30 + 200*2**20:
    raise RuntimeError('Insufficient disk reserve for this portable runtime.')
if not archive.exists():
    h = hashlib.sha256()
    with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent':'NadLan-local-avatar-research'}), timeout=60) as r, archive.with_suffix('.part').open('wb') as f:
        for data in iter(lambda:r.read(1024*1024), b''):
            h.update(data)
            f.write(data)
    if archive.with_suffix('.part').stat().st_size != BYTES or h.hexdigest() != SHA:
        raise RuntimeError('Release does not match the official pinned metadata.')
    archive.with_suffix('.part').replace(archive)
if archive.stat().st_size != BYTES or hashlib.sha256(archive.read_bytes()).hexdigest() != SHA:
    raise RuntimeError('Existing archive hash mismatch.')
with zipfile.ZipFile(archive) as z:
    if sum(x.file_size for x in z.infolist()) > 200*2**20:
        raise RuntimeError('Unexpected extraction size.')
    for item in z.infolist():
        if not (OUT/item.filename).resolve().is_relative_to(OUT.resolve()):
            raise RuntimeError('Unsafe archive path.')
    z.extractall(OUT)
cli = next(OUT.rglob('llama-completion.exe'))
r = subprocess.run([str(cli), '--list-devices'], capture_output=True, text=True, timeout=20, creationflags=0x08000000)
receipt = {'url':URL, 'release':'b12189', 'sha256':SHA, 'bytes':BYTES, 'cli':str(cli),
           'queryExit':r.returncode, 'deviceQuery':(r.stdout+r.stderr)[-5000:], 'modelLoaded':False,
           'installedGlobally':False, 'paidService':False, 'remainingDiskGiB':shutil.disk_usage(OUT).free/2**30}
(ROOT/'research/primary/vulkan-candidate.json').write_text(json.dumps(receipt, indent=2), encoding='utf8')
print(json.dumps(receipt))
