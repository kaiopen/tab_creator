from typing import Union
import argparse
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import torch

from kaitorch.data import mask_in_range, rotate_point_2d, PI
from kaitorch.pcd import PointCloudReaderXYZIR, PointClouds, PointCloudXYZIR


RANGE_RHO = (0, 20)
RANGE_THETA = (-PI / 2., PI / 2.)
RANGE_X = (0, 20)
RANGE_Y = (-20, 20)
RANGE_Z = (-1.5, 1.5)

RANGE_X_E = (-1, 21)
RANGE_Y_E = (-21, 21)

RANGE_INTENSITY = (0, 18)

PHI = torch.as_tensor(PI / 12)

SIZE = torch.as_tensor((2200, 4200))
ERROR = torch.as_tensor((0, 0))
CLOSED = torch.as_tensor((False, False))

BOUNDARY = ('straight', 'turning', 'fuzzys', 'fuzzyt')


def read_seq() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument('seq', type=str)
    args = parser.parse_args()
    return args.seq


def adjust_pcd_(pcd: PointClouds) -> PointClouds:
    xyz = pcd.xyz_
    xyz[:, [2, 0]] = rotate_point_2d(xyz[:, [2, 0]], PHI)
    pcd.update_xyz_(xyz)
    return pcd


def filter_pcd_(pcd: PointClouds) -> PointClouds:
    pcd.filter_(mask_in_range(pcd.rho_, RANGE_RHO))
    pcd.filter_(mask_in_range(pcd.theta_, RANGE_THETA))
    pcd.filter_(mask_in_range(pcd.z_, RANGE_Z))
    return pcd


def load_pcd(f: Union[Path, str]) -> PointCloudXYZIR:
    return PointCloudXYZIR.from_similar(PointCloudReaderXYZIR(f))


def round(x: float):
    return float(Decimal(str(x)).quantize(Decimal('0.00'), ROUND_HALF_UP))
