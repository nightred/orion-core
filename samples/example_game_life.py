
import logging
import orion_core
import arcade
import random

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.DEBUG, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
logger.info("example of conway's game life ")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Orion Engine: game of life"

CELL_SIZE = 10
CELLS_WIDTH = int(SCREEN_WIDTH / CELL_SIZE)
CELLS_HEIGHT = int(SCREEN_HEIGHT / CELL_SIZE)


class Window(orion_core.Window):

    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.selected_x = 0
        self.selected_y = 0

        self.sim_active = False

        logger.debug("setting the fields, width:{}, Height:{}".format(CELLS_WIDTH, CELLS_HEIGHT))
        self.active_field = [0] * (CELLS_WIDTH * CELLS_HEIGHT)
        self.change_field = [0] * (CELLS_WIDTH * CELLS_HEIGHT)

        self.sprites = arcade.SpriteList()
        cell_light = arcade.make_soft_square_texture(CELL_SIZE, orion_core.color.DARK_YELLOW, 255, 30)

        for y in range(CELLS_HEIGHT):
            for x in range(CELLS_WIDTH):
                sprite = arcade.Sprite()
                sprite.append_texture(cell_light)
                sprite.set_texture(0)
                sprite.center_x = CELL_SIZE * x + CELL_SIZE // 2
                sprite.center_y = SCREEN_HEIGHT - CELL_SIZE * y - CELL_SIZE // 2
                self.sprites.append(sprite)

    def on_draw_frame(self) -> None:

        for x in range(1, CELLS_WIDTH - 1):
            for y in range(1, CELLS_HEIGHT - 1):
                i = y * CELLS_WIDTH + x
                if self.change_field[i] == 1:
                    self.sprites[i].draw()

        out = ""
        out += "cell count {} \n".format(CELLS_WIDTH * CELLS_HEIGHT)
        out += "selected cell {}, {} \n".format(self.selected_x, self.selected_y)
        if self.sim_active:
            out += "sim active \n"
        else:
            out += "sim paused \n"

        line_height = 14
        padding = 20
        line_y = self.height - padding - line_height
        for line in out.split("\n"):
            if not line:
                continue
            arcade.draw_text(text=line,
                             start_x=self.width - padding, start_y=line_y,
                             color=orion_core.color.LIGHT_GRAY, font_size=10,
                             anchor_x="right", anchor_y="bottom")
            line_y -= line_height

    def on_update_frame(self, delta_time: float) -> None:

        if not self.sim_active:
            return

        def cell(xc: int, yc: int) -> int:
            return self.active_field[yc * CELLS_WIDTH + xc]

        for i in range(CELLS_WIDTH * CELLS_HEIGHT):
            self.active_field[i] = self.change_field[i]

        for x in range(1, CELLS_WIDTH - 1):
            for y in range(1, CELLS_HEIGHT - 1):
                neighbours = cell(x - 1, y - 1) + cell(x - 0, y - 1) + cell(x + 1, y - 1) + \
                             cell(x - 1, y + 0) + 0 + cell(x + 1, y + 0) + \
                             cell(x - 1, y + 1) + cell(x + 0, y + 1) + cell(x + 1, y + 1)

                i = y * CELLS_WIDTH + x
                if cell(x, y) == 1:
                    if neighbours == 2 or neighbours == 3:
                        self.change_field[i] = 1
                    else:
                        self.change_field[i] = 0
                elif neighbours == 3:
                    self.change_field[i] = 1

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        super().on_key_press(key, key_modifiers)

        if key == orion_core.key.KEY_1:
            self.board_clear()

        elif key == orion_core.key.KEY_2:
            self.board_random()

        elif key == orion_core.key.KEY_3:
            self.board_gun()

        elif key == orion_core.key.KEY_4:
            self.board_growth()

        elif key == orion_core.key.SPACE:
            self.sim_active = not self.sim_active

    def on_mouse_motion(self, x: int, y: int, delta_x, delta_y) -> None:
        super().on_mouse_motion(x, y, delta_x, delta_y)

        self.selected_x = x // CELL_SIZE
        self.selected_y = abs(y - SCREEN_HEIGHT) // CELL_SIZE

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        super().on_mouse_press(x, y, button, key_modifiers)

        if button == orion_core.MOUSE_BUTTON_LEFT:
            self.change_field[self.selected_y * CELLS_WIDTH + self.selected_x] = 1

    def board_clear(self) -> None:
        for x in range(1, CELLS_WIDTH - 1):
            for y in range(1, CELLS_HEIGHT - 1):
                i = y * CELLS_WIDTH + x
                self.change_field[i] = 0

    def board_random(self) -> None:
        for x in range(1, CELLS_WIDTH - 1):
            for y in range(1, CELLS_HEIGHT - 1):
                self.change_field[y * CELLS_WIDTH + x] = random.randint(0, 1)

    def board_gun(self) -> None:
        self.set( 5,  5, "........................#............")
        self.set( 5,  6, "......................#.#............")
        self.set( 5,  7, "............##......##............##.")
        self.set( 5,  8, "...........#...#....##............##.")
        self.set( 5,  9, "##........#.....#...##...............")
        self.set( 5, 10, "##........#...#.##....#.#............")
        self.set( 5, 11, "..........#.....#.......#............")
        self.set( 5, 12, "...........#...#.....................")
        self.set( 5, 13, "............##.......................")

    def board_growth(self) -> None:
        self.set(20, 20, "########.#####...###......#######.#####")

    def set(self, x: int, y: int, string: str) -> None:
        i = 0
        for v in string:
            if v == "#":
                self.change_field[y * CELLS_WIDTH + (x + i)] = 1
            i += 1


if __name__ == '__main__':
    orion_core.init()
    _window = Window()
    orion_core.run()



