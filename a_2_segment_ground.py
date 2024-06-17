from typing import Optional, Tuple
import math
from pathlib import Path

import torch

from kaitorch.typing import TorchTensor, TorchTensorLike, \
    TorchFloat, TorchInt64, TorchReal, Bool, Real
from kaitorch.data import Group, cell_from_size, PI
from kaitorch.pcd import PointCloudXYZIRID, PointCloudWriterXYZIRID, \
    PointClouds

from utils import adjust_pcd_, filter_pcd_, load_pcd, read_seq, \
    RANGE_RHO, RANGE_THETA


class GroundSegmentation:
    def __init__(
        self,
        range_rt: TorchTensorLike[Real],
        size: TorchTensorLike[Real],
        ground: TorchTensorLike[Real],

        error: TorchTensorLike[Real] = torch.as_tensor(0),
        closed: TorchTensorLike[Bool] = torch.as_tensor(False),
        window: Tuple[int, int] = (5, 5),
        height: float = 0.1,
        grad: float = math.tan(18. / 180. * PI),
        *args, **kwargs
    ) -> None:
        range_rt = torch.as_tensor(range_rt)
        lower_bound = range_rt[[0, 2]]
        upper_bound = range_rt[[1, 3]]
        size = torch.as_tensor(size)
        error = torch.as_tensor(error)
        closed = torch.as_tensor(closed)

        self._group = Group(
            lower_bound=lower_bound,
            cell=cell_from_size(lower_bound, upper_bound, size, error, closed),
            error=error,
            closed=closed,
            upper_bound=upper_bound
        )

        self._num_ann, self._num_sec = size.tolist()
        self._num_grid = self._num_ann * self._num_sec

        self._ground = torch.as_tensor(ground)
        self._l_ann, self._l_sec = window
        self._u_ann = self._l_ann + 1
        self._u_sec = self._l_sec + 1

        self._t_height_0 = height
        self._t_height_1 = -height
        self._t_grad_0 = grad
        self._t_grad_1 = -grad

    def __call__(
        self, pcd: PointClouds, ground: Optional[TorchTensor[TorchReal]] = None
    ) -> TorchTensor[TorchFloat]:
        ids, scores = self.get_map(pcd, ground)

        # Assign each point with a occupancy score.
        scores = scores.flatten()
        occ = torch.zeros(len(pcd))
        for i in torch.nonzero(
            torch.logical_and(scores != 0, scores != -10), as_tuple=True
        )[0].tolist():
            occ[ids == i] = scores[i]
        return occ

    def get_map(
        self, pcd: PointClouds, ground: Optional[TorchTensor[TorchReal]] = None
    ) -> Tuple[TorchTensor[TorchInt64], TorchTensor[TorchFloat]]:
        groups = self._group(pcd.rt_)
        # Assign a grid ID to each point.
        ids = self._num_sec * groups[:, 0] + groups[:, 1]
        _ids, indices = torch.sort(ids)
        _ids, counts = torch.unique_consecutive(_ids, return_counts=True)

        grids = torch.zeros((self._num_grid, 5))
        scores = -10 * torch.ones(self._num_grid)

        points_xy = pcd.xy_
        points_z = pcd.z_
        i = 0
        for id, c in zip(_ids.tolist(), torch.cumsum(counts, dim=0).tolist()):
            _inds = indices[i: c]

            grids[id, :2] = torch.mean(points_xy[_inds])
            grids[id, 2] = torch.max(points_z[_inds])
            grids[id, 3: 5] = groups[_inds[0]]
            scores[id] = 0

            i = c

        grids = grids.reshape(self._num_ann, self._num_sec, 5)
        scores = scores.reshape(self._num_ann, self._num_sec)

        if ground is None:
            ground = self._ground
        base_xy = ground[:2]
        base_z = ground[2]
        for i_sec in range(self._num_sec):
            ground_xy = base_xy
            ground_z = base_z
            for i_ann in range(self._num_ann):
                inds_ann, inds_sec = torch.meshgrid(
                    torch.arange(
                        max(i_ann - self._l_ann, 0),
                        min(i_ann + self._u_ann, self._num_ann)
                    ),
                    torch.arange(
                        max(i_sec - self._l_sec, 0),
                        min(i_sec + self._u_sec, self._num_sec)
                    ),
                    indexing='ij'
                )
                inds_ann = inds_ann.flatten()
                inds_sec = inds_sec.flatten()

                inds = torch.nonzero(
                    0 == scores[inds_ann, inds_sec], as_tuple=True
                )[0]

                _grids = grids[inds_ann[inds], inds_sec[inds]]
                zs = _grids[:, 2] - ground_z

                m = zs >= self._t_height_0
                if torch.any(m):
                    gs = _grids[m]
                    gs = gs[
                        zs[m] / torch.linalg.norm(gs[:, :2] - ground_xy, dim=1)
                        >= self._t_grad_0
                    ]
                    scores[
                        gs[:, 3].type(torch.long), gs[:, 4].type(torch.long)
                    ] = 1

                m = zs <= self._t_height_1
                if torch.any(m):
                    gs = _grids[m]
                    gs = gs[
                        zs[m] / torch.linalg.norm(gs[:, :2] - ground_xy, dim=1)
                        <= self._t_grad_1
                    ]
                    scores[
                        gs[:, 3].type(torch.long), gs[:, 4].type(torch.long)
                    ] = -1

                if 0 == scores[i_ann, i_sec]:
                    ground = grids[i_ann, i_sec]
                    ground_xy = ground[:2]
                    ground_z = ground[2]

        return ids, scores


seq = read_seq()

dir = Path.cwd().joinpath('data', 'raw', 'pcd', seq)
dst = Path.cwd().joinpath('data', 'raw', 'ground', seq)

seg = GroundSegmentation(
    range_rt=list(RANGE_RHO) + list(RANGE_THETA),
    size=(200, 180),
    ground=(0, 0, -0.72)
)
writer = PointCloudWriterXYZIRID()

for id in Path.cwd().joinpath(
    'data', 'raw', seq + '.txt'
).read_text().splitlines():
    print(id)
    id += '.pcd'
    pcd = filter_pcd_(adjust_pcd_(load_pcd(dir.joinpath(id))))
    pcd = PointCloudXYZIRID(pcd.xyz_, pcd.intensity_, pcd.ring_, seg(pcd))
    writer(pcd, dst.joinpath(id))
