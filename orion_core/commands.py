
import arcade
import logging

logger = logging.getLogger(__name__)


def set_camera(left: int, right: int, bottom: int, top: int) -> None:
    arcade.set_viewport(left, right, bottom, top)

