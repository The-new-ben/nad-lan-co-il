"""Local-only Dune exploration. Private source data stays outside the Git worktree.
Usage: python cyprus/local/serve.py --register <private units-source-register.json>
No writes, contact endpoint, credentials, external APIs or production integration.
"""
import argparse, json, mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
ALLOWED = {'/':'index.html','/index.html':'index.html','/app.js':'app.js','/style.css':'style.css','/plan-data.js':'plan-data.js'}
MEDIA = {'/media/a-ground.png':'a-ground.png','/media/a-upper.png':'a-upper.png',
    '/media/site.png':'b-plan-1.png','/media/b-ground.png':'b-plan-2.png',
    '/media/b-upper.png':'b-upper.png','/media/architect-exterior.jpg':'architect-exterior.jpg'}

def project_packet(path):
    raw=json.loads(path.read_text(encoding='utf-8-sig'))
    units=[]
    for row in raw['units']:
        b=row['brochure']
        # Deliberate allowlist: no contacts, prices, availability, source-file IDs,
        # common-area conflicts, exact coordinates or inferred physical layout.
        units.append({'id':row['brochureId'],'bedrooms':row['bedrooms'],'bathrooms':row['bathrooms'],
            'interior':b['coveredAreaM2'],'terrace':b['coveredTerracesM2'],
            'parking':b['coveredParkingM2'],'totalCovered':b['totalCoveredM2']})
    if len({u['id'] for u in units}) != len(units): raise ValueError('Duplicate source unit IDs')
    for u in units:
        if u['interior']+u['terrace']+u['parking'] != u['totalCovered']:
            raise ValueError('Source area sum mismatch')
    return {'name':raw['project']['brochureName'],'district':raw['project']['district'],
        'units':units,'contactEnabled':False,'languages':['he','en'],
        'geometryMode':'none','availabilityMode':'not-offered'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--register',type=Path,required=True);ap.add_argument('--port',type=int,default=47918)
    ap.add_argument('--media-dir',type=Path,help='Private local folder of reviewed public reference images. Never served as a directory.')
    args=ap.parse_args();packet=project_packet(args.register)
    media_dir=(args.media_dir or args.register.parent/'public-reference-media').resolve()
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path=urlsplit(self.path).path
            if path=='/api/project': data=json.dumps(packet,ensure_ascii=False).encode();mime='application/json'
            elif path in ALLOWED:
                f=ROOT/ALLOWED[path];data=f.read_bytes();mime={'.html':'text/html','.js':'text/javascript','.css':'text/css'}[f.suffix]
            elif path in MEDIA:
                f=media_dir/MEDIA[path]
                if not f.is_file(): self.send_error(404);return
                data=f.read_bytes();mime=mimetypes.guess_type(f.name)[0] or 'application/octet-stream'
            else: self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',mime+('; charset=utf-8' if mime.startswith(('text/','application/json')) else ''))
            self.send_header('Cache-Control','no-store');self.send_header('X-Robots-Tag','noindex, nofollow')
            self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(data)
        def log_message(self,*_): pass
    print(f'Local preview: http://127.0.0.1:{args.port}/ | {len(packet["units"])} source records | contact OFF',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
if __name__=='__main__': main()
