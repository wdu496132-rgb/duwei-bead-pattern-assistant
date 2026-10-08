# 🧿 拼豆小助手 - MARD Bead Pattern Assistant

**作者**: 杜维  
**版本**: 1.0.0  
**来源**: 基于 [mard-bead-pattern-skill](https://github.com/jiahao31530-crypto/mard-bead-pattern-skill) 修改

---

## 📌 简介

拼豆小助手是一款专业的 **MARD/MARDI 拼豆图纸生成工具**，可以将任意图片快速转换为可打印的拼豆图纸，支持 Perler 珠、Hama 珠、MARD 珠等主流拼豆品牌。

✨ **核心功能**：
- 🎨 **智能配色** - CIELAB 色彩空间精确匹配 MARD 色号
- 📐 **自动裁切** - 智能识别主体，去除多余背景
- 📊 **专业图纸** - 每个珠子格标注色号，清晰易读
- 🔄 **镜像输出** - 支持正常/镜像双版本导出
- 📦 **一键打包** - 自动压缩为 ZIP，方便分享打印

---

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

依赖包：
- `Pillow` - 图像处理
- `opencv-python` - 色彩空间转换
- `numpy` - 数值计算

### 单张图片生成

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input image.jpg \
  --output-dir out \
  --grid 104x104 \
  --colors 42 \
  --cell-px 40 \
  --mirror \
  --zip-name pattern.zip
```

### 批量处理

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror \
  --zip-name batch.zip
```

---

## 📐 网格尺寸推荐

| 图片类型 | 推荐网格 | 适用场景 |
|---------|---------|---------|
| 小型 Q版/简单图标 | `80x100`, `100x120`, `104x104` | 小挂件、钥匙扣 |
| 半身像/肖像 | `104x156`, `120x180`, `128x192` | 人像、角色头像 |
| 全身/双人/密集海报 | `156x234`, `176x264`, `176x312`, `208x312` | 全身像、群像海报 |

---

## ⚙️ 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--input` | string | 否 | - | 单张图片路径 |
| `--input-dir` | string | 否 | - | 图片目录（批量处理） |
| `--output-dir` | string | ✅ | - | 输出目录 |
| `--grid` | string | ✅ | - | 网格尺寸，格式：`宽x高`，如 `104x104` |
| `--colors` | int | 否 | 46 | 颜色数量（26-64） |
| `--cell-px` | int | 否 | 36 | 每个珠子的像素大小 |
| `--mirror` | flag | 否 | false | 导出镜像版本 |
| `--no-auto-crop` | flag | 否 | false | 禁用自动裁切 |
| `--chart-html` | string | 否 | - | 本地 MARD 色卡 HTML |
| `--zip-name` | string | 否 | mard_patterns.zip | ZIP 文件名 |

---

## 🎯 使用示例

### 示例 1：简单图标转图纸

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input icon.png \
  --output-dir out \
  --grid 104x104 \
  --colors 26 \
  --cell-px 40 \
  --mirror
```

### 示例 2：人物肖像

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input portrait.jpg \
  --output-dir out \
  --grid 128x192 \
  --colors 42 \
  --cell-px 36 \
  --mirror
```

### 示例 3：密集海报

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input poster.png \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --cell-px 30 \
  --mirror
```

---

## 📁 输出说明

生成结果包含：
```
out/
├── 01_image_104x104_normal_MARD.png   # 正常版图纸
├── 01_image_104x104_mirror_MARD.png   # 镜像版图纸
└── pattern.zip                         # 打包文件
```

**图纸内容**：
- 顶部：主珠串网格，每个格子标注 MARD 色号
- 红色分隔线：每 26 个珠子一条分隔线
- 底部：颜色区域，显示色号、色卡和数量

---

## 🔧 质量建议

- **单元格大小**：小网格用 35-42px，大网格用 24-30px
- **图纸宽度**：4K 请求建议宽度 > 4000px
- **颜色数量**：简单图 26-46 色，密集海报 50-64 色
- **自动裁切**：默认开启，可自动去除空白背景

---

## 📜 许可证

MIT License

Copyright (c) 2026 杜维  
Original work copyright (c) jiahao31530-crypto

---

## 🔗 相关链接

- 原始仓库：https://github.com/jiahao31530-crypto/mard-bead-pattern-skill
- MARD 色卡：https://www.pixel-beads.com/en/mard-bead-color-chart
- Agnes 技能：`$mard-bead-pattern`

---

*🧿 让拼豆制作更简单！*
