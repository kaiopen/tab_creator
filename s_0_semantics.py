import csv
from pathlib import Path

from tab import TAB

from utils import round


tab_train = TAB('data/TAB', 'train')
tab_val = TAB('data/TAB', 'val')
tab_test = TAB('data/TAB', 'test')

c_tr = 0
s_tr = 0
fc_tr = 0
fs_tr = 0
for f in tab_train:
    for bound in tab_train.get_boundaries(f):
        if 'turning' == bound['semantics']:
            if bound['fuzzy']:
                fc_tr += 1
            else:
                c_tr += 1
        else:
            if bound['fuzzy']:
                fs_tr += 1
            else:
                s_tr += 1
tr = c_tr + s_tr + fc_tr + fs_tr


c_v = 0
s_v = 0
fc_v = 0
fs_v = 0
for f in tab_val:
    for bound in tab_val.get_boundaries(f):
        if 'turning' == bound['semantics']:
            if bound['fuzzy']:
                fc_v += 1
            else:
                c_v += 1
        else:
            if bound['fuzzy']:
                fs_v += 1
            else:
                s_v += 1
v = c_v + s_v + fc_v + fs_v

c_tv = c_tr + c_v
s_tv = s_tr + s_v
fc_tv = fc_tr + fc_v
fs_tv = fs_tr + fs_v
tv = c_tv + s_tv + fc_tv + fs_tv


c_te = 0
s_te = 0
fc_te = 0
fs_te = 0
for f in tab_test:
    for bound in tab_test.get_boundaries(f):
        if 'turning' == bound['semantics']:
            if bound['fuzzy']:
                fc_te += 1
            else:
                c_te += 1
        else:
            if bound['fuzzy']:
                fs_te += 1
            else:
                s_te += 1
te = c_te + s_te + fc_te + fs_te

c_t = c_tv + c_te
s_t = s_tv + s_te
fc_t = fc_tv + fc_te
fs_t = fs_tv + fs_te
t = c_t + s_t + fc_t + fs_t

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('semantics.csv').open('w')).writerows(
    (
        (
            '',
            '# SGS', '% SGS', '# fuzzy SGS', '% fuzzy SGS',
            '# turning', '% turning', '# fuzzy turning', '% fuzzy turning',
            '# total'
        ),
        (
            'TRAIN',
            s_tr, round(s_tr / tr * 100.), fs_tr, round(fs_tr / tr * 100.),
            c_tr, round(c_tr / tr * 100.), fc_tr, round(fc_tr / tr * 100.),
            tr
        ),
        (
            'VAL',
            s_v, round(s_v / v * 100.), fs_v, round(fs_v / v * 100.),
            c_v, round(c_v / v * 100.), fc_v, round(fc_v / v * 100.),
            v
        ),
        (
            'TRAINVAL',
            s_tv, round(s_tv / tv * 100.), fs_tv, round(fs_tv / tv * 100.),
            c_tv, round(c_tv / tv * 100.), fc_tv, round(fc_tv / tv * 100.),
            tv
        ),
        (
            'TEST',
            s_te, round(s_te / te * 100.), fs_te, round(fs_te / te * 100.),
            c_te, round(c_te / te * 100.), fc_te, round(fc_te / te * 100.),
            te
        ),
        (
            'TOTAL',
            s_t, round(s_t / t * 100.), fs_t, round(fs_t / t * 100.),
            c_t, round(c_t / t * 100.), fc_t, round(fc_t / t * 100.),
            t
        )
    )
)
