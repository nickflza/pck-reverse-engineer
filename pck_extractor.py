import struct, sys, os, zlib

def extract(path, out):
    d = open(path, 'rb').read()
    assert d[:4] == b'PCKF', 'not a PCKF archive'
    _, count = struct.unpack_from('<II', d, 0x80)
    p, n_ok, n_bad = 0x88, 0, 0
    for _ in range(count):
        stored, real, off, nlen, comp = struct.unpack_from('<5I', d, p); p += 20
        name = d[p:p+nlen].decode('utf-8', 'replace'); p += nlen
        blob = d[off:off+stored]
        if comp:
            try: blob = zlib.decompress(blob)
            except zlib.error:
                try: blob = zlib.decompress(blob, -15)
                except zlib.error: n_bad += 1; print('FAIL', name); continue
        if len(blob) != real: print('size mismatch', name, len(blob), real); n_bad += 1
        dest = os.path.join(out, *name.split('/'))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'wb').write(blob); n_ok += 1
    print(f'{n_ok}/{count} extracted, {n_bad} problems')

if __name__ == '__main__':
    extract(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'pck_out')
