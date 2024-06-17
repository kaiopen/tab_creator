r'''

unstructured, lengthened, blind, occluded, distorted, irregular

'''
import csv
from pathlib import Path

from tab import TAB

from utils import round


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

c_tr = 0
tr = 0
for f in tab_train:
    bounds = tab_train.get_boundaries(f)
    tr += len(bounds)

    for bound in bounds:
        if bound['single']:
            c_tr += 1
        else:
            for p in bound['points']:
                if (
                    p['unstructured'] or p['irregular']
                    or p['occluded'] or p['blind']
                    or p['distorted'] or p['lengthened']
                ):
                    c_tr += 1
                    break
u_tr = tr - c_tr

c_v = 0
val = 0
for f in tab_val:
    bounds = tab_val.get_boundaries(f)
    val += len(bounds)

    for bound in bounds:
        if bound['single']:
            c_v += 1
        else:
            for p in bound['points']:
                if (
                    p['unstructured'] or p['irregular']
                    or p['occluded'] or p['blind']
                    or p['distorted'] or p['lengthened']
                ):
                    c_v += 1
                    break
u_v = val - c_v

c_tv = c_tr + c_v
u_tv = u_tr + u_v
tv = tr + val

c_te = 0
te = 0
for f in tab_test:
    bounds = tab_train.get_boundaries(f)
    te += len(bounds)

    for bound in bounds:
        if bound['single']:
            c_te += 1
        else:
            for p in bound['points']:
                if (
                    p['unstructured'] or p['irregular']
                    or p['occluded'] or p['blind']
                    or p['distorted'] or p['lengthened']
                ):
                    c_te += 1
                    break
u_te = te - c_te

c_t = c_tv + c_te
u_t = u_tv + u_te
t = tv + te

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('complex.csv').open('w')).writerows(
    (
        ('', '# clear', '% clear', '# complex', '% complex', '# total'),
        (
            'TRAIN',
            u_tr, round(u_tr / tr * 100.), c_tr, round(c_tr / tr * 100.), tr
        ),
        (
            'VAL',
            u_v, round(u_v / val * 100.), c_v, round(c_v / val * 100.), val
        ),
        (
            'TRAINVAL',
            u_tv, round(u_tv / tv * 100.), c_tv, round(c_tv / tv * 100.), tv
        ),
        (
            'TEST',
            u_te, round(u_te / te * 100.), c_te, round(c_te / te * 100.), te
        ),
        (
            'TOTAL',
            u_t, round(u_t / t * 100.), c_t, round(c_t / t * 100.), t
        )
    )
)
