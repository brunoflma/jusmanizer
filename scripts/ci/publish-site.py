"""Publish the verified static output, preserving the Pages branch history."""
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def git(*args,data=None):
    return subprocess.check_output(['git',*args],cwd=ROOT,input=data).decode().strip()

def main():
    if os.environ.get('CIRCLECI')!='true' or os.environ.get('CIRCLE_BRANCH')!='main':
        raise SystemExit('Publication requires CircleCI on main')
    revision=os.environ['CIRCLE_SHA1']
    if git('rev-parse','HEAD')!=revision:
        raise SystemExit('Checkout differs from pipeline')
    remote=git('config','--get','remote.origin.url').removesuffix('.git')
    if remote not in ('https://github.com/brunoflma/jusmanizer','git@github.com:brunoflma/jusmanizer'):
        raise SystemExit('Unexpected repository')
    if git('ls-remote','origin','refs/heads/main').split()[0]!=revision:
        raise SystemExit('Main advanced; preserve the newer source')
    output=Path(sys.argv[1]).resolve()
    if not (output/'index.html').is_file() or not (output/'.nojekyll').is_file():
        raise SystemExit('Missing static website output')
    count=0;total=0
    def tree(directory):
        nonlocal count,total
        entries=[]
        for path in sorted(directory.iterdir()):
            if path.is_symlink() or path.name in ('.git','.github') or any(c in path.name for c in '\n\r\t'):
                raise SystemExit('Unsafe website entry')
            if path.is_dir():
                oid=tree(path);mode='040000';kind='tree'
            elif path.is_file():
                count+=1;total+=path.stat().st_size
                if count>5000 or total>100_000_000:raise SystemExit('Website output exceeds limits')
                oid=git('hash-object','-w','--stdin',data=path.read_bytes());mode='100644';kind='blob'
            else:raise SystemExit('Unsupported website entry')
            entries.append(f'{mode} {kind} {oid}\t{path.name}\0'.encode())
        return git('mktree','-z',data=b''.join(entries))
    tree_id=tree(output)
    prior=git('ls-remote','origin','refs/heads/gh-pages').split()
    parent=prior[0] if prior else None
    args=['-c','user.name=CircleCI','-c','user.email=ci@users.noreply.github.com','commit-tree',tree_id]
    if parent:
        subprocess.run(['git','fetch','--no-tags','origin',parent],cwd=ROOT,check=True)
        if git('rev-parse',parent+'^{tree}')==tree_id:
            print('Verified website is already current');return
        args+=['-p',parent]
    commit=git(*args,data=f'Publish website from {revision}\n\nCircleCI: {os.environ["CIRCLE_BUILD_URL"]}\n'.encode())
    subprocess.run(['git','push','origin',commit+':refs/heads/gh-pages'],cwd=ROOT,check=True)
    print(json.dumps({'source':revision,'pages_commit':commit,'files':count,'bytes':total}))

if __name__=='__main__':main()
