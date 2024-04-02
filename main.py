import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
TILE_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 5, 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

words = [
    "cat", "dog", "bat", "fly", "pig", "cow", "ant", "frog", "snake", "bird", "hawk", "wolf", "lion", "zebra", "horse", "fish", "shark", "panda", "bear", "ape", "worm", "sheep", "goat", "tiger", "fox", "bunny"
]

class Tile:
    def __init__(self, x, y, width, height, word):
        self.rect = pygame.Rect(x, y, width, height)
        self.word = word

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font.render(self.word, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

grid = []
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = col * TILE_SIZE + 50
        y = row * TILE_SIZE + 50
        word = words[row * GRID_WIDTH + col]
        tile = Tile(x, y, TILE_SIZE, TILE_SIZE, word)
        grid.append(tile)

def main():
    
    input_string = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  
                    print("Input:" + input_string)
                    input_string = ""  
                else:
                    input_string += pygame.key.name(event.key)  
        
        screen.fill(WHITE)

        for tile in grid:
            tile.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()
