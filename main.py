import pygame
import sys
import random
from player import Player
from enemy import FlyingEye, Goblin, Mushroom, Skeleton, EvilWizard

# Initialize Pygame
pygame.init()

# Screen Dimensions
TILE_SIZE = 16
GRID_SIZE = 44
MAP_WIDTH = TILE_SIZE * GRID_SIZE
MAP_HEIGHT = TILE_SIZE * GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load tile and map resources
DESERT_TILE = pygame.image.load('Sprites/Sprites_Environment/desert_tile.png')  # Replace 'desert_tile.png' with your desert tile image
DESERT_TILE = pygame.transform.scale(DESERT_TILE, (TILE_SIZE, TILE_SIZE))  # Resize tile to 16x16

# Set up display
screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
pygame.display.set_caption("SwarmShot by IIITA")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load Player
player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)

# Define Enemy Wave Data
waves = [
    {'enemies': [(FlyingEye, 10, 0.4),(Mushroom, 5, 1),(EvilWizard, 1, 1)], 'message': "Wave 1: 30 Flying Eyes!"},
    {'enemies': [(FlyingEye, 30, 0.5), (Goblin, 10, 2)], 'message': "Wave 2: 30 Flying Eyes, 10 Goblins!"},
    {'enemies': [(FlyingEye, 30, 0.6), (Goblin, 10, 1.5)], 'message': "Wave 3: 30 Flying Eyes, 10 Goblins!"},  # Add more waves as needed
    {'enemies': [(FlyingEye, 90, 0.2), (Goblin, 30, 0.5), (Mushroom, 20, 1), (Skeleton, 40, 3)], 'message': "Wave 12: 90 Flying Eyes, 30 Goblins, 20 Mushrooms, 40 Skeletons!"}
]

class WaveManager:
    def __init__(self):
        self.wave_index = 0
        self.enemies = []
        self.spawn_timer = 0
        self.wave_message = ""
        self.message_timer = 0 ########
        self.time_between_waves = 5  # Time in seconds between waves

    def start_wave(self):
        wave_data = waves[self.wave_index]
        self.enemies = []
        self.wave_message = wave_data['message']
        self.message_timer = pygame.time.get_ticks()  # Start timer for message display
        
        # Spawn enemies
        for enemy_type, count, spawn_rate in wave_data['enemies']:
            for _ in range(count):
                x = random.randint(0, GRID_SIZE - 1) * TILE_SIZE
                y = random.randint(0, GRID_SIZE - 1) * TILE_SIZE
                enemy = enemy_type(x, y)
                self.enemies.append(enemy)
                
                # Set spawn time
                enemy.spawn_rate = spawn_rate

    def update(self):
        if len(self.enemies) == 0:
            self.wave_index += 1
            if self.wave_index < len(waves):
                self.start_wave()
        
        # Handle enemy spawning
        for enemy in self.enemies:
            if enemy.spawn_rate:
                enemy.update(player)
                
    def draw(self, surface):
        # Draw all enemies
        for enemy in self.enemies:
            enemy.draw(surface)

# Initialize Wave Manager
wave_manager = WaveManager()

# Function to render a basic map
def render_map():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            screen.blit(DESERT_TILE, (x * TILE_SIZE, y * TILE_SIZE))

# Function to draw the health bar
def draw_health_bar(surface, x, y, health, max_health):
    bar_width = 200
    bar_height = 20
    fill = (health / max_health) * bar_width
    border_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, RED, border_rect, 2)

# Main game loop
def main():
    wave_manager.start_wave()  # Start the first wave
    player_health = player.health
    max_health = 100

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        player.update(keys)

        # Update wave manager
        wave_manager.update()

        # Check for health reduction here (after collision)
        player_health = player.health  # Update player health after enemies hit

        # Render everything
        screen.fill(WHITE)  # Optional fallback color
        render_map()
        player.draw(screen)
        wave_manager.draw(screen)  # Draw the enemies

        # Display wave message
        if pygame.time.get_ticks() - wave_manager.message_timer < 2000:
            font = pygame.font.Font(None, 36)
            text = font.render(wave_manager.wave_message, True, WHITE)
            screen.blit(text, (MAP_WIDTH // 2 - text.get_width() // 2, MAP_HEIGHT // 2 - text.get_height() // 2))

        # Draw health bardd
        draw_health_bar(screen, 10, 10, player_health, max_health)

        # Check player health and display game over if health is 0
        if player_health <= 0:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (MAP_WIDTH // 2 - game_over_text.get_width() // 2, MAP_HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main()
