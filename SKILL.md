---
name: mard-bead-pattern
description: 拼豆小助手 - 将图片转换为专业 MARD/MARDI 拼豆图纸。支持智能配色、自动裁切、镜像输出、ZIP 打包。
author: 杜维
version: 1.0.0
source: https://github.com/wdu496132-rgb/duwei-bead-pattern-assistant
---

# 🧿 拼豆小助手

## 功能概述

本技能用于将图片转换为专业的 MARD/MARDI 拼豆图纸，支持 Perler 珠、Hama 珠等主流拼豆品牌。

## 工作流程

当用户要求制作拼豆图纸、MARD 色号图纸、fuse-bead pattern、Perler-style chart 时，使用此技能。

### 1. 分析输入图片

- 检查图片尺寸和主体类型
- 判断图片复杂度（简单/中等/密集）

### 2. 选择网格尺寸

根据图片类型选择合适网格：
- **小型 Q版/简单图标**: `80x100`, `100x120`, `104x104`, `104x130`
- **半身像/肖像**: `104x156`, `120x180`, `128x192`
- **全身/双人/密集海报**: `156x234`, `176x264`, `176x312`, `208x312`

### 3. 生成图纸

运行脚本：

```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input image.jpg \
  --output-dir out \
  --grid 104x104 \
  --colors 42 \
  --cell-px 40 \
  --mirror \
  --zip-name pattern.zip
```

### 4. 批量处理

```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror \
  --zip-name batch.zip
```

## 参数说明

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| `--input` | string | 否 | - | 单张图片 |
| `--input-dir` | string | 否 | - | 图片目录 |
| `--output-dir` | string | ✅ | - | 输出目录 |
| `--grid` | string | ✅ | - | 网格尺寸 |
| `--colors` | int | 否 | 46 | 颜色数量 |
| `--cell-px` | int | 否 | 36 | 单元格像素 |
| `--mirror` | flag | 否 | - | 镜像输出 |
| `--zip-name` | string | 否 | mard_patterns.zip | ZIP 文件名 |

## 质量建议

- 单元格大小：小网格 35-42px，大网格 24-30px
- 图纸宽度：4K 请求建议 > 4000px
- 颜色数量：简单图 26-46 色，密集海报 50-64 色

## 依赖

```
Pillow
opencv-python
numpy
```

## 输出文件

- `01_name_grid_normal_MARD.png` - 正常版图纸
- `01_name_grid_mirror_MARD.png` - 镜像版图纸
- `pattern.zip` - 打包文件

---

*🧿 拼豆小助手 - 让拼豆制作更简单*
