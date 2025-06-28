#!/bin/zsh

python3 <<EOF
from PIL import Image, ImageDraw

width, height = 600, 1000
border_thickness = 40
background_color = (54, 86, 89)  # Desaturated teal
border_color = (15, 15, 15)      # Obsidian black

img = Image.new("RGB", (width, height), border_color)
draw = ImageDraw.Draw(img)
draw.rectangle(
    [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
    fill=background_color
)

img.save("tarot_card_base.png")
print("🖤 Tarot base created: tarot_card_base.png")
EOF
