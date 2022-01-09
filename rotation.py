from PIL import Image, ImageDraw, ImageFilter, ImageChops


img = Image.open('cropped.jpg').convert('RGBA')
#rotate in any degree
rotated = img.rotate(45, fillcolor = 0, expand=True)
rotated.save('rotated.png')
