import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 700, 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and ball dimensions
PADDLE_WIDTH = 30
PADDLE_HEIGHT = 70
BALL_RADIUS = 7

# Game settings
FPS = 60
WINNING_SCORE = 3
SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Paddle:
    """Class to represent a paddle"""

    def __init__(self, x, y, width, height, color=WHITE):
        self.x = self.x_start = x
        self.y = self.y_start = y
        self.width = width
        self.height = height
        self.color = color
        self.vel = 4

    def draw(self, window):
        """Draw the paddle on the screen"""
        pygame.draw.rect(window, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self, direction):
        """Move the paddle up or down"""
        if direction == "up" and self.y > 0:
            self.y -= self.vel
        elif direction == "down" and self.y + self.height < HEIGHT:
            self.y += self.vel

    def reset_to_starting_position(self):
        """Reset paddle position to starting position"""
        self.x = self.x_start
        self.y = self.y_start

class Ball:
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
        """Draw the ball on the screen"""
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        """Move the ball"""
        self.x += self.x_vel
        self.y += self.y_vel

    def reset_to_starting_position(self):
        """Reset ball position and velocity to starting values"""
        self.x = self.x_start
        self.y = self.y_start
        self.x_vel = random.choice([5, -5])
        self.y_vel = 0

class Game:
    """Class to manage the game"""

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
        self.left_score = 0
        self.right_score = 0

    def draw_scoreboard(self):
        """Draw the scoreboard on the screen"""
        left_score_text = SCORE_FONT.render(f"{self.left_score}", 1, WHITE)
        right_score_text = SCORE_FONT.render(f"{self.right_score}", 1, WHITE)
        self.window.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, (WIDTH * 3 // 4 - right_score_text.get_width() // 2, 20))

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def handle_key_input(self):
        """Handle key input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.left_paddle.move("up")
        if keys[pygame.K_s]:
            self.left_paddle.move("down")
        if keys[pygame.K_UP]:
            self.right_paddle.move("up")
        if keys[pygame.K_DOWN]:
            self.right_paddle.move("down")

    def handle_ball_collision(self):
        """Handle ball collision with paddles and screen edges"""
        if self.ball.y + self.ball.radius >= HEIGHT or self.ball.y - self.ball.radius <= 0:
            self.ball.y_vel *= -1

        if self.ball.x_vel < 0 and self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width:
            if self.ball.y >= self.left_paddle.y and self.ball.y <= self.left_paddle.y + self.left_paddle.height:
                self.ball.x_vel *= -1
                middle_y = self.left_paddle.y + self.left_paddle.height / 2
                difference_in_y = middle_y - self.ball.y
                reduction_factor = self.left_paddle.height / (2 * self.ball.max_vel)
                self.ball.y_vel = -difference_in_y / reduction_factor

        elif self.ball.x_vel > 0 and self.ball.x + self.ball.radius >= self.right_paddle.x:
            if self.ball.y >= self.right_paddle.y and self.ball.y <= self.right_paddle.y + self.right_paddle.height:
                self.ball.x_vel *= -1
                middle_y = self.right_paddle.y + self.right_paddle.height / 2
                difference_in_y = middle_y - self.ball.y
                reduction_factor = self.right_paddle.height / (2 * self.ball.max_vel)
                self.ball.y_vel = -difference_in_y / reduction_factor

    def update_game_state(self):
        """Update game state"""
        self.ball.move()
        self.handle_ball_collision()
        if self.ball.x < -20:
            self.right_paddle.reset_to_starting_position()
            self.left_paddle.reset_to_starting_position()
            self.ball.reset_to_starting_position()
            self.right_score += 1
        elif self.ball.x > WIDTH + 20:
            self.left_paddle.reset_to_starting_position()
            self.right_paddle.reset_to_starting_position()
            self.ball.reset_to_starting_position()
            self.left_score += 1

    def display_winner(self):
        """Display the winner of the game"""
        if self.left_score >= WINNING_SCORE:
            winner_text = "Left Player Won!"
        elif self.right_score >= WINNING_SCORE:
            winner_text = "Right Player Won!"
        else:
            return

        text = SCORE_FONT.render(winner_text, 1, WHITE)
        self.window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)
        self.left_score = 0
        self.right_score = 0

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.window.fill(BLACK)
            self.draw_scoreboard()
            self.left_paddle.draw(self.window)
            self.right_paddle.draw(self.window)
            self.ball.draw(self.window)
            pygame.display.update()

            running = self.handle_events()
            self.handle_key_input()
            self.update_game_state()
            self.display_winner()

            # Cap the frame rate
            self.clock.tick(FPS)

        # Quit pygame
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()