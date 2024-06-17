from pathlib import Path

from tqdm import tqdm

from tab import BEV, TAB, Visualizer


vis = Visualizer(
    BEV(mode=BEV.Mode.CONSTANT),
    mode=Visualizer.Mode.UNCLEAR,
    palette=Visualizer.Palette.UNCLEAR,
    width=2,
    save=True,
    dst=Path.cwd().joinpath('vis', 'unclear')
)

tab = TAB(Path.cwd().joinpath('data', 'TAB'), 'train')
# tab = TAB(Path.cwd().joinpath('data', 'TAB'), 'val')
# tab = TAB(Path.cwd().joinpath('data', 'TAB'), 'test')

for f in tqdm(tab):
    vis(f.sequence, f.id, tab.get_pcd(f), tab.get_boundaries(f))
