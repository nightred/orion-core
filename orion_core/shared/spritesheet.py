# spritesheet management

import logging
from PIL import Image
import arcade


logger = logging.getLogger(__name__)


class Spritesheet(object):

    sprite_textures = []

    def __init__(self, file: str, tile_size: int):
        try:
            image = Image.open(file)
        except:
            logger.error("unable to read file: {}".format(file))
            return

        width, height = image.size
        tiles_wide = int(width // tile_size)
        tiles_tall = int(height // tile_size)

        for y in range(tiles_tall):
            for x in range(tiles_wide):
                left = x * tile_size
                top = y * tile_size
                right = left + tile_size
                bottom = top + tile_size
                cropped = image.crop((left, top, right, bottom))
                texture = arcade.Texture(f"{file}{x}{y}", cropped)
                self.sprite_textures.append(texture)

    def get_texture(self, index: int) -> Image:
        if index < 0 or index > len(self.sprite_textures):
            return None
        return self.sprite_textures[index]
