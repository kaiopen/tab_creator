# 可通行区域边缘数据集标注工具

[English](README.md)

### Python 环境
- tqdm
- PIL
- NumPy
- Matplotlib
- [PyTorch](https://pytorch.org)
- [KaiTorch](https://github.com/kaiopen/kaitorch)
- [TABKit](https://github.com/kaiopen/tab_kit)

### 标准工具
[LabelMe](https://github.com/labelmeai/labelme)

### 文件目录
```
.
|-- data
|   |-- raw
|   |   |-- pcd  // 原始点云文件
|   |   |   |-- <序列名称>
|   |   |   |   |-- <时间戳>.pcd
|   |   |   |   |-- <时间戳>.pcd
|   |   |   |   |-- ……
|   |   |   |-- <序列名称>
|   |   |   |   |-- <时间戳>.pcd
|   |   |   |   |-- <时间戳>.pcd
|   |   |   |   |-- ……
|   |   |   |-- ……
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

### 标注与处理
1. 提取点云文件，获取频率为5Hz的点云序列。该过程不复制或修改点云文件。该过程产生的结果为有序记录点云时间戳的文本文件，文件名为`<序列名称>.txt`。结果保存在 `./data/raw/` 路径中。指令格式如下：
```
python a_0_pick_5Hz.py <序列名称>
```
例如
```shell
python a_0_pick_5Hz.py 2021-12-31-15-10-20
```

2. 生成用于标注的鸟瞰图。结果保存在 `./data/raw/bev/` 路径中。指令格式如下：
```
python a_1_generate_bev.py <序列名称>
```
例如
```shell
python a_1_generate_bev.py 2021-12-31-15-10-20
```

3. 【可选项】分割地面。此处给出了简单的点云地面分割方法。可以尝试其他方法。结果保存在 `./data/raw/ground/` 路径中。指令格式如下：
```
python a_2_segment_ground.py <序列名称>
```
例如
```shell
python a_2_segment_ground.py 2021-12-31-15-10-20
```

4. 【可选项】检测路牙。结果保存在 `./data/raw/bev/` 路径中。指令格式如下：
```
python a_3_detect_curb.py <序列名称>
```
例如
```shell
python a_3_detect_curb.py 2021-12-31-15-10-20
```

5. 使用 LabelMe 标注工具标注可通行区域边缘曲线及其语义。推荐使用折线、直线和点，这三种几何形状勾勒边缘曲线。

6. 检查标注的边缘曲线及其语义。指令格式如下：
```
python a_4_check_semantics.py <序列名称>
```
例如
```shell
python a_4_check_semantics.py 2021-12-31-15-10-20
```

7. 使用 LabelMe 标注工具标注可通行区域边缘的复杂性。推荐使用折线、直线和点，这三种几何形状完成标注。

8. 检查可通行区域边缘的复杂性。格式如下：
```
python a_5_check_complexity.py <序列名称>
```
例如
```shell
python a_5_check_complexity.py 2021-12-31-15-10-20
```

9. 修正点云，包括旋转和裁减点云。同时根据标注的结果，将具有连续标注的点云序列保存在一个路径中，不连续的点云序列保存在不同路径中。结果保存在 `./data/TAB/pcd/` 路径中。该步骤生成的点云文件即为可从 [TAB](https://github.com/kaiopen/tab) 下载的文件。指令格式如下：
```
python a_6_part_pcd.py <序列名称>
```
例如
```shell
python a_6_part_pcd.py 2021-12-31-15-10-20
```

10. 生成（半成品）真值文件。结果保存在 `./data/TAB/boundary/` 路径中。该步骤生成的真值文件即为可从 [TAB](https://github.com/kaiopen/tab) 下载的文件。指令格式如下：
```
python a_7_generate_bound.py <序列名称>
```
例如
```shell
python a_7_generate_bound.py 2021-12-31-15-10-20
```

11. 划分训练集、验证集和测试集。结果保存在 `./data/TAB/` 路径中。该步骤生成的文件即为可从 [TAB](https://github.com/kaiopen/tab) 下载的文件。指令如下：
```shell
python a_8_split.py
```

### 统计与分析

<font color=Orange>注意：</font>进行统计与分析之前，需要初始化数据集。在 `./data/TAB/` 路径下运行
```shell
python init_boundary.py
```

`init_boundary.py` 文件可在 [TAB](https://github.com/kaiopen/tab) 中获取。若已完成初始化，则无需重复操作。

1. 统计语义数量与占比。结果保存在 `./statistics/semantics.csv` 文件中。指令如下：
```shell
python s_0_semantics.py
```

2. 统计形状数量与占比。结果保存在 `./statistics/shape.csv` 文件中。指令如下：
```shell
python s_1_shape.py
```

3. 统计复杂性的数量与占比。结果保存在 `./statistics/complexity.csv` 文件中。指令如下：
```shell
python s_2_complexity.py
```

4. 统计复杂场景的数量与占比。结果保存在 `./statistics/complex.csv` 文件中。指令如下：
```shell
python s_3_complex.py
```

5. 统计弯道与路口数量与占比。结果保存在 `./statistics/bend.csv` 文件中。指令如下：
```shell
python s_4_bend_intersection.py
```

6. 统计最远距离。结果保存在 `./statistics/distance.csv` 文件中。指令如下：
```shell
python s_5_distance.py
```

7. 统计长度。结果保存在 `./statistics/length.csv` 文件中。指令如下：
```shell
python s_6_length.py
```

8. 统计空间分布。训练-验证集结果保存在 `./statistics/space_tv.csv` 文件中，测试集结果保存在 `./statistics/space_te.csv` 文件中。指令如下：
```shell
python s_7_space.py
```

### 可视化
<font color=Orange>注意：</font>进行可视化之前，需要初始化数据集。在 `./data/TAB/` 路径下运行
```shell
python init_boundary.py
```
`init_boundary.py` 文件可在 [TAB](https://github.com/kaiopen/tab) 中获取。若已完成初始化，则无需重复操作。

1. 可视化语义。结果保存在 `./vis/semantics/` 路径中。指令如下：
```shell
python v_0_semantics.py
```

2. 可视化形状。结果保存在 `./vis/curve/` 路径中。指令如下：
```shell
python v_1_curve.py
```

3. 可视化结构性。结果保存在 `./vis/unstructured/` 路径中。指令如下：
```shell
python v_2_unstructured.py
```

4. 可视化不清晰可见部分。结果保存在 `./vis/unclear/` 路径中。指令如下：
```shell
python v_3_unclear.py
```

5. 可视化单线边缘。结果保存在 `./vis/single/` 路径中。指令如下：
```shell
python v_4_single.py
```

6. 可视化端点。结果保存在 `./vis/end/` 路径中。指令如下：
```shell
python v_5_end.py
```
