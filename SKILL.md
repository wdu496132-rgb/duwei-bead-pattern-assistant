---
name: bead-assistant
description: 拼豆小助手 - 将图片转换为专业 MARD/MARDI 拼豆图纸。支持智能配色、自动裁切、镜像输出、ZIP 打包。
author: 杜维
version: 1.0.0
source: https://github.com/wdu496132-rgb/duwei-bead-pattern-assistant
---

# 🧿 拼豆小助手 - MARD Bead Pattern

## Workflow

当用户要求制作拼豆图纸、MARD 色号图纸、fuse-bead pattern、Perler-style chart 时，使用此技能。

### 1. 分析输入图片
- 检查图片尺寸和主体类型
- 判断图片复杂度

### 2. 选择网格尺寸
- 小型 Q版/简单图标: `80x100`, `100x120`, `104x104`
- 半身像/肖像: `104x156`, `120x180`
- 全身/密集海报: `156x234`, `176x312`

### 3. 生成图纸
```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input image.jpg \
  --output-dir out \
  --grid 104x104 \
  --colors 42 \
  --mirror
```

### 4. 批量处理
```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror
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

## 依赖

```
Pillow
opencv-python
numpy
```

---

*🧿 拼豆小助手 - 杜维*
