import pygame
import random
import sys
import os
from Constantes import *
from Player import Player
from Enemy import Enemy
from Bullet import Bullet

# Initialize Pygame
pygame.init()

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Shooter")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 48)

# Load Images
def get_image_path(name):
    # Get the directory where main.py is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to find Imagenes folder
    return os.path.join(script_dir, "..", "Imagenes", name)

def load_image(name, width, height):
    path = get_image_path(name)
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (width, height))
    except pygame.error as e:
        print(f"Error loading image {name} at {path}: {e}")
        sys.exit()

def load_background():
    path = get_image_path("el-fondo-de-la-galaxia-de-estilo-fantasia.jpg")
    try:
        img = pygame.image.load(path).convert()
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except pygame.error as e:
        print(f"Error loading background at {path}: {e}")
        sys.exit()

def draw_text(surf, text, size, x, y, color=WHITE):
    font_obj = pygame.font.SysFont("Arial", size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def main():
    # Load Assets
    background_img = load_background()
    player_img = load_image("astronave.png", PLAYER_WIDTH, PLAYER_HEIGHT)
    enemy_img = load_image("meteorito.png", ENEMY_WIDTH, ENEMY_HEIGHT)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Create Player
    player = Player(player_img, all_sprites, bullets)
    all_sprites.add(player)

    # Game Variables
    score = 0
    start_time = pygame.time.get_ticks()
    running = True
    game_over = False

    # Game Loop
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000 # Seconds

        # Difficulty Scaling
        speed_multiplier = 1 + (elapsed_time / 20.0) 
        health_bonus = int(elapsed_time / 30.0)
        
        # Spawn Enemies
        if not game_over:
            if random.random() < 0.02 + (elapsed_time * 0.001): 
                enemy = Enemy(enemy_img, speed_multiplier, health_bonus)
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.shoot()
                if event.key == pygame.K_r and game_over:
                    # Reset Game
                    game_over = False
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    player = Player(player_img, all_sprites, bullets)
                    all_sprites.add(player)
                    score = 0
                    start_time = pygame.time.get_ticks()

        # Update
        if not game_over:
            all_sprites.update()

            # Check Bullet - Enemy Collisions
            hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
            for enemy, bullet_list in hits.items():
                enemy.health -= len(bullet_list)
                if enemy.health <= 0:
                    enemy.kill()
                    score += 10

            # Check Player - Enemy Collisions
            hits = pygame.sprite.spritecollide(player, enemies, True)
            for hit in hits:
                player.lives -= 1
                if player.lives <= 0:
                    game_over = True

        # Draw / Render
        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)

        # UI
        draw_text(screen, f"Score: {score}", 18, SCREEN_WIDTH / 2, 10)
        draw_text(screen, f"Lives: {player.lives}", 18, SCREEN_WIDTH - 60, 10)
        draw_text(screen, f"Time: {int(elapsed_time)}s", 18, 50, 10)

        if game_over:
            draw_text(screen, "GAME OVER", 48, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, RED)
            draw_text(screen, "Press R to Restart", 24, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WHITE)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
