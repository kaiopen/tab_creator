# Travelable Area Boundary Dataset and Benchmark Annotation Toolkit

[中文](README.md)

### Python Environment
- tqdm
- PIL
- NumPy
- Matplotlib
- [PyTorch](https://pytorch.org)
- [KaiTorch](https://github.com/kaiopen/kaitorch)
- [TABKit](https://github.com/kaiopen/tab_kit)

### Annotation Tools
[LabelMe](https://github.com/labelmeai/labelme)

### File Structures
```
.
|-- data
|   |-- pcd  // raw point cloud files
|   |   |-- <sequence>
|   |   |   |-- <timestamp>.pcd
|   |   |   |-- <timestamp>.pcd
|   |   |   |-- ...
|   |   |-- <sequence>
|   |   |   |-- <timestamp>.pcd
|   |   |   |-- <timestamp>.pcd
|   |   |   |-- ...
|   |   |-- ...
|-- a_0_pick_5Hz.py
|-- a_1_generate_bev.py
|-- a_2_segment_ground.py
|-- a_3_detect_curb.py
|-- a_4_check_semantics.py
|-- a_5_check_complexity.py
|-- a_6_part_pcd.py
|-- a_7_generate_bound.py
|-- a_8_split.py
|-- s_0_semantics.py
|-- s_1_shape.py
|-- s_2_complexity.py
|-- s_3_complex.py
|-- s_4_bend_intersection.py
|-- s_5_distance.py
|-- s_6_length.py
|-- s_7_space.py
|-- v_0_semantics.py
|-- v_1_curve.py
|-- v_2_unstructured.py
|-- v_3_unclear.py
|-- v_4_single.py
|-- v_5_end.py
|-- utils.py
|-- LICENSE
|-- README.md
|-- README_EN.md
```

### Annotation and Processing
1. Sample point cloud files at a frequency of 5 Hz. No point cloud file will be modified or copied. Some text files will be created to record the timestamps of ordered point cloud files. The text file is named in the form of `<sequence>.txt`. The results will be saved in `./data/raw/`. Run the following command to complete this operation:
```
python a_0_pick_5Hz.py <sequence>
```
For example,
```shell
python a_0_pick_5Hz.py 2021-12-31-15-10-20
```

2. Generate bird's eye view images for labeling. The results will be saved in `./data/raw/bev/`. Run the following command to complete this operation:
```
python a_1_generate_bev.py <sequence>
```
For example,
```shell
python a_1_generate_bev.py 2021-12-31-15-10-20
```

3. [OPTIONAL] Segment the ground. Here a simple segmentation method is given. Other methods can be tested. The results will be saved in `./data/raw/ground/`. Run the following command to complete this operation:
```
python a_2_segment_ground.py <sequence>
```
For example,
```shell
python a_2_segment_ground.py 2021-12-31-15-10-20
```

4. [OPTIONAL] Detect curbs. The results will be saved in `./data/raw/bev/`. Run the following command to complete this operation:
```
python a_3_detect_curb.py <sequence>
```
For example,
```shell
python a_3_detect_curb.py 2021-12-31-15-10-20
```

5. Label boundaries and their guiding semantics with LabelMe. Boundaries can be outlined via linestrips, lines and points.

6. Check the labeled boundaries with their semantics. Run the following command to complete this operation:
```
python a_4_check_semantics.py <sequence>
```
For example,
```shell
python a_4_check_semantics.py 2021-12-31-15-10-20
```

7. Label shapes and complexities of the boundaries with LabelMe. Linestrips, lines and points are recommended to be used.

8. Check the labeled shapes and complexities. Run the following command to complete this operation:
```
python a_5_check_complexity.py <sequence>
```
For example,
```shell
python a_5_check_complexity.py 2021-12-31-15-10-20
```

9. Rotate and clip point clouds. And split point cloud files into different sub-sequence. Continuous point cloud files will be saved in a sub-sequence. The results will be saved in `./data/TAB/pcd/`. The published point cloud files of the [TAB](https://github.com/kaiopen/tab) are the products of this step. Run the following command to complete this operation:
```
python a_6_part_pcd.py <sequence>
```
For example,
```shell
python a_6_part_pcd.py 2021-12-31-15-10-20
```

10. Generate semi-finished ground truth files. The results will be saved in `./data/TAB/boundary/`. The published ground truth files of the [TAB](https://github.com/kaiopen/tab) are the products of this step. Run the following command to complete this operation:
```
python a_7_generate_bound.py <sequence>
```
For example,
```shell
python a_7_generate_bound.py 2021-12-31-15-10-20
```

11. Split training set, validation set and test set. The results will be saved in `./data/TAB/`. The published split files of the [TAB](https://github.com/kaiopen/tab) are the products of this step. Run the following command to complete this operation:
```shell
python a_8_split.py
```

### Statistics

<font color=Orange>NOTE:</font> Before do the following steps, change to the `./data/TAB/` and run the command first to finish initialization:
```shell
python init_boundary.py
```

`init_boundary.py` can be obtained from [TAB](https://github.com/kaiopen/tab). If the initialization has been done before, no need to run the command.

1. Semantics. The results will be saved in `./statistics/semantics.csv`. Run the following command to complete this operation:
```shell
python s_0_semantics.py
```

2. Shape. The results will be saved in `./statistics/shape.csv`. Run the following command to complete this operation:
```shell
python s_1_shape.py
```

3. Complexity. The results will be saved in `./statistics/complexity.csv`. Run the following command to complete this operation:
```shell
python s_2_complexity.py
```

4. Complex scenes. The results will be saved in `./statistics/complex.csv`. Run the following command to complete this operation:
```shell
python s_3_complex.py
```

5. Bend and intersections. The results will be saved in `./statistics/bend.csv`. Run the following command to complete this operation:
```shell
python s_4_bend_intersection.py
```

6. The farthest distances. The results will be saved in `./statistics/distance.csv`. Run the following command to complete this operation:
```shell
python s_5_distance.py
```

7. Length. The results will be saved in `./statistics/length.csv`. Run the following command to complete this operation:
```shell
python s_6_length.py
```

8. Space distribution. The results of the training-validation set will be saved in `./statistics/space_tv.csv`. The results of the test set will be saved in `./statistics/space_te.csv`. Run the following command to complete this operation:
```shell
python s_7_space.py
```

### Visualization

<font color=Orange>NOTE:</font> Before do the following steps, change to the `./data/TAB/` and run the command first to finish initialization:
```shell
python init_boundary.py
```

`init_boundary.py` can be obtained from [TAB](https://github.com/kaiopen/tab). If the initialization has been done before, no need to run the command.

1. Semantics. The results will be saved in `./vis/semantics/`. Run the following command to complete this operation:
```shell
python v_0_semantics.py
```

2. Curve parts. The results will be saved in `./vis/curve/`. Run the following command to complete this operation:
```shell
python v_1_curve.py
```

3. Unstructured parts. The results will be saved in `./vis/unstructured/`. Run the following command to complete this operation:
```shell
python v_2_unstructured.py
```

4. Unclear parts. The results will be saved in `./vis/unclear/`. Run the following command to complete this operation:
```shell
python v_3_unclear.py
```

5. Single boundaries. The results will be saved in `./vis/single/`. Run the following command to complete this operation:
```shell
python v_4_single.py
```

6. Endpoints. The results will be saved in `./vis/end/`. Run the following command to complete this operation:
```shell
python v_5_end.py
```
