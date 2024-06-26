import pygame
import random
import asyncio

async def main():
    pygame.init()

    WIDTH = 400
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Game settings
    GRAVITY = 0.2
    JUMP_STRENGTH = -5
    PIPE_SPEED = 1

    class Bird:
        def __init__(self, x, y, color, is_ai=False):
            self.x = x
            self.y = y
            self.velocity = 0
            self.color = color
            self.rect = pygame.Rect(x, y, 30, 30)
            self.is_ai = is_ai

        def jump(self):
            self.velocity = JUMP_STRENGTH

        def update(self):
            self.velocity += GRAVITY
            self.y += self.velocity
            self.rect.y = int(self.y)

        def draw(self):
            pygame.draw.rect(screen, self.color, self.rect)

        def reset(self, y):
            self.y = y
            self.velocity = 0
            self.rect.y = int(self.y)

        def decide_jump(self, pipes):
            if not pipes:
                return

            next_pipe = pipes[0]
            if self.x < next_pipe.x + next_pipe.width:
                if self.y > next_pipe.top + 20 and self.y < next_pipe.bottom - 50:
                    if self.velocity > 0:
                        self.jump()
                elif self.y > next_pipe.bottom - 50:
                    self.jump()
            else:
                next_pipe = pipes[1] if len(pipes) > 1 else pipes[0]
                if self.y > next_pipe.top + 20:
                    self.jump()

    class Pipe:
        def __init__(self, x):
            self.x = x
            self.gap = 200
            self.top = random.randint(50, HEIGHT - 50 - self.gap)
            self.bottom = self.top + self.gap
            self.width = 50
            self.color = GREEN
            self.passed = False

        def update(self):
            self.x -= PIPE_SPEED

        def draw(self):
            pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top))
            pygame.draw.rect(screen, self.color, (self.x, self.bottom, self.width, HEIGHT - self.bottom))

    player = Bird(50, HEIGHT // 2, RED)
    ai_birds = [Bird(100, HEIGHT // 2, BLUE, True), Bird(150, HEIGHT // 2, WHITE, True)]
    pipes = [Pipe(WIDTH), Pipe(WIDTH + WIDTH // 2)]
    score = 0
    font = pygame.font.Font(None, 36)

    def reset_game():
        nonlocal player, ai_birds, pipes, score
        player.reset(HEIGHT // 2)
        for ai_bird in ai_birds:
            ai_bird.reset(HEIGHT // 2)
        pipes = [Pipe(WIDTH), Pipe(WIDTH + WIDTH // 2)]
        score = 0

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        reset_game()
                        game_over = False
                    else:
                        player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                if game_over:
                    reset_game()
                    game_over = False
                else:
                    player.jump()

        if not game_over:
            player.update()
            for ai_bird in ai_birds:
                ai_bird.update()
                ai_bird.decide_jump(pipes)

            for pipe in pipes:
                pipe.update()

            if pipes[-1].x < WIDTH - WIDTH // 2:
                pipes.append(Pipe(WIDTH))

            if pipes and pipes[0].x < -50:
                pipes.pop(0)

            for pipe in pipes:
                if player.rect.colliderect(pygame.Rect(pipe.x, 0, pipe.width, pipe.top)) or \
                   player.rect.colliderect(pygame.Rect(pipe.x, pipe.bottom, pipe.width, HEIGHT - pipe.bottom)):
                    game_over = True

                if not pipe.passed and pipe.x < player.x:
                    pipe.passed = True
                    score += 1

            if player.y < 0 or player.y > HEIGHT:
                game_over = True

            # Remove AI birds that collide or go out of bounds
            ai_birds = [bird for bird in ai_birds if not (
                any(bird.rect.colliderect(pygame.Rect(pipe.x, 0, pipe.width, pipe.top)) or
                    bird.rect.colliderect(pygame.Rect(pipe.x, pipe.bottom, pipe.width, HEIGHT - pipe.bottom))
                    for pipe in pipes) or bird.y < 0 or bird.y > HEIGHT
            )]

        screen.fill(BLACK)
        for pipe in pipes:
            pipe.draw()
        player.draw()
        for ai_bird in ai_birds:
            ai_bird.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render("Game Over", True, WHITE)
            restart_text = font.render("Tap or Press SPACE to Restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
