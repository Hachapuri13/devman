from PIL import Image

image = Image.open("avatar.jpg")

if image.mode == "CMYK":
    image = image.convert("RGB")

red_canal, green_canal, blue_canal = image.split()

shift = image.width/14
left_shift = (shift, 0, image.width, image.height)
right_shift = (0, 0, image.width-shift, image.height)
middle_shift =(shift/2, 0, image.width-shift/2, image.height)

left_red = red_canal.crop(left_shift)
middle_red = red_canal.crop(middle_shift)
red_shift = Image.blend(left_red, middle_red, 0.5)

right_blue = blue_canal.crop(right_shift)
middle_blue = blue_canal.crop(middle_shift)
blue_shift = Image.blend(right_blue, middle_blue, 0.5)

middle_green = green_canal.crop(middle_shift)

retro_userpic = Image.merge("RGB", (red_shift, middle_green, blue_shift))
avatar_max_size = (80, 80)
retro_userpic.thumbnail(avatar_max_size)
retro_userpic.save("userpic.jpg")