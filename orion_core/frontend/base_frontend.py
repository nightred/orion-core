

import arcade
import logging
from orion_core.commands import set_camera

logger = logging.getLogger(__name__)


class Window(arcade.Window):

    mouse_x = 0
    mouse_y = 0
    camera_x = 0.0
    camera_y = 0.0
    camera_offset_x = 0
    camera_offset_y = 0

    fps = 0.0
    time_elapsed = 0.0

    debug_console = True
    debug_color = arcade.color.LIGHT_GRAY

    keys_down = {}
    key_repeat_delay = 0.2
    key_repeat_time = 0.05
    key_repeat_ignore = (arcade.key.RETURN,)

    def __init__(self, width: int, height: int, title: str) -> None:
        super().__init__(width, height, title, antialiasing=False)
        self.camera_offset_x = width // 2
        self.camera_offset_y = height // 2
        self.camera_x = self.camera_offset_x
        self.camera_y = self.camera_offset_y

    def on_draw(self) -> None:
        """
        render the screen
        """

        bottom = self.camera_y - self.camera_offset_y
        top = self.camera_y + self.camera_offset_y
        left = self.camera_x - self.camera_offset_x
        right = self.camera_x + self.camera_offset_x

        set_camera(left, right, bottom, top)

        # clear the screen
        arcade.start_render()
        arcade.set_background_color(arcade.color.BLACK)

        # draw the current frame
        self.on_draw_frame()

        # draw the debug text
        if self.debug_console:
            self.draw_debug(top, left)

    def on_draw_frame(self) -> None:
        """ override this function to draw the screen """
        pass

    def draw_debug(self, top: int, left: int) -> None:
        """ Default debug text handling """
        debug_text = "Time elapsed: {0:7.2f} \n".format(self.time_elapsed)
        debug_text += "FPS: {0:3.2f} \n".format(self.fps)
        debug_text += "Window ({0} x {1}) \n".format(self.width, self.height)
        debug_text += "Mouse Position ({0} x {1}) \n".format(self.mouse_x, self.mouse_y)
        debug_text += "Camera Position ({0} x {1}) \n".format(self.camera_x, self.camera_y)

        line_height = 14
        left_padding = left + 20
        line_y = top - 10 - line_height
        for line in debug_text.split("\n"):
            if not line:
                continue
            arcade.draw_text(text=line, start_x=left_padding, start_y=line_y,
                             color=self.debug_color, font_size=10,
                             anchor_x="left", anchor_y="bottom")
            line_y -= line_height

    def on_update(self, delta_time: float) -> None:
        """
        Call the tick handlers on_tick
        :param delta_time:
        """

        self.time_elapsed += delta_time
        self.fps = 1.0 / delta_time

        for key, t in sorted(self.keys_down.items()):
            t += delta_time
            while t > self.key_repeat_delay:
                t -= self.key_repeat_time
                self.on_key_press(key=key, key_modifiers=0)
            self.keys_down[key] = t

        self.on_update_frame(delta_time)

    def on_update_frame(self, delta_time: float) -> None:
        """
        override this function to add game logic for the frame
        :param delta_time:
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        called when a key is presses
        :param key:
        :param key_modifiers:
        """

        if key not in self.key_repeat_ignore:
            self.keys_down.setdefault(key, 0.0)

        if key == arcade.key.GRAVE:
            self.debug_console = not self.debug_console

    def on_key_release(self, key, key_modifiers):
        """
        called when released key press
        :param key:
        :param key_modifiers:
        """

        self.keys_down.pop(key, None)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        called when the mouse moves
        :param x:
        :param y:
        :param delta_x:
        :param delta_y:
        """
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        called when mouse button is pressed
        :param x:
        :param y:
        :param button:
        :param key_modifiers:
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        called on release of mouse button
        :param x:
        :param y:
        :param button:
        :param key_modifiers:
        """
        pass


def frontend_run():
    """
    We are using the arcade library for rendering
    Run the main arcade loop
    """
    arcade.run()
