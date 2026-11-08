"""Build the validated portable knowledge allowlist locally; never export to a repo.

The default command validates and reports a plan. --build writes only the fixed
project-local ZIP and its receipt. No provider, browser, model or network calls.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
SKILL = PROJECT/'skill'
PACKAGE = PROJECT/'talking-avatar-studio-portable.zip'
RECEIPT = ROOT/'evidence/shared-skill-package.json'

# Fixed relative filenames, not a directory walk or caller-controlled export path.
SKILL_FILES = (
    'SKILL.md', 'references/domain-adaptation.md',
    'references/evidence-map.md', 'references/operations.md',
)
PROJECT_FILES = (
    'README.md', 'prototype-3d/PUBLIC-PILOT.md',
    'prototype-3d/PROOF-OF-WORK.md', 'prototype-3d/BACKEND.md',
    'prototype-3d/RUNTIME.md', 'prototype-3d/STREAMING.md',
    'prototype-3d/VISUAL-ROUNDS.md',
    'prototype-3d/research/current-avatar-review.md',
    'prototype-3d/research/latency-integration-round.md',
    'prototype-3d/evidence/skill-forward-test.md',
    'prototype-3d/evidence/public-relay/live-browser/receipt.json',
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def prepare():
    manifest = json.loads((SKILL/'manifest.json').read_text(encoding='utf-8'))
    validation = json.loads((SKILL/'validation.json').read_text(encoding='utf-8'))
    if not validation.get('allStaticChecksPassed') or validation.get('packageVersion') != manifest['version']:
        raise RuntimeError('Validate the current package version before archiving.')
    expected = {Path(item['path']).resolve(): item['sha256'] for item in manifest['packageFiles']}
    if set(expected) != {(SKILL/name).resolve() for name in SKILL_FILES}:
        raise RuntimeError('Manifest package files differ from the reviewed fixed allowlist.')
    entries = []
    for name in SKILL_FILES:
        path = SKILL/name
        if sha(path.read_bytes()) != expected[path.resolve()]:
            raise RuntimeError('Refresh validated source hash before archiving: '+name)
        entries.append((path, 'talking-agent/skill/'+name))
    for name in ('manifest.json', 'validation.json'):
        entries.append((SKILL/name, 'talking-agent/skill/'+name))
    for name in PROJECT_FILES:
        entries.append((PROJECT/name, 'talking-agent/'+name))
    for path, _ in entries:
        if not path.resolve().is_relative_to(PROJECT.resolve()) or not path.is_file():
            raise RuntimeError('Missing or out-of-project allowlisted file: '+str(path))
    # Operational facts live in the included dated handoff, not a second mutable
    # synopsis that can silently lag behind an active public-response test.
    start = f'''# Portable Talking Avatar Studio

Package version: {manifest['version']}. Read talking-agent/skill/SKILL.md and the relevant references, then talking-agent/prototype-3d/PUBLIC-PILOT.md for the current dated deployment and response evidence. Earlier sections and receipts are historical; they do not prove today's readiness.

The approved NadLan public scope is only WordPress page 5154. Other projects need their own role, brand, facts and authorization. Sample approval, a local response, public transport, and verified browser playback are separate milestones. Do not turn one into another or claim physical-phone testing from Chrome viewport emulation. This package makes no world-best, automatic-memory, publishing or spending claim.

Paths outside this archive intentionally refer to Ben's computer. Tool/key registries, credentials, model runtime, private user recordings and unrelated files are excluded. Request only the needed sanitized evidence when a linked result is unavailable. The receiving agent must actually read the files; no provider account was contacted or updated by creating them.

This builder writes only the local portable archive and its receipt. It performs no repository/worktree copy, export, commit, upload or deployment. Root owns any separately authorized export.
'''
    return manifest, entries, start


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true', help='Write the validated local allowlist archive and receipt.')
    args = parser.parse_args()
    manifest, entries, start = prepare()
    plan = {'version': manifest['version'], 'file': str(PACKAGE), 'entries':len(entries)+1,
            'entryNames':['START-HERE.md']+[name for _, name in entries],
            'worktreeExportPerformed':False, 'providerDeliveryPerformed':False,
            'privateRuntimeOrCredentialsIncluded':False}
    if not args.build:
        print(json.dumps({'dryPlan':True, **plan}, indent=2)); return
    # Buffer exactly the allowlisted snapshot before writing.
    payloads = [('START-HERE.md', start.encode('utf-8'))]
    payloads.extend((name, path.read_bytes()) for path, name in entries)
    temporary = PACKAGE.with_suffix('.zip.tmp')
    try:
        with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for name, data in payloads:
                archive.writestr(name, data)
        with zipfile.ZipFile(temporary) as archive:
            if archive.testzip() is not None or set(archive.namelist()) != {name for name, _ in payloads}:
                raise RuntimeError('Portable archive integrity check failed.')
            for name, data in payloads:
                if sha(archive.read(name)) != sha(data):
                    raise RuntimeError('Portable entry hash mismatch: '+name)
        temporary.replace(PACKAGE)
    finally:
        if temporary.exists():
            temporary.unlink()
    receipt = {**plan, 'createdAtUTC':datetime.now(timezone.utc).isoformat(),
               'bytes':PACKAGE.stat().st_size, 'sha256':sha(PACKAGE.read_bytes()),
               'archiveIntegrityPassed':True, 'entryHashesMatchSource':True,
               'independentForwardTestRerun':False,
               'allowlistScope':'Fixed 18-entry portable knowledge allowlist; no directory walk or automatic repository copy.'}
    RECEIPT.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
