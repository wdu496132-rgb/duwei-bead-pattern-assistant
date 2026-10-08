# 🧿 拼豆小助手

**作者**: 杜维  
**版本**: 1.0.0  
**来源**: 基于 [mard-bead-pattern-skill](https://github.com/jiahao31530-crypto/mard-bead-pattern-skill) 修改

---

## 简介

拼豆小助手是一款专业的 **MARD/MARDI 拼豆图纸生成工具**，可以将任意图片快速转换为可打印的拼豆图纸。

## 功能特性

- 🎨 **智能配色** - CIELAB 色彩空间精确匹配 MARD 色号
- 📐 **自动裁切** - 智能识别主体，去除多余背景
- 📊 **专业图纸** - 每个珠子格标注色号，清晰易读
- 🔄 **镜像输出** - 支持正常/镜像双版本导出
- 📦 **一键打包** - 自动压缩为 ZIP，方便分享打印

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 单张图片生成

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input image.jpg \
  --output-dir out \
  --grid 104x104 \
  --colors 42 \
  --cell-px 40 \
  --mirror
```

### 批量处理

```bash
python mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror
```

## 依赖

- Python 3
- Pillow
- opencv-python
- numpy

## 许可证

MIT License

---

*🧿 让拼豆制作更简单！*
