import struct, sys, os, zlib, glob

def extract(path, out):
    d = open(path, 'rb').read()
    if d[:4] != b'PCKF':
        print(f'SKIP {path}: not a PCKF archive'); return
    _, count = struct.unpack_from('<II', d, 0x80)
    p, ok, bad = 0x88, 0, 0
    for _ in range(count):
        stored, real, off, nlen, comp = struct.unpack_from('<5I', d, p); p += 20
        name = d[p:p+nlen].decode('utf-8', 'replace'); p += nlen
        blob = d[off:off+stored]
        if comp:
            try: blob = zlib.decompress(blob)
            except zlib.error:
                try: blob = zlib.decompress(blob, -15)
                except zlib.error: bad += 1; print('FAIL', name); continue
        if len(blob) != real:
            bad += 1; print('size mismatch', name, len(blob), real)
        dest = os.path.join(out, *name.split('/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(blob); ok += 1
    print(f'{path}: {ok}/{count} extracted to {out}, {bad} problems')

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        here = os.path.dirname(os.path.abspath(__file__))
        pcks = glob.glob(os.path.join(here, '*.pck')) + glob.glob(os.path.join(here, '*.PCK'))
        if not pcks:
            print('No .pck files found next to this script.\nUsage: python pckf_extract.py file.pck [outdir]')
        for f in sorted(set(pcks)):
            extract(f, os.path.splitext(f)[0])
    else:
        src = args[0]
        extract(src, args[1] if len(args) > 1 else os.path.splitext(src)[0])
    if os.name == 'nt' and len(sys.argv) == 1 or (os.name == 'nt' and len(sys.argv) == 2):
        input('Done. Press Enter to close...') if sys.stdin and sys.stdin.isatty() else None
