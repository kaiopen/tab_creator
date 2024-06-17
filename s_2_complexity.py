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

u_tr = 0
i_tr = 0
o_tr = 0
b_tr = 0
d_tr = 0
l_tr = 0
s_tr = 0
tr = 0
for f in tab_train:
    bounds = tab_train.get_boundaries(f)
    tr += len(bounds)

    for bound in bounds:
        u = i = o = b = d = l = False
        for p in bound['points']:
            if p['unstructured']:
                u = True
            if p['irregular']:
                i = True
            if p['occluded']:
                o = True
            if p['blind']:
                b = True
            if p['distorted']:
                d = True
            if p['lengthened']:
                l = True

        u_tr += u
        i_tr += i
        o_tr += o
        b_tr += b
        d_tr += d
        l_tr += l
        s_tr += bound['single']

u_v = 0
i_v = 0
o_v = 0
b_v = 0
d_v = 0
l_v = 0
s_v = 0
val = 0
for f in tab_val:
    bounds = tab_val.get_boundaries(f)
    val += len(bounds)

    for bound in bounds:
        u = i = o = b = d = l = False
        for p in bound['points']:
            if p['unstructured']:
                u = True
            if p['irregular']:
                i = True
            if p['occluded']:
                o = True
            if p['blind']:
                b = True
            if p['distorted']:
                d = True
            if p['lengthened']:
                l = True

        u_v += u
        i_v += i
        o_v += o
        b_v += b
        d_v += d
        l_v += l
        s_v += bound['single']

u_tv = u_tr + u_v
i_tv = i_tr + i_v
o_tv = o_tr + o_v
b_tv = b_tr + b_v
d_tv = d_tr + d_v
l_tv = l_tr + l_v
s_tv = s_tr + s_v
tv = tr + val

u_te = 0
i_te = 0
o_te = 0
b_te = 0
d_te = 0
l_te = 0
s_te = 0
te = 0
for f in tab_test:
    bounds = tab_train.get_boundaries(f)
    te += len(bounds)

    for bound in bounds:
        u = i = o = b = d = l = False
        for p in bound['points']:
            if p['unstructured']:
                u = True
            if p['irregular']:
                i = True
            if p['occluded']:
                o = True
            if p['blind']:
                b = True
            if p['distorted']:
                d = True
            if p['lengthened']:
                l = True

        u_te += u
        i_te += i
        o_te += o
        b_te += b
        d_te += d
        l_te += l
        s_te += bound['single']

u_t = u_tv + u_te
i_t = i_tv + i_te
o_t = o_tv + o_te
b_t = b_tv + b_te
d_t = d_tv + d_te
l_t = l_tv + l_te
s_t = s_tv + s_te
t = tv + te

dst = Path.cwd().joinpath('statistics')
dst.mkdir(parents=True, exist_ok=True)
csv.writer(dst.joinpath('complexity.csv').open('w')).writerows(
    (
        (
            '',
            '# unstructured', '% unstructured', '# irregular', '% irregular',
            '# occluded', '% occluded', '# blind', '% blind',
            '# distorted', '% distorted', '# lengthened', '% lengthened',
            '# single', '% single', '# total'
        ),
        (
            'TRAIN',
            u_tr, round(u_tr / tr * 100.), i_tr, round(i_tr / tr * 100.),
            o_tr, round(o_tr / tr * 100.), b_tr, round(b_tr / tr * 100.),
            d_tr, round(d_tr / tr * 100.), l_tr, round(l_tr / tr * 100.),
            s_tr, round(s_tr / tr * 100.), tr
        ),
        (
            'VAL',
            u_v, round(u_v / val * 100.), i_v, round(i_v / val * 100.),
            o_v, round(o_v / val * 100.), b_v, round(b_v / val * 100.),
            d_v, round(d_v / val * 100.), l_v, round(l_v / val * 100.),
            s_v, round(s_v / val * 100.), val
        ),
        (
            'TRAINVAL',
            u_tv, round(u_tv / tv * 100.), i_tv, round(i_tv / tv * 100.),
            o_tv, round(o_tv / tv * 100.), b_tv, round(b_tv / tv * 100.),
            d_tv, round(d_tv / tv * 100.), l_tv, round(l_tv / tv * 100.),
            s_tv, round(s_tv / tv * 100.), tv
        ),
        (
            'TEST',
            u_te, round(u_te / te * 100.), i_te, round(i_te / te * 100.),
            o_te, round(o_te / te * 100.), b_te, round(b_te / te * 100.),
            d_te, round(d_te / te * 100.), l_te, round(l_te / te * 100.),
            s_te, round(s_te / te * 100.), te
        ),
        (
            'TOTAL',
            u_t, round(u_t / t * 100.), i_t, round(i_t / t * 100.),
            o_t, round(o_t / t * 100.), b_t, round(b_t / t * 100.),
            d_t, round(d_t / t * 100.), l_t, round(l_t / t * 100.),
            s_t, round(s_t / t * 100.), t
        )
    )
)
