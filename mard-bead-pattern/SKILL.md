---
name: mard-bead-pattern
description: 拼豆小助手 - 将图片转换为专业 MARD/MARDI 拼豆图纸。支持智能配色、自动裁切、镜像输出、ZIP 打包。
author: 杜维
version: 1.0.0
source: https://github.com/wdu496132-rgb/duwei-bead-pattern-assistant
---

# 🧿 拼豆小助手 - MARD Bead Pattern

## Workflow

当用户要求制作拼豆图纸、MARD 色号图纸、fuse-bead pattern、Perler-style chart、mirrored bead chart 或专业珠豆软件风格导出时，使用此技能。

### 1. 分析输入图片

检查输入图片的尺寸和主体类型：
- 图片分辨率
- 主体类型（人物、动物、物品、抽象）
- 复杂度（简单/中等/密集）

### 2. 选择网格尺寸

根据复杂度选择合适网格：
- **小型 Q版/简单图标**: `80x100`, `100x120`, `104x104`, `104x130`
- **半身像/肖像**: `104x156`, `120x180`, `128x192`
- **全身/双人/密集海报**: `156x234`, `176x264`, `176x312`, `208x312`

### 3. 裁剪与预处理

当图片有大量空白背景时，自动裁剪主体周围区域。不要盲目地将整个源图压缩到固定网格。

### 4. 色彩匹配

在 CIELAB 色彩空间中匹配 MARD/MARDI 色号，不使用普通 RGB 最近颜色。

### 5. 生成图纸

导出完整的 PNG 图纸：
- 顶部主珠串网格
- 每个格子着色并标注 MARD 色号
- 可见的网格线
- 每 26 个珠子添加红色分隔线
- 底部颜色区域，显示 MARD 色号、色卡和数量

### 6. 镜像输出

当用户可能需要反向转印图案时，导出镜像版本。

### 7. 打包输出

将输出打包为 ZIP。如果使用 Gmail 发送且 ZIP 超过常见附件限制，拆分为正常/镜像 ZIP。

## Script

运行 `mard-bead-pattern/scripts/mard_pattern_generator.py` 进行确定性生成。

### 单张图片示例

```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input image.jpg \
  --output-dir out \
  --grid 104x104 \
  --colors 42 \
  --mirror \
  --zip-name pattern.zip
```

### 批量处理示例

```bash
python3 mard-bead-pattern/scripts/mard_pattern_generator.py \
  --input-dir ./images \
  --output-dir out \
  --grid 176x312 \
  --colors 58 \
  --mirror \
  --zip-name batch.zip
```

## Quality Rules

- 使用足够高的 `--cell-px` 值以确保单元格色号可读。小网格使用 `35-42`，大网格使用 `24-30`。
- 主图纸宽度保持在 4000px 以上以满足"4K"请求。
- 对于已经是像素/珠豆风格的图片，使用中等网格如 `100x120` 或 `104x104`；避免不必要的放大添加假细节。
- 对于高大的多角色海报图纸，如果用户想要所有角色，保留完整海报；选择高网格而不是裁剪到单个主体。
- 保持颜色数量实用。典型值为小/简单图片 `26-46`，密集海报 `50-64`。

## 依赖

```
Pillow
opencv-python
numpy
```

## 输出格式

```
output/
├── 01_name_104x104_normal_MARD.png  # 正常版图纸
├── 01_name_104x104_mirror_MARD.png  # 镜像版图纸
└── pattern.zip                       # 打包文件
```

## 许可证

MIT License

---

*🧿 拼豆小助手 - 杜维 | 基于 jiahao31530-crypto/mard-bead-pattern-skill 修改*
