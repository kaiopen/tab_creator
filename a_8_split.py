import json
from pathlib import Path

import numpy as np


TRAINVAL = (
    '2021-10-18-15-50-29-00',  # 423
    '2021-10-18-16-41-54-00',  # 93
    '2021-12-08-14-54-07-00',  # 128
    '2021-12-08-15-18-30-01',  # 185
    '2021-12-08-15-18-30-02',  # 152
    '2021-12-08-15-18-30-03',  # 181
    '2021-12-08-15-18-30-04',  # 30
    '2021-12-08-15-18-30-05',  # 98
    '2021-12-08-15-26-27-00',  # 125
    '2021-12-08-15-26-27-01',  # 247
    '2021-12-08-15-26-27-02',  # 75
    '2021-12-08-15-33-15-01',  # 216
    '2021-12-08-15-38-39-00',  # 153
    '2021-12-08-15-46-51-00',  # 274
    '2021-12-08-15-56-32-00',  # 115
    '2021-12-08-15-56-32-01',  # 184
    '2021-12-08-15-56-32-03',  # 184
    '2021-12-08-16-07-46-00',  # 104
    '2021-12-08-16-09-08-00',  # 143
    '2021-12-08-16-09-08-01',  # 131
    '2021-12-08-16-09-08-03',  # 84
    '2021-12-31-15-07-24-00',  # 212
    '2021-12-31-15-10-20-00',  # 80
    '2021-12-31-15-22-19-00',  # 129
    '2021-12-31-15-22-19-01',  # 132
    '2021-12-31-15-57-05-00',  # 84
    '2023-05-11-10-27-24-00',  # 111
    '2023-05-11-10-29-02-00',  # 176
    '2023-05-11-10-32-13-00'   # 169
)
TEST = (
    '2021-12-08-14-56-54-00',  # 53
    '2021-12-08-15-18-30-00',  # 87
    '2021-12-08-15-18-30-06',  # 113
    '2021-12-08-15-33-15-00',  # 589
    '2021-12-08-15-43-04-00',  # 152
    '2021-12-08-15-56-32-02',  # 320
    '2021-12-08-15-56-32-04',  # 63
    '2021-12-08-16-09-08-02',  # 122
    '2021-12-31-15-09-22-00',  # 108
    '2021-12-31-15-24-47-00',  # 110
    '2021-12-31-15-57-05-01',  # 52
    '2023-05-11-10-29-02-01',  # 99
    '2023-05-11-11-10-16-00'   # 64
)

dir_pcd = Path.cwd().joinpath('data', 'TAB', 'pcd')
dir_bound = Path.cwd().joinpath('data', 'TAB', 'bound')
dst = Path.cwd().joinpath('data', 'TAB')

# TRAINVAL
s = {}
for seq in TRAINVAL:
    fs = []
    for f in dir_pcd.joinpath(seq).glob('*.pcd'):
        fs.append(f.stem)
    fs.sort()

    is_existed = False
    exists = []
    count = 0
    ids = []
    for i, f in enumerate(fs):
        if dir_bound.joinpath(seq, f + '.json').exists():
            if is_existed:
                raise Exception(
                    f'{seq}/{f}: two consecutive annotated frames.'
                )
            is_existed = True
            ids.append([f, 'train'])
            exists.append(i)
            count += 1
        else:
            if is_existed:
                is_existed = False
                ids.append((f, None))
            else:
                raise Exception(
                    f'{seq}/{f}: two consecutive unannotated frames.'
                )

    for i in np.random.choice(exists, size=int(count * 0.25), replace=False):
        ids[i][1] = 'val'
    s[seq] = ids
json.dump(s, dst.joinpath('trainval.json').open('w'), indent=2)

# TEST
s = {}
for seq in TEST:
    fs = []
    for f in dir_pcd.joinpath(seq).glob('*.pcd'):
        fs.append(f.stem)
    fs.sort()

    is_existed = False
    ids = []
    for f in fs:
        if dir_bound.joinpath(seq, f + '.json').exists():
            if is_existed:
                raise Exception(
                    f'{seq}/{f}: two consecutive annotated frames.'
                )
            is_existed = True
            ids.append((f, 'test'))
        else:
            if is_existed:
                is_existed = False
                ids.append((f, None))
            else:
                raise Exception(
                    f'{seq}/{f}: two consecutive unannotated frames.'
                )
    s[seq] = ids
json.dump(s, dst.joinpath('test.json').open('w'), indent=2)
