import pygame
from src.game.tetris import TetrisGame
from src.ui.menus import MainMenu

def main():
    pygame.init()
    game = TetrisGame()
    menu = MainMenu(game)
    menu.run()

if __name__ == "__main__":
    main()