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

BALL_RADIUS = 7


class Paddle():
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.x_start = x
        self.y = self.y_start = y 
        self.width = width
        self.height = height

    def draw_paddle(self):
        pygame.draw.rect(WINDOW, self.COLOR, pygame.Rect(self.x, self.y, self.width, self.height))

    def move_paddle(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL



    #TO DO
    #draw
    #move
    #reset_position
    #pass
    #pygame.draw.rect

class Ball():
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self):
        pygame.draw.circle(WINDOW, self.COLOR, (self.x, self.y), self.radius)

    def move (self):
        self.x += self.x_vel
        self.y += self.y_vel


class Draw():
    # bude vykreslovat vsetko

    def __init__(self, paddles, ball):
        self.paddles = paddles
        self.ball = ball

    def draw_objects(self):
        for paddle in self.paddles:
            paddle.draw_paddle()

        self.ball.draw()

    # pygame.display.update()
        
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # left paddle
    if ball.x_vel < 0:
        # ci je v tom padle na y-ovej osi
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    # right paddle
    else:
        if ball.y > right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            # tento riadok zabezpeci, ze to loptu odrazi aj ked nie je na obrazovke
            # a to neviem ci je ZIADUCE uplne, POZOR NA TO
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

def main():

    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)

    paddles = [left_paddle, right_paddle]

    drawer = Draw(paddles, ball)

    while run:
        clock.tick(FPS)

        WINDOW.fill(BLACK)

        drawer.draw_objects()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.y > 0:
            left_paddle.move_paddle(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.height < HEIGHT:
            left_paddle.move_paddle(up=False)

        if keys[pygame.K_UP] and right_paddle.y > 0:
            right_paddle.move_paddle(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height < HEIGHT:
            right_paddle.move_paddle(up=False)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        pygame.display.update()

    # V TOMTO BUDEM VYUZIVAT
    # pygame.key_pressed()
    # WINDOW.blit()

    
    pygame.quit()

if __name__ == '__main__':
    main()