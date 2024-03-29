# tile map generation

import logging
import arcade

logger = logging.getLogger(__name__)


class TileMap(object):

    map_string = ""
    texture_map = {}

    def __init__(self, width, height, tile_size):
        self.width = width * tile_size
        self.height = height * tile_size
        self.tile_width = width
        self.tile_height = height
        self.tile_size = tile_size
        self.tile_offset_x = self.tile_size // 2
        self.tile_offset_y = self.tile_size // 2
        self.map_sprite_tiles = arcade.SpriteList()

    def load_texture_map(self, textures: dict) -> None:
        self.texture_map = textures

    def parse_map_string(self, map_string) -> None:
        self.map_string = map_string

        for y in range(self.tile_height):
            for x in range(self.tile_width):
                c = map_string[y * self.tile_width + x]
                sprite = arcade.Sprite()
                if c not in self.texture_map:
                    continue
                sprite.append_texture(self.texture_map[c])
                sprite.set_texture(0)
                sprite.center_x = self.tile_size * x + self.tile_offset_x
                sprite.center_y = self.height - self.tile_size * y - self.tile_offset_y
                self.map_sprite_tiles.append(sprite)

    def draw(self) -> None:
        self.map_sprite_tiles.draw()

    def tile_to_world(self, tile_x: int, tile_y: int) -> (int, int):
        world_x = self.tile_size * tile_x + self.tile_offset_x
        world_y = self.height - self.tile_size * tile_y - self.tile_offset_y
        return world_x, world_y

    def world_to_tile(self, world_x: int, world_y: int) -> (int, int):
        tile_x = world_x // self.tile_size
        tile_y = (self.height - world_y) // self.tile_size
        return tile_x, tile_y

    def get_tile_type(self, tile_x: int, tile_y: int) -> str:
        return self.map_string[int(tile_y) * self.tile_width + int(tile_x)]

    def get_tile(self, world_x: int, world_y: int) -> str:
        tile_x, tile_y = self.world_to_tile(world_x, world_y)
        return self.get_tile_type(tile_x, tile_y)

    def get_tile_center(self, world_x: int, world_y: int) -> (int, int):
        tile_x, tile_y = self.world_to_tile(world_x, world_y)
        cx = self.tile_size * tile_x + self.tile_offset_x
        cy = self.tile_size * tile_y + self.tile_offset_y
        return cx, cy

