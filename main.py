import pygame
pygame.init()

WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH = 30
PADDLE_HEIGHT = 70


class Paddle():
    def __init__(self, x_start, y_start, width, height):
        self.x_start = x_start
        self.y_start = y_start 
        self.width = width
        self.height = height

    def draw_paddle(self):
        pygame.draw.rect(WINDOW, WHITE, pygame.Rect(self.x_start, self.y_start, self.width, self.height))

    #TO DO
    #draw
    #move
    #reset_position
    #pass
    #pygame.draw.rect

class Ball():
    pass 
    # pygame.draw.circle

class Draw():
    pass
    # bude vykreslovat vsetko
    # pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    while run:
        clock.tick(FPS)
        left_paddle.draw_paddle()
        right_paddle.draw_paddle()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        pygame.display.update()

    # V TOMTO BUDEM VYUZIVAT
    # pygame.key_pressed()
    # WINDOW.blit()

    
    pygame.quit()

if __name__ == '__main__':
    main()