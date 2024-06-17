from pathlib import Path

from PIL import Image
import numpy as np
import torch

from kaitorch.typing import TorchTensor, TorchFloat
from kaitorch.data import Group, cell_from_size, mask_in_range, \
    min_max_normalize, reverse_group, xy_to_rt
from kaitorch.pcd import PointClouds
from kaitorch.utils import pseudo_colors

from utils import adjust_pcd_, load_pcd, read_seq, \
    RANGE_RHO, RANGE_THETA, RANGE_Z, RANGE_X_E, RANGE_Y_E, RANGE_INTENSITY, \
    SIZE, ERROR, CLOSED


class BEVGenerator:
    def __init__(self, *args, **kwargs) -> None:
        self._r_xyz = list(RANGE_X_E) + list(RANGE_Y_E) + list(RANGE_Z)
        self._r_int = RANGE_INTENSITY

        lower_bound = torch.as_tensor((RANGE_X_E[0], RANGE_Y_E[0]))
        upper_bound = torch.as_tensor((RANGE_X_E[1], RANGE_Y_E[1]))

        cell = cell_from_size(lower_bound, upper_bound, SIZE, ERROR, CLOSED)
        self._group = Group(lower_bound, cell, ERROR, CLOSED, upper_bound)

        self._h, self._w = SIZE
        self._num_pillar = self._h * self._w

        anchors = reverse_group(
            torch.stack(
                torch.meshgrid(
                    torch.arange(self._h),
                    torch.arange(self._w),
                    indexing='ij'
                ),
                dim=-1
            ).reshape(-1, 2) + 0.5,
            lower_bound, cell
        )
        self._mask = torch.logical_not(
            mask_in_range(
                xy_to_rt(anchors), list(RANGE_RHO) + list(RANGE_THETA)
            )
        )

    def __call__(self, pcd: PointClouds) -> TorchTensor[TorchFloat]:
        pcd.filter_(mask_in_range(pcd.xyz_, self._r_xyz))
        groups = self._group(pcd.xy_)

        ids = self._w * groups[:, 0] + groups[:, 1]
        ids, indices = torch.sort(ids)
        ids, counts = torch.unique_consecutive(
            ids, return_counts=True
        )

        points_z = pcd.z_
        points_i = pcd.intensity_
        mask = torch.zeros((self._num_pillar,), dtype=bool)
        colors = []
        i = 0
        for id, c in zip(ids.tolist(), torch.cumsum(counts, dim=0).tolist()):
            inds = indices[i: c]
            colors.append(points_i[inds][torch.argmax(points_z[inds])])
            mask[id] = True
            i = c
        bev = torch.zeros((self._num_pillar, 3))
        bev[self._mask] = 0.1
        bev[mask] = pseudo_colors(
            min_max_normalize(
                torch.clip(torch.as_tensor(colors), *RANGE_INTENSITY),
                *RANGE_INTENSITY
            )
        )
        return torch.permute(bev.reshape(self._h, self._w, 3), (1, 0, 2))


seq = read_seq()

dir_pcd = Path.cwd().joinpath('data', 'raw', 'pcd', seq)
dir_dst = Path.cwd().joinpath('data', 'raw', 'bev', seq)
dir_dst.mkdir(parents=True, exist_ok=True)

generator = BEVGenerator()

for id in Path.cwd().joinpath(
    'data', 'raw', seq + '.txt'
).read_text().splitlines():
    print(id)

    Image.fromarray(
        (
            generator(
                adjust_pcd_(load_pcd(dir_pcd.joinpath(id + '.pcd')))
            ) * 255
        ).numpy().astype(np.uint8)
    ).convert('RGB').save(dir_dst.joinpath(id + '.png'))
