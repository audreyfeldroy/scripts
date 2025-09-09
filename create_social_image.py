# /// script
# dependencies = [
#   "Pillow",
# ]
# ///

"""
Create a beautiful 1500x500px social image.
Usage:
  uv venv 2025-08-29-create-social-image.py --title "My Brand" --subtitle "@handle" --out out.png

This UV-style script declares Pillow as a dependency so `uv run` will install it when used.
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import random
import argparse
import os

WIDTH = 1500
HEIGHT = 500

DEFAULT_TITLE = "Audrey M. Roy Greenfeld"
DEFAULT_SUBTITLE = "@audreyfeldroy"
DEFAULT_OUT = "social-header-1500x500.png"

def lerp(a, b, t):
    return int(a + (b - a) * t)

def blend_color(c1, c2, t):
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))

def create_gradient_background(width, height, top_color, bottom_color):
    img = Image.new("RGB", (width, height), color=0)
    for y in range(height):
        t = y / (height - 1)
        color = blend_color(top_color, bottom_color, t)
        ImageDraw.Draw(img).line([(0, y), (width, y)], fill=color)
    return img

def add_radial_shapes(base, shapes=3):
    w, h = base.size
    overlay = Image.new("RGBA", base.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    for i in range(shapes):
        rx = random.randint(int(w * 0.1), int(w * 0.9))
        ry = random.randint(int(h * 0.1), int(h * 0.9))
        rr = random.randint(int(min(w,h) * 0.2), int(min(w,h) * 0.6))
        color = (255 - i*30, 200 - i*20, 230, 40) if i % 2 == 0 else (200, 230, 255 - i*20, 36)
        bbox = [rx-rr, ry-rr, rx+rr, ry+rr]
        draw.ellipse(bbox, fill=color)
    blurred = overlay.filter(ImageFilter.GaussianBlur(radius=80))
    return Image.alpha_composite(base.convert("RGBA"), blurred)

def add_stripes(base):
    w, h = base.size
    overlay = Image.new("RGBA", base.size, (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    spacing = 40
    thickness = 10
    for x in range(-w, w*2, spacing):
        draw.line([(x, 0), (x + w, h)], fill=(255,255,255,8), width=thickness)
    striped = overlay.filter(ImageFilter.GaussianBlur(radius=6))
    return Image.alpha_composite(base.convert("RGBA"), striped)

def add_noise(base, intensity=18):
    w, h = base.size
    noise = Image.new("RGBA", base.size)
    pixels = noise.load()
    for y in range(h):
        for x in range(w):
            v = random.randint(0, intensity)
            pixels[x,y] = (v, v, v, 12)
    return Image.alpha_composite(base.convert("RGBA"), noise)

def draw_text(base, title, subtitle):
    draw = ImageDraw.Draw(base)
    w, h = base.size
    # Try common macOS/Windows fonts, fall back to default
    font_title = None
    font_sub = None
    for path in [
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        try:
            font_title = ImageFont.truetype(path, 60)
            font_sub = ImageFont.truetype(path, 28)
            break
        except Exception:
            font_title = None
    if font_title is None:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # drop shadow
    tx = w // 2
    ty = h // 2 - 30
    # Use textbbox for accurate sizing (compatible with modern Pillow)
    try:
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w, title_h = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
        sub_bbox = draw.textbbox((0, 0), subtitle, font=font_sub)
        sub_w, sub_h = sub_bbox[2] - sub_bbox[0], sub_bbox[3] - sub_bbox[1]
    except Exception:
        # Fallback for older Pillow versions
        title_w, title_h = font_title.getsize(title) if hasattr(font_title, 'getsize') else (0, 0)
        sub_w, sub_h = font_sub.getsize(subtitle) if hasattr(font_sub, 'getsize') else (0, 0)

    # center
    title_xy = (tx - title_w // 2, ty - title_h // 2)
    sub_xy = (tx - sub_w // 2, ty + title_h // 2 + 10)

    # shadow
    draw.text((title_xy[0]+2, title_xy[1]+2), title, font=font_title, fill=(0,0,0,120))
    draw.text((sub_xy[0]+1, sub_xy[1]+1), subtitle, font=font_sub, fill=(0,0,0,90))

    # main
    draw.text(title_xy, title, font=font_title, fill=(255,255,255,230))
    draw.text(sub_xy, subtitle, font=font_sub, fill=(245,245,245,220))

    return base


def generate(title="Your Brand", subtitle="@yourhandle", out_path="social-header-1500x500.png"):
    # Colors chosen for a pleasant teal->purple gradient
    top_color = (20, 120, 140)   # teal
    bottom_color = (120, 40, 140) # purple
    print(f"Creating {WIDTH}x{HEIGHT} image...")
    bg = create_gradient_background(WIDTH, HEIGHT, top_color, bottom_color)
    layered = add_radial_shapes(bg, shapes=4)
    layered = add_stripes(layered)
    layered = add_noise(layered, intensity=18)
    layered = layered.filter(ImageFilter.GaussianBlur(radius=1))
    # Convert back to RGB for final drawing
    final = layered.convert("RGBA")
    final = draw_text(final, title, subtitle)
    # subtle vignette
    vignette = Image.new("L", (WIDTH, HEIGHT), 0)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # distance from center
            dx = (x - WIDTH/2) / (WIDTH/2)
            dy = (y - HEIGHT/2) / (HEIGHT/2)
            d = (dx*dx + dy*dy)
            v = int(255 * (d * 0.4))
            vignette.putpixel((x,y), max(0, min(180, v)))
    final.putalpha(255)
    # Use the vignette as a mask that selects the black edge and preserves the final image in the center
    final = Image.composite(Image.new("RGBA", final.size, (0,0,0,255)), final, vignette)

    # Save as PNG
    final.convert("RGB").save(out_path, format="PNG")
    print(f"Saved: {os.path.abspath(out_path)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default=DEFAULT_TITLE, help="Main title text")
    parser.add_argument("--subtitle", default=DEFAULT_SUBTITLE, help="Subtitle or handle")
    parser.add_argument("--out", default=DEFAULT_OUT, help="Output filename")
    args = parser.parse_args()
    generate(args.title, args.subtitle, args.out)
