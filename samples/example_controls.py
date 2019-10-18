
import logging
import orion_core
import arcade

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.DEBUG,
                    datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
logger.info("example keyboard controls application ")

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Orion Engine: ball example"
MOVEMENT_SPEED = 3.0


class Ball(object):

    def __init__(self, position_x=100.0, position_y=100.0,
                 change_x=0.0, change_y=0.0,
                 radius=15, color=arcade.color.RED):
        self.position_x = position_x
        self.position_y = position_y
        self.change_x = change_x
        self.change_y = change_y
        self.radius = radius
        self.color = color

    def draw(self):
        arcade.draw_circle_filled(self.position_x, self.position_y, self.radius, self.color)

    def update(self):
        # update the position
        self.position_y += self.change_y
        self.position_x += self.change_x

        # check it is still on screen
        if self.position_y < self.radius:
            self.position_y = self.radius

        if self.position_x < self.radius:
            self.position_x = self.radius

        if self.position_x > _window.width - self.radius:
            self.position_x = _window.width - self.radius

        if self.position_y > _window.height - self.radius:
            self.position_y = _window.height - self.radius


class Window(orion_core.Window):

    def __init__(self) -> None:
        """ Create the base window """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # create a ball
        self.ball = Ball()

    def on_draw_frame(self) -> None:
        """ frame rendering details """
        self.ball.draw()

    def on_update_frame(self, delta_time: float) -> None:
        """ game logic update per frame """
        self.ball.update()

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """ key press handling """
        super().on_key_press(key, key_modifiers)

        if key == arcade.key.LEFT:
            self.ball.change_x = -MOVEMENT_SPEED

        if key == arcade.key.RIGHT:
            self.ball.change_x = MOVEMENT_SPEED

        if key == arcade.key.UP:
            self.ball.change_y = MOVEMENT_SPEED

        if key == arcade.key.DOWN:
            self.ball.change_y = -MOVEMENT_SPEED

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """ key press handling """
        super().on_key_release(key, key_modifiers)

        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ball.change_x = 0

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ball.change_y = 0


if __name__ == '__main__':
    orion_core.init()
    _window = Window()
    orion_core.run()

