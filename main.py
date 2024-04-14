import pygame
import sys
import random

pygame.init()
pygame.font.init()
pygame.font.get_fonts()
display_info = pygame.display.Info()
WIDTH, HEIGHT = display_info.current_w, display_info.current_h
TILE_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 8, 8
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
font = pygame.font.SysFont(None, 24)

words = [
    "cat", "dog", "bat", "fly", "pig", "cow", "ant", "frog", 
    "snake", "bird", "hawk", "wolf", "lion", "zebra", "horse", "fish", 
    "shark", "panda", "bear", "ape", "worm", "sheep", "goat", "tiger", 
    "fox", "bunny", "elk", "bee", "eel", "owl", "hen", "rat", 
    "emu", "gnu", "koi", "doe", "ewe", "yak", "bug", "cod", 
    "boa", "polar", "twister", "tree", "ball", "cake", "candy", "air",
    "net", "rod", "ore", "tail", "meat", "egg", "fire", "ice"
    "boat", "zen", "rot", "flame", "with", "out", "top", "tide", "fling",
    "like", "love", "hate", "sad", "mad", "joy", "joyful", "joyous",
    "lily", "leaf", "flower", "blooms",
    "rock", "stone", "grass", "gravel", "dirt", "earth", "soil", "ground"
]

class Tile:
    def __init__(self, x, y, width, height, word):
        self.rect = pygame.Rect(x, y, width, height)
        self.word = word

    def draw(self, surface):
        pygame.draw.rect(surface, "black", self.rect, 2)
        text_surface = font.render(self.word, True, "black")
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.health = 100
        self.word = random.choice(words)
        self.enemies_killed = 0
        self.invincible = False

    def move(self, new_rect, grid):
        previous_tile = None
        for tile in grid:
            if tile.rect == self.rect:
                previous_tile = tile
                break
        if previous_tile:
            unused_words = [word for word in words if word not in [tile.word for tile in grid]]
            if unused_words:
                new_word = random.choice(unused_words)
                previous_tile.word = new_word
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
        pygame.draw.rect(surface, "red", self.rect)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 20)
        self.speed = 5

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, "green", self.rect)

def draw_player_word(word):
    text_surface = font.render(word, True, "black")
    text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    screen.blit(text_surface, text_rect)

class Enemy:
    def __init__(self, x, y, speed, direction):
        self.rect = pygame.Rect(x * TILE_SIZE + 50, y * TILE_SIZE + 50, TILE_SIZE, TILE_SIZE)
        self.speed = speed
        self.direction = direction

    def move(self):
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, "black", self.rect)

def check_collision(player, enemies, bullets):
    for enemy in enemies:
      if player.rect.colliderect(enemy.rect):
        player.health -= 10
    for bullet in bullets:
      if bullet.rect.y < 0:
        bullets.remove(bullet)
      for enemy in enemies:
        if bullet.rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            bullets.remove(bullet)
            player.enemies_killed += 1
      
def spawn_enemy(enemies, grid):
  side = random.choice(["left", "right", "top", "bottom"])
  if side == "left":
      x = 0
      y = random.randint(0, GRID_HEIGHT - 1)
      direction = "right"
  elif side == "right":
      x = GRID_WIDTH - 1
      y = random.randint(0, GRID_HEIGHT - 1)
      direction = "left"
  elif side == "top":
      x = random.randint(0, GRID_WIDTH - 1)
      y = 0
      direction = "down"
  elif side == "bottom":
      x = random.randint(0, GRID_WIDTH - 1)
      y = GRID_HEIGHT - 1
      direction = "up"
  enemies.append(Enemy(x, y, 1, direction))

  
grid = []
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = col * TILE_SIZE + 50
        y = row * TILE_SIZE + 50
        word = words[row * GRID_WIDTH + col]
        tile = Tile(x, y, TILE_SIZE, TILE_SIZE, word)
        grid.append(tile)

player = Player(50, 50)
enemies = []
bullets = []

def main():
    input_string = ""
    clock = pygame.time.Clock()

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
                            player.move(rect, grid)
                        if input_string == player.word:
                            bullets.append(Bullet(player.rect.centerx - 5, player.rect.y))
                            break
                    input_string = ""
                elif event.key in range(32, 127):
                    input_string += event.unicode

        for bullet in bullets:
            bullet.move()
        for enemy in enemies:
          enemy.move()
        check_collision(player, enemies, bullets)

        screen.fill("white")
        for tile in grid:
            tile.draw(screen)

        player.draw(screen)
        for enemy in enemies:
          enemy.draw(screen)
        draw_player_word(player.word)
        for bullet in bullets:
            bullet.draw(screen)

        pygame.display.flip()
        if len(enemies) < 5:
          spawn_enemy(enemies, grid)
        if player.health <= 0:
            print("Game Over")
            #pygame.quit()
        clock.tick(60)  # Limit to 60 frames per second

if __name__ == "__main__":
    main()
