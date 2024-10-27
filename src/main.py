from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
import time
import sys
import pathlib
from game import MineSweeper
from tile import *


def main(argv):
    
    if len(argv) == 2 or len(argv) > 4:
        print(f"Usage: python {argv[0]} <width> <height> [num_bombs]")
        exit()

    # Default values
    width = 30
    height = 16
    num_bombs = 99

    try:
        if len(argv) > 1:
            width = int(argv[1])
        if len(argv) > 2:
            height = int(argv[2])
        if len(argv) > 3:
            num_bombs = int(argv[3])
    except ValueError:
        print("Width, height and num_bombs must be integers")
        exit()
        
    if num_bombs > width * height:
        print("Number of bombs is too large compared to grid size.")
        exit()

    # Init
    pygame.init()
    
    # Set default tile size
    TILE_SIZE = 40
    
    # Get current directory
    CURR_DIR = str(pathlib.Path(__file__).resolve().parent)

    # Get monitor width and height to adapt tile size to fit if needed
    infoObject = pygame.display.Info()
    monitor_width, monitor_height = infoObject.current_w, infoObject.current_h
    
    # Adapt tile size if needed
    if width * TILE_SIZE > monitor_width or height * TILE_SIZE > monitor_height:
        TILE_SIZE = int(min(monitor_width // width, monitor_height // height) - TILE_SIZE / max(width, height))

    # load images
    images = [pygame.transform.scale(pygame.image.load(CURR_DIR + "/../assets/" + tile_image), (TILE_SIZE, TILE_SIZE))
            for tile_image in tile_images]
    
    # Create game screen
    screen = pygame.display.set_mode([width * TILE_SIZE, height * TILE_SIZE])
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(images[BOMB])
    
    display_info = {
        "screen": screen,
        "images": images,
        "tile_size": TILE_SIZE
    }
    
    game = MineSweeper(width, height, num_bombs, display_info)
    running = True

    # Game Loop
    while running:

        # Check for event
        for event in pygame.event.get():

            # Quit
            if event.type == pygame.QUIT:
                running = False

            # Keyboard events
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        running = False
                    case pygame.K_r:
                        game.restart()
                    case pygame.K_u:
                        print(f"flags: {game.flag_positions}")
                        print(f"hidden: {game.hidden_positions}")

            # Mouse down events
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                i, j = y // TILE_SIZE, x // TILE_SIZE

                # Left click
                if event.button == 1:

                    if game.get(i, j) == HIDDEN:
                        game.set(i, j, PRESSED)
                        game.single_press = (i, j)
                    elif game.get(i, j) in range(1, 9):
                        game.pressed_neighbours(i, j)
                    for i, j in game.pressed_positions:
                        game.set(i, j, PRESSED)

                # Right click
                elif event.button == 3:
                    if game.get(i, j) == HIDDEN:
                        game.set(i, j, FLAG)
                    elif game.get(i, j) == FLAG:
                        game.set(i, j, HIDDEN)
                        
            # Mouse up events
            if event.type == pygame.MOUSEBUTTONUP:

                if event.button == 3:
                    continue

                # Tile press
                if game.single_press:
                    i, j = game.single_press
                    over = game.reveal_tile(i, j)
                    if game.get(i, j) == BOMB:
                        game.lost_grid(i, j)
                    elif game.get(i, j) == EMPTY:
                        game.empty_patch(i, j)
                    game.single_press = None

                # Flag reveal
                game.reveal_pressed_neighours()
                
                # Check for win
                if game.check_win():
                    print("You win!")
                    game.over = True

        game.auto_finish()

        # Update display
        game.update_display()
        # for i in range(height):
        #     for j in range(width):
        #         screen.blit(images[game.get(i, j)], (j*TILE_SIZE, i*TILE_SIZE))

        # pygame.display.flip()

        if game.over:
            time.sleep(2)
            pygame.event.clear()
            game.restart()

    # Pygame Quit
    pygame.quit()


if __name__ == '__main__':
    main(sys.argv)
