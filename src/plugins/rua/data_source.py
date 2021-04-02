from os import path
from io import BytesIO
from PIL import Image, ImageDraw

from src.utils.util import async_request


data_dir = path.abspath(path.join(__file__, "..", "data"))


async def get_avatar(qq: int) -> Image.Image:
    url = f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160'
    resp = await async_request('get', url)
    avatar = Image.open(BytesIO(resp.content))
    return avatar


def get_circle_avatar(avatar, size) -> Image.Image:
    # avatar.thumbnail((size, size))
    avatar = avatar.resize((size, size))
    scale = 5
    mask = Image.new('L', (size * scale, size * scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask.resize((size, size), Image.ANTIALIAS)
    ret_img = avatar.copy()
    ret_img.putalpha(mask)
    return ret_img


def generate_gif(avatar: Image.Image) -> str:
    avatar_size = [(350,350), (372,305), (395,283), (380,305), (350,372)]
    avatar_pos = [(50,150), (28,195), (5,217), (5,195), (50,128)]
    imgs = []

    for i in range(5):
        im = Image.new(mode='RGBA', size=(600, 600), color='white')
        hand = Image.open(path.join(data_dir, f'hand-{i+1}.png'))
        hand = hand.convert('RGBA')
        avatar = get_circle_avatar(avatar, 350)
        avatar = avatar.resize(avatar_size[i])
        im.paste(avatar, avatar_pos[i], mask=avatar.split()[3])
        im.paste(hand, mask=hand.split()[3])
        mask = im.split()[3]
        mask = Image.eval(mask, lambda a: 255 if a <= 50 else 0)
        im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
        im.paste(255, mask)
        imgs.append(im)

    out_path = path.join(data_dir, 'output.gif')
    imgs[0].save(fp=out_path, save_all=True, append_images=imgs, duration=25, loop=0, quality=80)

    return out_path
