"""Restore only the page block from this pilot's exact saved pre-deployment page."""
from pathlib import Path
import argparse,hashlib,importlib.util,json

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--go',action='store_true');args=parser.parse_args()
receipt=json.loads((ROOT/'evidence/public-deployment/latest.json').read_text(encoding='utf-8'))
backup=Path(receipt['backup']).resolve()
assert backup.parent==(ROOT/'evidence/public-deployment').resolve()
prior=backup.read_text(encoding='utf-8')
assert hashlib.sha256(prior.encode()).hexdigest()==receipt['pageBeforeSHA256']
spec=importlib.util.spec_from_file_location('scoped_relay_deploy',ROOT/'public-relay/deploy_relay.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
request=module.load_request()
status,page,_=request('GET','/wp-json/wp/v2/pages/5154?context=edit&_fields=id,content,link')
assert status==200 and page['id']==5154 and page['link']==receipt['url']
current=page['content']['raw']
assert hashlib.sha256(current.encode()).hexdigest()==receipt['pageAfterSHA256'],'Page changed after this pilot; review before restoring.'
print(json.dumps({'dryRun':not args.go,'page':5154,'restoresExactBackup':True,'otherPages':False}))
if args.go:
    status,_,_=request('POST','/wp-json/wp/v2/pages/5154',{'content':prior});assert status==200
    status,verified,_=request('GET','/wp-json/wp/v2/pages/5154?context=edit&_fields=content')
    assert status==200 and verified['content']['raw']==prior
    (ROOT/'evidence/public-deployment/rollback.json').write_text(json.dumps({'page':5154,'restored':True,'readbackExact':True},indent=2),encoding='utf-8')
    print(json.dumps({'page':5154,'restored':True,'readbackExact':True}))
