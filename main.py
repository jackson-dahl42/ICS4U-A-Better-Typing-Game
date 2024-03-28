import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

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
        
        pygame.display.flip()  

if __name__ == "__main__":
    main()
