# MARD Bead Pattern Skill - 杜维修改版

**作者**: 杜维  
**版本**: 1.0.0  
**来源**: [jiahao31530-crypto/mard-bead-pattern-skill](https://github.com/jiahao31530-crypto/mard-bead-pattern-skill)

---

## 简介

这是一个用于将图片转换为专业 MARD/MARDI 拼豆图纸的 Agnes 技能。

## 功能特性

- 根据图片复杂度选择合适的珠串网格尺寸
- 自动裁剪主体周围的空白区域
- 在 CIELAB 色彩空间中匹配 MARD/MARDI 色号
- 生成高分辨率 PNG 图纸，每个格子标注 MARD 色号
- 每 26 个珠子添加红色分隔线
- 底部添加颜色区域，显示色号、色卡和数量
- 导出正常和镜像版本，并打包为 ZIP

## 使用方法

### 单张图片

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

### 批量处理

```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror \
  --zip-name batch.zip
```

## 网格尺寸建议

| 图片类型 | 推荐网格 |
|----------|----------|
| 小型 Q版/简单图标 | 80x100, 100x120, 104x104, 104x130 |
| 半身像/肖像 | 104x156, 120x180, 128x192 |
| 全身/双人/密集海报 | 156x234, 176x264, 176x312, 208x312 |

## 依赖

- Python 3
- Pillow
- opencv-python
- numpy

## 许可证

MIT License

---

*基于 [jiahao31530-crypto/mard-bead-pattern-skill](https://github.com/jiahao31530-crypto/mard-bead-pattern-skill) 修改*
