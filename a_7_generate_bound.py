from typing import Sequence, Tuple, Union
import math
import json
from pathlib import Path

import torch

from kaitorch.data import ReverseGroup, cell_from_size

from utils import read_seq, \
    RANGE_X_E, RANGE_Y_E, RANGE_RHO, SIZE, ERROR, CLOSED, BOUNDARY


R = RANGE_RHO[1]
SQU_R = math.pow(R, 2)
CATEOGRIES = BOUNDARY[:2]


def get_line(
    a: tuple[float, float], b: Tuple[float, float]
) -> Tuple[float, float]:
    x_a, y_a = a
    x_b, y_b = b
    return (0, x_b * (y_a - y_b) / (x_b - x_a) + y_b)


def get_circle(
    a: Tuple[float, float], b: Tuple[float, float]
) -> Tuple[float, float]:
    x_a, y_a = a
    x_b, y_b = b

    del_x = x_a - x_b
    del_y = y_a - y_b
    squ_d = del_x * del_x + del_y * del_y
    d = math.sqrt(squ_d)
    t = -x_b * del_x - y_b * del_y

    d_bp = t / d
    d_pe = math.sqrt(
        SQU_R
        - math.pow(t * del_x / squ_d + x_b, 2)
        - math.pow(t * del_y / squ_d + y_b, 2)
    )
    d_be = d_bp - d_pe
    return (d_be * del_x / d + x_b, d_be * del_y / d + y_b)


def clip_linestrip(
    linestrip: Sequence[Tuple[float, float]]
) -> Union[Sequence[Tuple[float, float]], None]:
    r'''
    NOTE: Each segment must cross or in the valid area. Just the first valid
    linestrip will be picked out.

    `x = 0` is a valid line.

    '''
    num = len(linestrip)
    if 0 == num:
        return None
    if 1 == num:
        x, y = linestrip[0]
        if 0 == x or x * x + y * y <= SQU_R:
            return linestrip
        return None

    end = start = -1
    for i in range(num - 1):
        j = i + 1
        a = linestrip[i]
        b = linestrip[j]
        x_a, y_a = a
        x_b, y_b = b
        if 0 == x_a:
            if -1 == start:
                start = i

            if 0 >= x_b:
                end = j

                if x_b * x_b + y_b * y_b > SQU_R:  # end of a linestrip
                    # Modify the end of the linestrip.
                    linestrip[j] = get_circle(a, b)
                    break
            else:  # end of a linestrip
                end = i
                break

        elif x_a < 0:  # may be the start of a linestrip
            if 0 == x_b:  # start of a linestrip
                end = start = j
            elif x_b > 0:  # start of a linestrip
                # Modify the start of the linestrip.
                linestrip[i] = get_line(a, b)
                start = i
                end = j

                if x_b * x_b + y_b * y_b > SQU_R:  # end of a linestrip
                    # Modify the end of the linestrip.
                    linestrip[j] = get_circle(a, b)
                    break
            # else the segment is not a valid part of a linestrip.

        else:
            if 0 == x_b:
                if -1 == start:
                    if x_a * x_a + y_a * y_a > SQU_R:
                        # Modify the start of the linestrip.
                        linestrip[i] = get_circle(a, b)
                    start = i

                end = j

            elif x_b < 0:  # end of a linestrip
                if -1 == start:
                    if x_a * x_a + y_a * y_a > SQU_R:
                        # Modify the start of the linestrip.
                        linestrip[i] = get_circle(a, b)
                    start = i

                # Modify the end of the linestrip.
                linestrip[j] = get_line(a, b)
                end = j
                break

            else:
                # Check the two points if they are out of the bound.
                x_a = x_a * x_a + y_a * y_a  # r_a^2
                x_b = x_b * x_b + y_b * y_b  # r_b^2
                if SQU_R == x_a:
                    if -1 == start:
                        start = i

                    if x_b <= SQU_R:
                        end = j
                    else:  # end of a linestrip
                        end = i
                        break

                elif x_a < SQU_R:
                    if -1 == start:
                        start = i

                    end = j
                    if x_b > SQU_R:  # end of a linestrip
                        # Modify the end of the linestrip.
                        linestrip[j] = get_circle(a, b)
                        break

                else:  # may be the start of a linestrip
                    if SQU_R == x_b:  # start of a linestrip
                        end = start = j
                    elif x_b < SQU_R:  # start of a linestrip
                        # Modify the start of the linestrip
                        linestrip[i] = get_circle(b, a)
                        start = i
                        end = j
                    # else the segment is not a valid part of a linestrip.

    return linestrip[start: end + 1]


seq = read_seq()

dir_anno = Path.cwd().joinpath('data', 'raw', 'bev', seq)
dir_bound = Path.cwd().joinpath('data', 'TAB', 'boundary')
dir_bound.mkdir(parents=True, exist_ok=True)

lower_bound = torch.as_tensor((RANGE_X_E[0], RANGE_Y_E[0]))
reverse = ReverseGroup(
    lower_bound,
    cell=cell_from_size(
        lower_bound, torch.as_tensor((RANGE_X_E[1], RANGE_Y_E[1])),
        SIZE, ERROR, CLOSED
    ),
    error=ERROR
)

for d in Path.cwd().joinpath('data', 'TAB', 'pcd').glob(seq + '-*'):
    dst = dir_bound.joinpath(d.stem)
    dst.mkdir(parents=True, exist_ok=True)

    for f in d.glob('*.pcd'):
        print(f)

        filename = f.stem + '.json'
        f_anno = dir_anno.joinpath(filename)
        if f_anno.exists():
            shapes = json.load(f_anno.open('r'))['shapes']

            # Process boundaries first.
            bounds = []
            comxs = []
            # For each boundary, get semantics and keypoints.
            for shape in shapes:
                lab = shape['label']
                if lab in BOUNDARY:
                    linestrip = clip_linestrip(
                        reverse(torch.as_tensor(shape['points'])).tolist()
                    )
                    if linestrip is None:
                        raise Exception('an invalid boundary.')

                    if lab in CATEOGRIES:
                        bounds.append(
                            {
                                'semantics': 'straight-going_side'
                                if 'straight' == lab else 'turning',
                                'fuzzy': False,
                                'linestrip': linestrip
                            }
                        )
                    else:
                        bounds.append(
                            {
                                'semantics': 'straight-going_side'
                                if 's' == lab[-1] else 'turning',
                                'fuzzy': True,
                                'linestrip': linestrip
                            }
                        )

                elif lab != 'curb':
                    v = lab[2]
                    comxs.append(
                        {
                            'curve': 'c' == lab[1],
                            'unstructured': 'u' == lab[0],
                            'irregular': 'i' == v,
                            'occluded': 'o' == v,
                            'blind': 'b' == v,
                            'distorted': 'd' == v,
                            'lengthened': 'l' == v,
                            'single': 's' == lab[3],
                            'linestrip': reverse(
                                torch.as_tensor(shape['points'])
                            ).tolist(),
                        }
                    )

            json.dump(
                {
                    'boundaries': bounds,
                    'complexity': comxs
                },
                dst.joinpath(filename).open('w'),
                indent=2
            )
