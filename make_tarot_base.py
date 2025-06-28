from PIL import Image, ImageDraw, ImageFilter
import random

width, height = 600, 1000
border_thickness = 40
background_color = (54, 86, 89)
border_color = (15, 15, 15)

# Base image
img = Image.new("RGB", (width, height), border_color)
draw = ImageDraw.Draw(img)

# Fill background
draw.rectangle(
    [border_thickness, border_thickness, width - border_thickness, height - border_thickness],
    fill=background_color
)

# Add light noise
for x in range(border_thickness, width - border_thickness):
    for y in range(border_thickness, height - border_thickness):
        if random.random() < 0.03:
            r = background_color[0] + random.randint(-10, 10)
            g = background_color[1] + random.randint(-10, 10)
            b = background_color[2] + random.randint(-10, 10)
            draw.point((x, y), fill=(max(0, min(r,255)), max(0, min(g,255)), max(0, min(b,255))))

# Glitch band at top third
glitch_y = height // 3
for i in range(10):
    offset = random.randint(-8, 8)
    img.paste(img.crop((border_thickness, glitch_y + i, width - border_thickness, glitch_y + i + 1)),
              (border_thickness + offset, glitch_y + i))

img.save("tarot_card_base_glitchy.png")
print("✨ Tarot base with glitch created: tarot_card_base_glitchy.png")