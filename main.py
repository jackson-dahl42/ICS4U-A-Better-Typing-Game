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

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def move(self, new_rect):
        self.rect = new_rect

    def adjacent_tiles_words(self, grid):
        adjacent_words = []
        for tile in grid:
            if tile == self:
                continue
            if abs(tile.rect.centerx - self.rect.centerx) <= TILE_SIZE and abs(tile.rect.centery - self.rect.centery) <= TILE_SIZE:
                adjacent_words.append((tile.word, tile.rect))
        return adjacent_words

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

grid = []
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = col * TILE_SIZE + 50
        y = row * TILE_SIZE + 50
        word = words[row * GRID_WIDTH + col]
        tile = Tile(x, y, TILE_SIZE, TILE_SIZE, word)
        grid.append(tile)

player = Player(50, 50)

def main():
    
    input_string = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Input:", input_string)
                    adjacent_words = player.adjacent_tiles_words(grid)
                    for word, rect in adjacent_words:
                        if input_string == word:
                            player.move(rect)
                            break
                    input_string = "" 
                elif event.key in range(32, 127): 
                    input_string += event.unicode

        screen.fill(WHITE) 
        for tile in grid:
            tile.draw(screen)

        player.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
