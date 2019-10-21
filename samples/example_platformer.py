
import logging
import orion_core
import arcade

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.DEBUG, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
logger.info("example application")

# window constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Orion Engine: platformer example"

# game constants
TILE_SIZE = 32
MOVE_SPEED = 110
JUMP_SPEED = 120
GRAVITY_SPEED = 100
SPRITESHEET = "assets_platformer/spritesheet.png"


class Player(object):

    def __init__(self, x: int, y: int, tile_size: int, textures):
        self.pos_x = x
        self.pos_y = y
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.dir_face_x = 0
        self.offset_x = tile_size // 2
        self.offset_y = tile_size // 2
        self.on_ground = False
        self.sprite = arcade.Sprite()
        for texture in textures:
            self.sprite.append_texture(texture)
        self.sprite.set_texture(0)

    def draw(self):
        self.sprite.center_x = self.pos_x
        self.sprite.center_y = self.pos_y
        if self.dir_face_x == 0:
            self.sprite.set_texture(1)
        else:
            self.sprite.set_texture(0)
        self.sprite.draw()


class Window(orion_core.Window):

    tile_set = []
    debug_points = []

    def __init__(self) -> None:
        """ Create the base window """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player = None
        self.map = None
        self.change_x = 0
        self.change_y = 0
        self.debug_color = orion_core.color.WARM_BLACK
        self.spritesheet = orion_core.Spritesheet(SPRITESHEET, TILE_SIZE)

    def init(self):
        """ generate the map from the level string and create a player object """

        level = ""
        level += "#.............................................................#B"
        level += "#.............................................................#B"
        level += "#.............................................................#B"
        level += "#...#############........##....##....##.......................#B"
        level += "#.............................................................#B"
        level += "#...............#........##..#..#..#..####....................#B"
        level += "#......................##.....................................#B"
        level += "#...###.#......#.....##...................#...................#B"
        level += "#...................###..................###..#....#..........#B"
        level += "GGGGGGGGGG.GGG.GGGGG###G..GGGGGGG..GGGGGGBBBGGBGGGGBGGGGGGGGGGBB"
        level += "BBB##..#####.###########G.####....GBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        level += "BBB#...#..................###....GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        level += "BBB#..##..#.################....GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        level += "BBB#...........................GBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        level += "BBBBGGGGGGGGGGGGGGGGGGGGGGGGGGGBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
        level += "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"

        textures = dict()
        textures['.'] = self.spritesheet.get_texture(3)
        textures['#'] = self.spritesheet.get_texture(2)
        textures['B'] = self.spritesheet.get_texture(1)
        textures['G'] = self.spritesheet.get_texture(0)

        self.map = orion_core.TileMap(64, 16, TILE_SIZE)
        self.map.load_texture_map(textures)
        self.map.parse_map_string(level)
        logger.debug("map generated")

        player_x, player_y = self.map.tile_to_world(32, 7)
        player_textures = [
            self.spritesheet.get_texture(4),
            self.spritesheet.get_texture(5)
            ]
        self.player = Player(player_x, player_y, TILE_SIZE, player_textures)

    def on_draw_frame(self) -> None:
        """ frame rendering details """

        self.map.draw()
        self.player.draw()

        for _ in range(len(self.debug_points)):
            x, y = self.debug_points.pop()
            arcade.draw_point(x, y, orion_core.color.YELLOW, 4)

    def on_update_frame(self, delta_time: float) -> None:
        """ Game logic update per frame """

        player = self.player
        cur_map = self.map

        # set gravity
        player.vel_y += -GRAVITY_SPEED * delta_time

        # create drag when on ground
        if player.on_ground:
            player.vel_x += -10.0 * player.vel_x * delta_time
            if abs(player.vel_x) < 0.05:
                player.vel_x = 0.0

        # check that speed is not unreasonable
        if self.player.on_ground:
            if self.player.vel_x > 200.0:
                self.player.vel_x = 200.0
            if self.player.vel_x < -200.0:
                self.player.vel_x = -200.0
        else:
            if self.player.vel_x > 80.0:
                self.player.vel_x = 80.0
            if self.player.vel_x < -80.0:
                self.player.vel_x = -80.0
        if self.player.vel_y > 400.0:
            self.player.vel_y = 400.0
        if self.player.vel_y < -400.0:
            self.player.vel_y = -400.0

        # get the new position
        new_pos_x = player.pos_x + player.vel_x * delta_time
        new_pos_y = player.pos_y + player.vel_y * delta_time

        # check for collisions
        if player.vel_x <= 0:  # moving left
            x1 = new_pos_x - player.offset_x
            y1 = new_pos_y - player.offset_y * 0.9
            x2 = new_pos_x - player.offset_x
            y2 = new_pos_y + player.offset_y * 0.9
            if cur_map.get_tile(x1, y1) != '.' or cur_map.get_tile(x2, y2) != '.':
                new_pos_x = int(player.pos_x)
                player.vel_x = 0

        else:  # moving right
            x1 = new_pos_x + player.offset_x
            y1 = new_pos_y - player.offset_y * 0.9
            x2 = new_pos_x + player.offset_x
            y2 = new_pos_y + player.offset_y * 0.9
            if cur_map.get_tile(x1, y1) != '.' or cur_map.get_tile(x2, y2) != '.':
                new_pos_x = int(player.pos_x)
                player.vel_x = 0

        player.on_ground = False
        if player.vel_y <= 0:  # moving down
            x1 = new_pos_x + player.offset_x * 0.9
            y1 = new_pos_y - player.offset_y
            x2 = new_pos_x - player.offset_x * 0.9
            y2 = new_pos_y - player.offset_y
            if cur_map.get_tile(x1, y1) != '.' or cur_map.get_tile(x2, y2) != '.':
                new_pos_y = int(player.pos_y)
                player.vel_y = 0
                player.on_ground = True

        else:  # moving up
            x1 = new_pos_x - player.offset_x * 0.9
            y1 = new_pos_y + player.offset_y
            x2 = new_pos_x + player.offset_x * 0.9
            y2 = new_pos_y + player.offset_y
            if cur_map.get_tile(x1, y1) != '.' or cur_map.get_tile(x2, y2) != '.':
                new_pos_y = int(player.pos_y)
                player.vel_y = 0

        # Apply movement to the character
        player.pos_x = new_pos_x
        player.pos_y = new_pos_y

        # check that the character is still on the map
        if player.pos_x < cur_map.tile_offset_x:
            player.pos_x = cur_map.tile_offset_x
        if player.pos_x + cur_map.tile_offset_x > cur_map.width:
            player.pos_x = cur_map.width - cur_map.tile_offset_x
        if player.pos_y < cur_map.tile_offset_y:
            player.pos_y = cur_map.tile_offset_y
        if player.pos_y + cur_map.tile_offset_y > cur_map.height:
            player.pos_y = cur_map.height - cur_map.tile_offset_y

        # make the camera follow the player
        self.camera_x = int(player.pos_x / 1)
        self.camera_y = int(player.pos_y / 1)

        # keep the camera clamped to the map
        if self.camera_x < self.camera_offset_x:
            self.camera_x = self.camera_offset_x
        if self.camera_x + self.camera_offset_x > cur_map.width:
            self.camera_x = cur_map.width - self.camera_offset_x
        if self.camera_y < self.camera_offset_y:
            self.camera_y = self.camera_offset_y
        if self.camera_y + self.camera_offset_y > cur_map.height:
            self.camera_y = cur_map.height - self.camera_offset_y

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """ Key press handling """
        super().on_key_press(key, key_modifiers)

        if key == orion_core.key.LEFT:
            self.player.dir_face_x = 0
            if self.player.on_ground:
                self.player.vel_x += -MOVE_SPEED
            else:
                self.player.vel_x += -MOVE_SPEED // 4
        elif key == orion_core.key.RIGHT:
            self.player.dir_face_x = 1
            if self.player.on_ground:
                self.player.vel_x += MOVE_SPEED
            else:
                self.player.vel_x += MOVE_SPEED // 4
        elif key == orion_core.key.UP:
            self.player.vel_y = MOVE_SPEED // 2
        elif key == orion_core.key.DOWN:
            self.player.vel_y = -MOVE_SPEED // 2
        elif key == orion_core.key.SPACE:
            if self.player.vel_y == 0:
                self.player.vel_y = JUMP_SPEED


if __name__ == '__main__':
    orion_core.init()
    _window = Window()
    _window.init()
    orion_core.run()

