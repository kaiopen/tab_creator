from pathlib import Path

from utils import read_seq


seq = read_seq()

dir_pcd = Path.cwd().joinpath('data', 'raw', 'pcd', seq)

dst = Path.cwd().joinpath('data', 'raw', seq + '.txt')

fs = []
for f in dir_pcd.glob('*.pcd'):
    fs.append(f)
fs.sort()

ids = []
for i in range(0, len(fs), 2):
    f = fs[i]
    ids.append(f.stem)

dst.write_text('\n'.join(ids))
