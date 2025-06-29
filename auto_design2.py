import os
from PIL import Image, ImageDraw, ImageFont

# === Settings ===
logoed = 'Images/bg1.jpg'
plain =  'Images/bg2.jpg'
bgPath = 'unspecified'
output_path = "Output/first.png"

inputType = input('Which type of output do you want? \n1. Plain background, not text wrapping' \
'\n2. Logoed background with text wrapping\n')

if int(inputType) == 1 : 
    bgPath = plain
else : 
    bgPath = logoed
bg_path = os.path.join(os.path.dirname(__file__), bgPath)


font_path = r"alfont_com_29LT-Azer-Regular.otf"  # Change to your desired Arabic font

image = Image.open(bg_path).convert("RGB")  # Ensure RGB mode

text_color = (0, 0, 0)  # Black text

# === Prepare to draw ===
draw = ImageDraw.Draw(image)
image_width, image_height = image.size


def createHeaderImage(bg_path, text, font):

    # === Calculate text position (centered) ===
    text_bbox = draw.textbbox((0, 0), text, font=font, direction='rtl')
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (image.size[0] - text_width) // 2
    y = (image.size[1] - text_height) // 2

    # === Draw the Arabic text with direction support ===
    draw.text((x, y), text, fill=text_color, font=font, direction='rtl')

    # === Save the final image ===
    image.save(output_path)

    print(f"Image saved as: {output_path}")

#=========================================


def wrap_arabic_text(text, font, max_width, draw):
    words = text.split(' ')  # Split text by Arabic spaces
    lines = []
    line = ''
    
    for word in words:
        test_line = word if line == '' else line + ' ' + word
        width = draw.textlength(test_line, font=font, direction='rtl')
        if width <= max_width:
            line = test_line
        else:
            if line:  # Avoid empty line
                lines.append(line)
            line = word  # Start new line with the word that didn’t fit
    if line:  # Append last line
        lines.append(line)
    return lines




inputText = input('Enter the text needed: \n')
inputTextSize = input('Enter the text size needed: \n')

fontSize = int(inputTextSize)

font = ImageFont.truetype(font_path, fontSize)


if(int(inputType) == 1): 
    createHeaderImage(bg_path, inputText, font)
else : 
    bg_path = os.path.join(os.path.dirname(__file__), logoed)

    output_path = "Output/second.png"


    # === Wrap text ===
    max_text_width = int(image_width * 0.9)  # Allow 90% width
    lines = wrap_arabic_text(inputText, font, max_text_width, draw)

    # === Calculate total height of all lines ===
    line_height = font.getbbox("hg")[3] - font.getbbox("hg")[1] + 20  # 10px padding between lines
    total_text_height = line_height * len(lines)

    # === Starting Y to vertically center ===
    y_start = (image_height - total_text_height) // 2

    # === Draw each line ===
    for line in lines:
        line_width = draw.textlength(line, font=font, direction='rtl')
        x = (image_width - line_width) // 2  # Centering
        draw.text((x, y_start), line, font=font, fill=text_color, direction='rtl')
        y_start += line_height
    # === Save result ===
    image.save(output_path)
    print(f"Saved wrapped Arabic text image to: {output_path}")