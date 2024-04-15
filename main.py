import pygame
import sys
import random

pygame.init()
pygame.font.init()
pygame.font.get_fonts()
display_info = pygame.display.Info()
WIDTH, HEIGHT = 1000, 1000
TILE_SIZE = 100
GRID_WIDTH, GRID_HEIGHT = 8, 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 24)
grid = []
grid_width_pixels = GRID_WIDTH * TILE_SIZE
grid_height_pixels = GRID_HEIGHT * TILE_SIZE
grid_x_offset = (WIDTH - grid_width_pixels) // 2
grid_y_offset = (HEIGHT - grid_height_pixels) // 2

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
        self.rect = pygame.Rect(x + grid_x_offset, y + grid_y_offset, TILE_SIZE, TILE_SIZE)
        self.health = 100
        self.word = random.choice(words)
        self.enemies_killed = 0
        self.image = pygame.image.load("ship.png")
        self.invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 120


    def update(self):
      if self.invincible:
          self.invincibility_timer -= 1
          if self.invincibility_timer <= 0:
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
        surface.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 20)
        self.speed = 10

    def move(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, "red", self.rect)

def draw_player_word(word):
    text_surface = font.render(word, True, "black")
    text_rect = text_surface.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
    screen.blit(text_surface, text_rect)

class Enemy:
    def __init__(self, x, y, speed, direction):
        self.rect = pygame.Rect(x * TILE_SIZE + grid_x_offset, y * TILE_SIZE + grid_y_offset, TILE_SIZE, TILE_SIZE)
        self.speed = speed
        self.direction = direction
        self.image = pygame.image.load("bug_enemya.png")
      
    def move(self):
      if self.direction == "up":
          self.rect.y -= self.speed
          if self.rect.bottom < 0:
              self.rect.top = HEIGHT
      elif self.direction == "down":
          self.rect.y += self.speed
          if self.rect.top > HEIGHT:
              self.rect.bottom = 0
      elif self.direction == "left":
          self.rect.x -= self.speed
          if self.rect.right < 0:
              self.rect.left = WIDTH
      elif self.direction == "right":
          self.rect.x += self.speed
          if self.rect.left > WIDTH:
              self.rect.right = 0
            
    def draw(self, surface):
      if self.direction == "up":
          rotated_image = pygame.transform.rotate(self.image, 180)
      elif self.direction == "down":
          rotated_image = self.image
      elif self.direction == "left":
          rotated_image = pygame.transform.rotate(self.image, -90)
      elif self.direction == "right":
          rotated_image = pygame.transform.rotate(self.image, 90)
    
      rotated_rect = rotated_image.get_rect(center=self.rect.center)
      surface.blit(rotated_image, rotated_rect)

def check_collision(player, enemies, bullets):
    if player.invincible:
      return
    for enemy in enemies:
      if player.rect.colliderect(enemy.rect):
          player.health -= 10
          player.invincible = True
          player.invincibility_timer = player.invincibility_duration
          break
    for bullet in bullets:
      if bullet.rect.y < 0:
        bullets.remove(bullet)
        break
      for enemy in enemies:
        if bullet.rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            bullets.remove(bullet)
            player.enemies_killed += 1
            break
      
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
  enemies.append(Enemy(x, y, 5, direction))

  


for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = grid_x_offset + col * TILE_SIZE
        y = grid_y_offset + row * TILE_SIZE
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
        player.update()
        check_collision(player, enemies, bullets)
        screen.fill("grey")
        for tile in grid:
            tile.draw(screen)
        player.draw(screen)
        for enemy in enemies:
          enemy.draw(screen)
        draw_player_word(player.word)
        text_surface = font.render(str(player.health), True, "black")
        text_rect = pygame.Rect(10, 10, 100, 100)
        screen.blit(text_surface, text_rect)
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
