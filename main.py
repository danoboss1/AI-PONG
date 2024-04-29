# https://youtu.be/2f6TmKm7yx0?si=xgi_o5pVxgS4ieH2
# INSPIRATION VIDEO FROM TECH WITH TIM

# NEXT STEP : CREATE NEW FILE WITH NEW GAME CLASS WHERE PLAYER WILL BE LEFT PADDLE, AI RIGHT PADDLE
# skratka, aby to nejako kvalitne fungovalo a inspiruj sa z toho videa

import pygame
import random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 500

# Paddle and ball settings
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 70
BALL_RADIUS = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings 
FPS = 60
WINNING_SCORE = 2
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
SCORE_FONT_HITS = pygame.font.SysFont("comicsans", 20)


class Paddle():
    """Class to represent a paddle"""

    def __init__(self, x, y, width, height, color=WHITE):
        self.x = self.x_start = x
        self.y = self.y_start = y
        self.width = width
        self.height = height 
        self.color = color
        self.vel = 4

    def draw(self, window):
        pygame.draw.rect(window, self.color, pygame.Rect((self.x, self.y, self.width, self.height)))

    def move(self, direction):
        if direction == "up" and self.y > 0:
            self.y -= self.vel
        elif direction == "down" and self.y + self.height < HEIGHT:
            self.y += self.vel

    def reset_to_starting_position(self):
        self.x = self.x_start
        self.y = self.y_start 

class Ball():
    """Class to represent the ball"""

    def __init__(self, x, y, radius, color=WHITE):
        self.x = self.x_start = x
        self.y = self.y_start = y 
        self.radius = radius
        self.color = color
        self.max_vel = 5
        self.x_vel = random.choice([5, -5])
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset_to_starting_position(self):
        self.x = self.x_start
        self.y = self.y_start
        self.x_vel = random.choice([5, -5])
        self.y_vel = 0

class Game():
    """Class that handle the PONG game"""

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("AI PONG")
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

    def draw_scoreboard(self):
        """Draw the scoreboard on the screen"""
        left_score_text = SCORE_FONT.render(f"{self.left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{self.right_score}", 1, WHITE)
        self.window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    def draw_hits(self):
        """Draw number of hits of each paddle"""
        left_hits_text = SCORE_FONT_HITS.render(f"{self.left_hits}", 1, WHITE)
        right_hits_text = SCORE_FONT_HITS.render(F"{self.right_hits}", 1, WHITE)
        self.window.blit(left_hits_text, (WIDTH // 8 - left_hits_text.get_width() // 2, 20))
        self.window.blit(right_hits_text, (WIDTH * 7 // 8 - right_hits_text.get_width() // 2, 20))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def handle_key_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move("up")
        elif keys[pygame.K_s]:
            self.left_paddle.move("down")
        elif keys[pygame.K_UP]:
            self.right_paddle.move("up")
        elif keys[pygame.K_DOWN]:
            self.right_paddle.move("down")

    def handle_ball_collision(self):
        if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1

        if self.ball.x_vel < 0 and self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                self.ball.x_vel *= -1
                middle_y = self.left_paddle.y + self.left_paddle.height / 2
                difference_in_y = middle_y - self.ball.y
                reduction_factor = self.left_paddle.height / (2 * self.ball.max_vel)
                self.ball.y_vel = -difference_in_y / reduction_factor
                # pocitanie dotykov laveho padla s loptou
                self.left_hits += 1

        if self.ball.x_vel > 0 and self.ball.x + self.ball.radius >= self.right_paddle.x:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                self.ball.x_vel *= -1
                middle_y = self.right_paddle.y + self.right_paddle.height / 2
                difference_in_y = middle_y - self.ball.y
                reduction_factor = self.right_paddle.height / (2 * self.ball.max_vel)
                self.ball.y_vel = -difference_in_y / reduction_factor
                self.right_hits += 1

    def update_game_state(self):
        self.ball.move()
        self.handle_ball_collision()
        if self.ball.x < -20:
            self.left_paddle.reset_to_starting_position()
            self.right_paddle.reset_to_starting_position()
            self.ball.reset_to_starting_position()
            self.right_score += 1
            # resetovanie left a right hitov
            self.left_hits = 0
            self.right_hits = 0
        elif self.ball.x > WIDTH + 20:
            self.left_paddle.reset_to_starting_position()
            self.right_paddle.reset_to_starting_position()
            self.ball.reset_to_starting_position()
            self.left_score += 1
            # resetovanie left a right hitov
            self.left_hits = 0
            self.right_hits = 0

    def display_winner(self):
        if self.left_score >= WINNING_SCORE:
            winner_text = "Left Player Won"
        elif self.right_score >= WINNING_SCORE:
            winner_text = "Right Player Won"
        else:
            return
        
        text = SCORE_FONT.render(winner_text, 1, WHITE)
        self.window.blit(text, (WIDTH // 2  - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)
        self.left_score = 0
        self.right_score = 0
        
   
    def run(self):
        # main
        running = True
        while running:
            self.window.fill(BLACK)
            self.draw_scoreboard()
            self.draw_hits()
            self.left_paddle.draw(self.window)
            self.right_paddle.draw(self.window)
            self.ball.draw(self.window)
            pygame.display.update()

            running = self.handle_events()
            self.handle_key_input()
            self.update_game_state()
            self.display_winner()

            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()