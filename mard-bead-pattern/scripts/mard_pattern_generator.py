#!/usr/bin/env python3
"""
MARD Bead Pattern Generator - 拼豆小助手
作者：杜维
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import urllib.request
import zipfile
from collections import Counter
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


MARD_COLOR_CHART_URL = "https://www.pixel-beads.com/en/mard-bead-color-chart"
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


def parse_grid(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+)x(\d+)", value.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("grid must look like 104x104 or 208x312")
    return int(match.group(1)), int(match.group(2))


def read_chart_html(path: str | None) -> str:
    if path:
        return Path(path).read_text(errors="ignore")
    request = urllib.request.Request(MARD_COLOR_CHART_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "ignore")


def load_palette(chart_html: str | None) -> list[tuple[str, tuple[int, int, int]]]:
    html = read_chart_html(chart_html)
    pairs = re.findall(
        r'style="background-color:(#[0-9A-Fa-f]{6})".*?text-\[\#EF4444\][^>]*>#<!-- -->([A-Z]\d+)',
        html,
    )
    by_code: dict[str, str] = {}
    for hex_value, code in pairs:
        by_code.setdefault(code, hex_value.upper())
    if len(by_code) < 120:
        raise RuntimeError(f"Could not extract enough MARD colors; found {len(by_code)}")
    return [
        (code, tuple(int(hex_value[i : i + 2], 16) for i in (1, 3, 5)))
        for code, hex_value in sorted(by_code.items(), key=lambda item: (item[0][0], int(item[0][1:])))
    ]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def ink(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    r, g, b = rgb
    return (255, 255, 255) if (0.299 * r + 0.587 * g + 0.114 * b) < 125 else (18, 18, 18)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fill, fnt) -> None:
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = box[0] + (box[2] - box[0] - tw) / 2
    y = box[1] + (box[3] - box[1] - th) / 2 - 1
    draw.text((x, y), text, fill=fill, font=fnt)


def subject_crop(im: Image.Image, grid: tuple[int, int], auto_crop: bool) -> Image.Image:
    if not auto_crop:
        return fit_ratio(im, grid)
    arr = np.array(im.convert("RGB"))
    hsv = cv2.cvtColor(arr, cv2.COLOR_RGB2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]
    mask = ((sat > 24) | (val < 170)).astype(np.uint8) * 255
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    ys, xs = np.where(mask > 0)
    if len(xs) < 100:
        return fit_ratio(im, grid)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    pad_x = max(8, int((x1 - x0) * 0.08))
    pad_y = max(8, int((y1 - y0) * 0.06))
    crop = im.crop((max(0, x0 - pad_x), max(0, y0 - pad_y), min(im.width, x1 + pad_x), min(im.height, y1 + pad_y)))
    return fit_ratio(crop, grid)


def fit_ratio(im: Image.Image, grid: tuple[int, int]) -> Image.Image:
    cols, rows = grid
    target_ratio = cols / rows
    current_ratio = im.width / im.height
    if abs(current_ratio - target_ratio) < 0.01:
        return im
    if current_ratio > target_ratio:
        new_h = round(im.width / target_ratio)
        canvas = Image.new("RGB", (im.width, new_h), (248, 248, 246))
        canvas.paste(im, (0, (new_h - im.height) // 2))
    else:
        new_w = round(im.height * target_ratio)
        canvas = Image.new("RGB", (new_w, im.height), (248, 248, 246))
        canvas.paste(im, ((new_w - im.width) // 2, 0))
    return canvas


def quantize_to_mard(
    im: Image.Image,
    grid: tuple[int, int],
    color_count: int,
    palette: list[tuple[str, tuple[int, int, int]]],
) -> tuple[np.ndarray, list[str], list[tuple[int, int, int]]]:
    cols, rows = grid
    small = im.convert("RGB").resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = np.array(small, dtype=np.uint8)
    lab = cv2.cvtColor(pixels.reshape(-1, 1, 3), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 80, 0.3)
    _, labels, centers = cv2.kmeans(lab, color_count, None, criteria, 4, cv2.KMEANS_PP_CENTERS)
    palette_rgb = np.array([rgb for _, rgb in palette], dtype=np.uint8).reshape(-1, 1, 3)
    palette_lab = cv2.cvtColor(palette_rgb, cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    center_to_palette = [int(np.linalg.norm(palette_lab - center, axis=1).argmin()) for center in centers]
    palette_indices = np.array(center_to_palette, dtype=np.int32)[labels.flatten()].reshape(rows, cols)
    used = sorted(set(palette_indices.flatten()), key=lambda idx: palette[idx][0])
    remap = {old: new for new, old in enumerate(used)}
    code_grid = np.vectorize(remap.get)(palette_indices).astype(np.int16)
    return code_grid, [palette[idx][0] for idx in used], [palette[idx][1] for idx in used]


def make_sheet(
    grid_data: np.ndarray,
    codes: list[str],
    colors: list[tuple[int, int, int]],
    title: str,
    cell_px: int,
    mirror: bool,
) -> Image.Image:
    if mirror:
        grid_data = np.fliplr(grid_data)
    rows, cols = grid_data.shape
    counts = Counter(grid_data.flatten().tolist())
    board_w, board_h = cols * cell_px, rows * cell_px
    margin, title_h, gap = 34, 62, 22
    tile_w, tile_h = 250, 82
    legend_cols = max(1, board_w // tile_w)
    legend_rows = math.ceil(len(codes) / legend_cols)
    legend_h = legend_rows * tile_h + 44
    canvas = Image.new("RGB", (board_w + margin * 2, title_h + board_h + gap + legend_h + margin), (246, 246, 242))
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 18), title, fill=(22, 22, 22), font=font(24, True))
    ox, oy = margin, title_h
    cell_font = font(max(7, int(cell_px * 0.28)), True)
    for y in range(rows):
        for x in range(cols):
            idx = int(grid_data[y, x])
            box = (ox + x * cell_px, oy + y * cell_px, ox + (x + 1) * cell_px, oy + (y + 1) * cell_px)
            draw.rectangle(box, fill=colors[idx])
            centered(draw, box, codes[idx], ink(colors[idx]), cell_font)
    for x in range(cols + 1):
        xx = ox + x * cell_px
        draw.line((xx, oy, xx, oy + board_h), fill=(220, 20, 28) if x % 26 == 0 else (84, 84, 84), width=4 if x % 26 == 0 else 1)
    for y in range(rows + 1):
        yy = oy + y * cell_px
        draw.line((ox, yy, ox + board_w, yy), fill=(220, 20, 28) if y % 26 == 0 else (84, 84, 84), width=4 if y % 26 == 0 else 1)
    ly = oy + board_h + gap
    draw.rectangle((margin, ly, margin + board_w, ly + legend_h - 10), fill=(255, 255, 255), outline=(25, 25, 25), width=3)
    draw.text((margin + 18, ly + 12), "MARD COLOR AREA", fill=(25, 25, 25), font=font(20, True))
    for i, code in enumerate(codes):
        col, row = i % legend_cols, i // legend_cols
        x0, y0 = margin + col * tile_w + 14, ly + 46 + row * tile_h
        draw.rectangle((x0, y0 + 8, x0 + 64, y0 + 64), fill=colors[i], outline=(18, 18, 18), width=2)
        draw.text((x0 + 78, y0 + 10), f"MARD {code}", fill=(18, 18, 18), font=font(22, True))
        draw.text((x0 + 78, y0 + 40), f"{counts[i]} pcs", fill=(58, 58, 58), font=font(18))
    return canvas


def input_files(args: argparse.Namespace) -> list[Path]:
    if args.input:
        return [Path(args.input)]
    root = Path(args.input_dir)
    return sorted(path for path in root.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)


def main() -> int:
    parser = argparse.ArgumentParser(description="拼豆小助手 - MARD Bead Pattern Generator")
    parser.add_argument("--input", help="单张图片路径")
    parser.add_argument("--input-dir", help="图片目录（批量处理）")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--grid", type=parse_grid, required=True, help="网格尺寸，如 104x104")
    parser.add_argument("--colors", type=int, default=46, help="颜色数量 (默认: 46)")
    parser.add_argument("--cell-px", type=int, default=36, help="单元格像素大小 (默认: 36)")
    parser.add_argument("--mirror", action="store_true", help="导出镜像版本")
    parser.add_argument("--no-auto-crop", action="store_true", help="禁用自动裁切")
    parser.add_argument("--chart-html", help="本地 MARD 色卡 HTML")
    parser.add_argument("--zip-name", default="mard_patterns.zip", help="ZIP 文件名")
    args = parser.parse_args()
    
    if not args.input and not args.input_dir:
        parser.error("请提供 --input 或 --input-dir")
    
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    palette = load_palette(args.chart_html)
    outputs: list[Path] = []
    
    for index, path in enumerate(input_files(args), 1):
        im = Image.open(path).convert("RGB")
        prepared = subject_crop(im, args.grid, not args.no_auto_crop)
        grid, codes, colors = quantize_to_mard(prepared, args.grid, args.colors, palette)
        variants = [False, True] if args.mirror else [False]
        
        for mirror in variants:
            suffix = "mirror" if mirror else "normal"
            cols, rows = args.grid
            title = f"{path.stem} {cols}x{rows} {'MIRROR' if mirror else 'NORMAL'}"
            sheet = make_sheet(grid, codes, colors, title, args.cell_px, mirror)
            output = out_dir / f"{index:02d}_{path.stem}_{cols}x{rows}_{suffix}_MARD.png"
            sheet.save(output, optimize=True)
            outputs.append(output)
            print(f"✓ {output}")
    
    zip_path = out_dir / args.zip_name
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for output in outputs:
            zf.write(output, output.name)
    
    print(f"\n📦 ZIP: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
