import csv
from pathlib import Path

from tab import TAB

from utils import round

tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

tr = 0
c_tr = 0
for f in tab_train:
    tr += 1
    for bound in tab_train.get_boundaries(f):
        if 'turning' == bound['semantics']:
            c_tr += 1
            break
u_tr = tr - c_tr

v = 0
c_v = 0
for f in tab_val:
    v += 1
    for bound in tab_val.get_boundaries(f):
        if 'turning' == bound['semantics']:
            c_v += 1
            break
u_v = v - c_v

c_tv = c_tr + c_v
u_tv = u_tr + u_v
tv = tr + v

te = 0
c_te = 0
for f in tab_test:
    te += 1
    for bound in tab_test.get_boundaries(f):
        if 'turning' == bound['semantics']:
            c_te += 1
            break
u_te = te - c_te

c_t = c_tv + c_te
u_t = u_tv + u_te
t = tv + te

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('bend.csv').open('w')).writerows(
    (
        ('', '# bend', ' % bend', '# non-bend', '% non-bend', 'total'),
        (
            'TRAIN',
            c_tr, round(c_tr / tr * 100.), u_tr, round(u_tr / tr * 100.), tr
        ),
        (
            'VAL',
            c_v, round(c_v / v * 100.), u_v, round(u_v / v * 100.), v
        ),
        (
            'TRAINVAL',
            c_tv, round(c_tv / tv * 100.), u_tv, round(u_tv / tv * 100.), tv
        ),
        (
            'TEST',
            c_te, round(c_te / te * 100.), u_te, round(u_te / te * 100.), te
        ),
        (
            'TOTAL',
            c_t, round(c_t / t * 100.), u_t, round(u_t / t * 100.), t
        )
    )
)
