from pygame.image import load
from pygame import font
from pygame import transform

def load_sprite(name, scale_num=1, with_alpha=True,):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        image = loaded_sprite.convert_alpha()
        size = image.get_size()
        return transform.scale(image, (int(size[0]*scale_num), int(size[1]*scale_num)))
    else:
        image = loaded_sprite.convert()
        size = image.get_size()
        return transform.scale(image, (int(size[0]*scale_num), int(size[1]*scale_num)))

def use_font(name, size):
    return font.Font(f"assets/fonts/{name}.ttf", size)