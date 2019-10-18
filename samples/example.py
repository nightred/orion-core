
import logging
import orion_core

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                    level=logging.DEBUG, datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)
logger.info("example application")


class Window(orion_core.Window):

    def __init__(self) -> None:
        """ Create the base window """
        super().__init__(640, 480, "Orion Engine")

    def on_draw_frame(self) -> None:
        """ frame rendering details """
        pass

    def on_update_frame(self, delta_time: float) -> None:
        """ game logic update per frame """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """ key press handling """
        super().on_key_press(key, key_modifiers)

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """ key release handling """
        super().on_key_release(key, key_modifiers)

    def on_mouse_motion(self, x: int, y: int, delta_x, delta_y) -> None:
        """ mouse movement handling """
        super().on_mouse_motion(x, y, delta_x, delta_y)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """ mouse button press handling """
        super().on_mouse_press(x, y, button, key_modifiers)


if __name__ == '__main__':
    orion_core.init()
    _window = Window()
    orion_core.run()

