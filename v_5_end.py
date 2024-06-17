from pathlib import Path

from tqdm import tqdm

from tab import BEV, TAB, Visualizer


vis = Visualizer(
    BEV(mode=BEV.Mode.CONSTANT),
    mode=Visualizer.Mode.END,
    palette=Visualizer.Palette.END,
    width=2,
    save=True,
    dst=Path.cwd().joinpath('vis', 'end')
)

tab = TAB(Path.cwd().joinpath('data', 'TAB'), 'train')

for f in tqdm(tab):
    vis(f.sequence, f.id, tab.get_pcd(f), tab.get_boundaries(f))
