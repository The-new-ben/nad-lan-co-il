"""Build an allowlisted public asset package; never copies runtime or credentials."""
from pathlib import Path
import hashlib,json,shutil,subprocess
from PIL import Image

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'public-package'
OUT.mkdir(exist_ok=True)
ESBUILD=ROOT/'.runtime/bundler/node_modules/@esbuild/win32-x64/esbuild.exe'
if not ESBUILD.is_file():raise SystemExit('Pinned local bundler is missing')
for source,target,extras in [
    ('widget-stream.js','widget.js',['--external:./dynamic-lips.js']),
    ('dynamic-lips.js','dynamic-lips.js',[]),
    ('dynamic-lips-worker.js','dynamic-lips-worker.js',[]),
    ('widget.css','widget.css',[])
]:
    subprocess.run([str(ESBUILD),str(ROOT/source),'--bundle','--minify','--format=esm','--legal-comments=eof',f'--outfile={OUT/target}',*extras],check=True,capture_output=True)
files=['widget.js','dynamic-lips.js','dynamic-lips-worker.js','widget.css']
for relative in ['assets/nadlan-advisor-v2.glb','assets/greet-en.mp3','assets/greet-en.cues.json','assets/fallback-original.webp','vendor/talking-avatar/viseme-model.bin','vendor/talking-avatar/LICENSE','vendor/THREE-LICENSE.txt']:
    target=OUT/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,target);files.append(relative)
source_image=Image.open(ROOT/'assets/portrait-cutout-v2.png').convert('RGBA')
portrait=OUT/'assets/portrait-cutout-v2.webp'
source_image.save(portrait,lossless=True,exact=True,method=6)
identical=Image.open(portrait).convert('RGBA').tobytes()==source_image.tobytes()
if not identical:raise SystemExit('Lossless portrait verification failed')
files.append('assets/portrait-cutout-v2.webp')
for name in ['nadlan-small-avatar-phone-final.mp4','nadlan-small-avatar-desktop-final.mp4']:
    relative='review/'+name
    target=OUT/relative;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'evidence/videos'/name,target);files.append(relative)
manifest={'build':'small-head-pilot','bundler':'esbuild 0.25.12','model':'photo-textured frontal 3D, not full volumetric','portraitRGBAUnchanged':identical,'files':[]}
for relative in files:
    data=(OUT/relative).read_bytes()
    manifest['files'].append({'path':relative,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
manifest['totalBytes']=sum(x['bytes'] for x in manifest['files'])
manifest['releaseId']='v-'+hashlib.sha256(json.dumps(manifest['files'],sort_keys=True).encode()).hexdigest()[:12]
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
preview=(ROOT/'site-preview.html').read_text(encoding='utf-8')
preview=preview.replace('href="widget.css"','href="public-package/widget.css"')
preview=preview.replace('<script type="module" src="widget.js"></script>',
    '<script>window.__NL3D='+json.dumps({'fallbackUrl':'/public-package/assets/portrait-cutout-v2.webp','storageKey':'nlag-package-proof'})+';</script><script type="module" src="public-package/widget.js"></script>')
(ROOT/'public-package-preview.html').write_text(preview,encoding='utf-8')
print(json.dumps({'releaseId':manifest['releaseId'],'files':len(files),'bytes':manifest['totalBytes'],'portraitRGBAUnchanged':identical}))
