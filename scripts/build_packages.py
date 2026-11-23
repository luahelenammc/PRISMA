"""Build reproducible, self-contained PRISMA method and skill distributions."""
import argparse, hashlib, io, json, pathlib, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'releases'
FIXED=(2026,11,23,0,0,0)
def sha(b): return hashlib.sha256(b).hexdigest()
def zip_bytes(members):
    bio=io.BytesIO()
    with zipfile.ZipFile(bio,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,b in sorted(members.items()):
            zi=zipfile.ZipInfo(name,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=0o100644<<16
            z.writestr(zi,b,compresslevel=9)
    return bio.getvalue()
def build():
    roots=['README.md','README.pt-BR.md','PRISMA.md','ARCHITECTURE.md','ADAPTER_CONTRACT.md','PUBLIC_BOUNDARY.md','LICENSING.md','CHANGELOG.md']
    paths=[ROOT/x for x in roots]+[p for d in ['docs','examples','LICENSES'] for p in (ROOT/d).rglob('*') if p.is_file()]
    method={p.relative_to(ROOT).as_posix():p.read_bytes() for p in paths}
    manifest={'version':'0.1.0-rc.1','files':{k:sha(v) for k,v in sorted(method.items())}}
    method['MANIFEST.json']=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
    skill={'prisma/SKILL.md':(ROOT/'skills/prisma/SKILL.md').read_bytes()}
    skill.update({'prisma/references/'+k:v for k,v in method.items()})
    output={'prisma-method.zip':zip_bytes(method),'prisma-skill.zip':zip_bytes(skill)}
    output['SHA256SUMS'] = ''.join(f'{sha(v)}  {k}\n' for k,v in sorted(output.items())).encode()
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); args=p.parse_args(); OUT.mkdir(exist_ok=True)
    for k,v in build().items():
        dst=OUT/k
        if args.check:
            if not dst.is_file() or dst.read_bytes()!=v: raise SystemExit(f'FAIL {k}')
            print(f'PASS {k} {sha(v)}')
        else: dst.write_bytes(v); print(f'BUILD {k} {sha(v)}')
