"""Interactive chess game."""


import arcade

from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
)
from views import WelcomeView


def main():
    """Main method."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    welcome = WelcomeView()
    window.show_view(welcome)
    arcade.run()


if __name__ == "__main__":
    main()
