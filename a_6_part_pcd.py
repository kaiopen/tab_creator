from typing import Sequence
from pathlib import Path

from kaitorch.pcd import PointCloudWriterXYZIR

from utils import adjust_pcd_, filter_pcd_, load_pcd, read_seq


seq = read_seq()

dir_pcd = Path.cwd().joinpath('data', 'raw', 'pcd', seq)
dir_bev = Path.cwd().joinpath('data', 'raw', 'bev', seq)

dst = Path.cwd().joinpath('data', 'TAB', 'pcd')
dst.mkdir(parents=True, exist_ok=True)

writer = PointCloudWriterXYZIR()


def part(name: str, ids: Sequence[str]):
    print(f'Generate SEQ. {name} ...')

    d = dst.joinpath(name)
    d.mkdir(parents=True, exist_ok=True)

    for id in ids:
        filename = id + '.pcd'
        writer(
            filter_pcd_(adjust_pcd_(load_pcd(dir_pcd.joinpath(filename)))),
            d.joinpath(filename)
        )


pcds = []
for f in dir_pcd.glob('*.pcd'):
    pcds.append(f.stem)
pcds.sort()
num_pcd = len(pcds)

annos = []
for f in dir_bev.glob('*.json'):
    annos.append(f.stem)
annos.sort()
num_anno = len(annos)

i_pcd = 0
i_anno = 0
ids = []
sub = 0
while i_anno < num_anno:
    anno = annos[i_anno]

    if anno == pcds[i_pcd]:
        ids.append(anno)

    else:
        if len(ids) != 0:
            if ids[-1] not in annos:
                ids = ids[:-1]

            part(seq + f'-{sub:02d}', ids)
            sub += 1

        ids = [anno]
        i_pcd = pcds.index(anno, i_pcd)

    i_pcd += 1
    if i_pcd < num_pcd:
        ids.append(pcds[i_pcd])
    i_pcd += 1
    i_anno += 1

if len(ids) != 0:
    part(seq + f'-{sub:02d}', ids)
