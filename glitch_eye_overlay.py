from PIL import Image

# Load base tarot card
base = Image.open("tarot_card_base.png").convert("RGBA")

# Load the eye overlay
eye = Image.open("test/eye.png").convert("RGBA")

# Resize and position the eye
eye = eye.resize((200, 200))
x = (base.width - eye.width) // 2
y = int(base.height * 0.15)
base.paste(eye, (x, y), eye)

# Save the result
base.save("tarot_card_base_glitchy.png")
print("👁️ Eye overlay added.")