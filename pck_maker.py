here = os.path.dirname(os.path.abspath(__file__))
name = os.path.basename(here)
out = os.path.join(here, name + '.pck')
skip = {os.path.abspath(__file__), out}

files = []
for root, _, fs in os.walk(here):
    for f in fs:
        full = os.path.abspath(os.path.join(root, f))
        if full in skip: continue
        files.append((os.path.relpath(full, here).replace(os.sep, '/'), full))
files.sort()

datas = [open(full, 'rb').read() for _, full in files]
names = [rel.encode('utf-8') for rel, _ in files]
head = b'PCKF' + name.encode('utf-8')[:123].ljust(124, b'\0') + struct.pack('<II', 0, len(files))
off = len(head) + sum(20 + len(n) for n in names)

directory = bytearray()
for n, d in zip(names, datas):
    directory += struct.pack('<5I', len(d), len(d), off, len(n), 0) + n
    off += len(d)

with open(out, 'wb') as f:
    f.write(head + directory + b''.join(datas))
print(f'{len(files)} files -> {out}')
