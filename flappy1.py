import pygame
import random

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 30
BIRD_HEIGHT = 30
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_VELOCITY = 3

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.Surface((BIRD_WIDTH, BIRD_HEIGHT))
bird_image.fill(BLUE)

# Function to draw the bird
def draw_bird(bird_rect):
    screen.blit(bird_image, bird_rect)

# Function to create a new pipe
def create_pipe():
    height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_rect = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return top_rect, bottom_rect

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe[0].x -= PIPE_VELOCITY
        pipe[1].x -= PIPE_VELOCITY
    pipes = [pipe for pipe in pipes if pipe[0].x > -PIPE_WIDTH]
    return pipes

# Function to detect collisions
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

# Main game loop
def main():
    bird_rect = pygame.Rect(50, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
    bird_velocity = 0
    pipes = []
    score = 0
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    running = True

    while running:
        screen.fill(WHITE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH

        # Update bird position
        bird_velocity += GRAVITY
        bird_rect.y += bird_velocity

        # Create new pipes
        if len(pipes) == 0 or pipes[-1][0].x < SCREEN_WIDTH - 200:
            pipes.append(create_pipe())

        # Move pipes
        pipes = move_pipes(pipes)

        # Check for collisions
        if check_collision(bird_rect, pipes):
            running = False

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe[0])
            pygame.draw.rect(screen, GREEN, pipe[1])

        # Draw bird
        draw_bird(bird_rect)

        # Update the score
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.update()
        clock.tick(60)

    # Game Over
    game_over_text = font.render("Game Over", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)

    pygame.quit()

if __name__ == "__main__":
    main()


