import pygame
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooter')

# Load player spaceship image
spaceship_image = pygame.image.load('spaceship.png')
spaceship_image = pygame.transform.scale(spaceship_image, (50, 50))  # Scale to desired size

# Load opponent spaceship image and scale to larger size
opponent_image = pygame.image.load('opponent.jpeg')
opponent_image = pygame.transform.scale(opponent_image, (40, 40))  # Larger size
opponent_image_red = pygame.Surface((40, 40))
opponent_image_red.fill((255, 0, 0))  # Red color

# Load bullet fire sound effect
bullet_fire_sound = pygame.mixer.Sound('bullet_fire.mp3')

# Load missile fire sound effect
missile_fire_sound = pygame.mixer.Sound('missile_fire.mp3')

# Load opponent bullet fire sound effect
opponent_bullet_fire_sound = pygame.mixer.Sound('opponent_bullet_fire.mp3')

# Spaceship attributes
spaceship_width, spaceship_height = spaceship_image.get_size()
opponent_width, opponent_height = opponent_image.get_size()

# Player attributes
player_x, player_y = (screen_width - spaceship_width) // 2, screen_height - spaceship_height - 20
player_speed = 5

# Bullet attributes
bullet_width, bullet_height = 5, 10
bullet_color = (255, 255, 0)  # Yellow color
player_bullets = []
bullet_speed = 1

# Missile attributes
missile_width, missile_height = 15, 30
missile_color = (255, 0, 0)  # Red color
player_missiles = []
missile_speed = 3
missile_delay = 200  # 200ms delay between missile shots
last_missile_shot_time = 0

# Explosion attributes
explosions = []
explosion_duration = 500  # Explosion duration in millisecondss

# Shooting delay
shoot_delay = 50  # 100ms delay between shots
last_player_shot_time = 0

# Opponent bullet attributes
opponent_bullet_color = (255, 0, 255)  # Magenta color
opponent_bullet_speed = 1  # Slower bullet speed (changed from 2 to 1)
opponents = []

# Increased opponent shoot delay
opponent_shoot_delay = 250  # 500ms delay between opponent shots

# Limit the number of opponents
max_opponents = 20

# Zigzag movement variables
zigzag_speed = 0.5  # Slow speed
zigzag_change_interval = 50  # Change direction every 50 frames

# Player health
player_health = 100  # Initial health
max_health = 100  # Maximum health

# Player score
score = 0  # Initial score

# Shield attributes
shield_active = False
shield_duration = 5000  # 5000ms = 5 seconds
shield_start_time = 0

# Font for score display
font = pygame.font.SysFont(None, 36)

# Function to draw the player health bar
def draw_health_bar(surface, x, y, health):
    # Calculate health bar dimensions
    bar_length = 100
    bar_height = 10
    fill = (health / max_health) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)

    # Draw health bar
    pygame.draw.rect(surface, (0, 255, 0), fill_rect)
    pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)

# Function to draw the player score
def draw_score(surface, score):
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    surface.blit(score_text, (screen_width - 150, 10))

# Function to spawn a single opponent
def spawn_opponent():
    x = random.randint(0, screen_width - opponent_width)
    y = random.randint(0, screen_height // 2)
    zigzag_direction = random.choice([-1, 1])
    opponents.append({'x': x, 'y': y, 'bullets': [], 'last_shot_time': 0, 'zigzag_direction': zigzag_direction, 'zigzag_counter': 0, 'hit': False, 'hit_time': 0})

# Function to handle missile explosion
def explode_missile(missile):
    explosion_time = pygame.time.get_ticks()
    explosions.append({'x': missile[0], 'y': missile[1], 'start_time': explosion_time})

# Function to display game over message
def display_game_over(screen):
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before quitting

# Function to draw a button
def draw_button(surface, text, x, y, width, height, color, font_color):
    pygame.draw.rect(surface, color, (x, y, width, height))
    font = pygame.font.SysFont(None, 48)
    text_surf = font.render(text, True, font_color)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    surface.blit(text_surf, text_rect)

# Main menu function
def main_menu():
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if screen_width // 2 - 100 < mouse_x < screen_width // 2 + 100 and screen_height // 2 - 50 < mouse_y < screen_height // 2 + 50:
                    menu_running = False

        screen.fill((0, 0, 0))  # Fill with black color
        draw_button(screen, "Play", screen_width // 2 - 100, screen_height // 2 - 50, 200, 100, (0, 255, 0), (0, 0, 0))
        pygame.display.flip()

# Function to pause the game
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    paused = False

# Function to resume the game
def resume_game():
    global paused
    paused = False

# Main menu before starting the game
main_menu()

# Game loop
running = True
paused = False  # Game starts running
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Pause the game when 'P' key is pressed
    keys = pygame.key.get_pressed()
    if keys[K_p]:
        pause_game()
    elif keys[K_r]:
        resume_game()

    # Game logic runs only if not paused
    if not paused:
        # Get keys pressed for movement
        player_movement_x = 0
        player_movement_y = 0

        if keys[K_LEFT] or keys[K_a]:
            player_movement_x = -player_speed
        if keys[K_RIGHT] or keys[K_d]:
            player_movement_x = player_speed
        if keys[K_UP] or keys[K_w]:
            player_movement_y = -player_speed
        if keys[K_DOWN] or keys[K_s]:
            player_movement_y = player_speed

        # Update player position
        player_x += player_movement_x
        player_y += player_movement_y

        # Continuous shooting logic for bullets
        current_time = pygame.time.get_ticks()
        if keys[K_SPACE]:
            if current_time - last_player_shot_time > shoot_delay:
                player_bullets.append((player_x + spaceship_width // 2 - bullet_width // 2, player_y))
                bullet_fire_sound.play()  # Play the bullet fire sound
                last_player_shot_time = current_time

        # Continuous shooting logic for missiles
        if keys[K_x]:
            if current_time - last_missile_shot_time > missile_delay:
                player_missiles.append((player_x + spaceship_width // 2 - missile_width // 2, player_y))
                missile_fire_sound.play()  # Play the missile fire sound
                last_missile_shot_time = current_time

        # Shield activation logic
        if keys[K_z]:
            if not shield_active:
                shield_active = True
                shield_start_time = pygame.time.get_ticks()

        # Deactivate shield after duration
        if shield_active and current_time - shield_start_time > shield_duration:
            shield_active = False

        # Update player bullet positions
        player_bullets = [(x, y - bullet_speed) for x, y in player_bullets if y > 0]

        # Update player missile positions and check for explosions
        new_missiles = []
        for missile in player_missiles:
            x, y = missile
            if y <= 0:
                explode_missile(missile)
            else:
                new_missiles.append((x, y - missile_speed))
        player_missiles = new_missiles

        # Opponent movement and shooting logic
        for opponent in opponents:
            # Zigzag movement logic
            if opponent['x'] <= 0 or opponent['x'] >= screen_width - opponent_width:
                opponent['zigzag_direction'] *= -1
            opponent['x'] += opponent['zigzag_direction'] * zigzag_speed

            # Opponent shooting logic
            current_time = pygame.time.get_ticks()
            if current_time - opponent['last_shot_time'] > opponent_shoot_delay and random.random() < 0.01:  # Reduced probability for shooting
                opponent['bullets'].append((opponent['x'] + opponent_width // 2 - bullet_width // 2, opponent['y'] + opponent_height))
                opponent_bullet_fire_sound.play()  # Play the opponent bullet fire sound
                opponent['last_shot_time'] = current_time

            # Update opponent bullet positions
            opponent['bullets'] = [(x, y + opponent_bullet_speed) for x, y in opponent['bullets'] if y < screen_height]

            # Check for collisions with opponent bullets hitting player
            for bullet in opponent['bullets']:
                if (player_x < bullet[0] < player_x + spaceship_width and
                        player_y < bullet[1] < player_y + spaceship_height):
                    opponent['bullets'].remove(bullet)
                    if not shield_active:  # Only decrease health if shield is not active
                        player_health -= 5  # Decrease player health by 5 for each bullet hit
                        print("Player hit by opponent bullet!")
                        if player_health <= 0:
                            running = False  # Game over if player health is zero
                    break

            # Check for collisions with opponent spaceships hitting player
            if (opponent['x'] < player_x + spaceship_width and
                    opponent['x'] + opponent_width > player_x and
                    opponent['y'] < player_y + spaceship_height and
                    opponent['y'] + opponent_height > player_y):
                if not shield_active:  # Only decrease health if shield is not active
                    player_health -= 10  # Decrease player health by 10
                    print("Player hit by opponent!")
                    if player_health <= 0:
                        running = False  # Game over if player health is zero
                break

            # Check for collisions with player bullets hitting opponents
            for bullet in player_bullets:
                if (opponent['x'] < bullet[0] < opponent['x'] + opponent_width and
                        opponent['y'] < bullet[1] < opponent['y'] + opponent_height):
                    player_bullets.remove(bullet)
                    opponent['hit'] = True
                    opponent['hit_time'] = current_time
                    score += 10  # Increase score by 10 for hitting an opponent
                    print("Opponent hit by player!")
                    break

            # Check for collisions with player missiles hitting opponents
            for missile in player_missiles:
                if (opponent['x'] < missile[0] < opponent['x'] + opponent_width and
                        opponent['y'] < missile[1] < opponent['y'] + opponent_height):
                    player_missiles.remove(missile)
                    explode_missile(missile)
                    opponent['hit'] = True
                    opponent['hit_time'] = current_time
                    score += 20  # Increase score by 20 for hitting an opponent with a missile
                    print("Opponent hit by player missile!")
                    break

        # Boundaries for the player
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - spaceship_width:
            player_x = screen_width - spaceship_width
        if player_y < 0:
            player_y = 0
        elif player_y > screen_height - spaceship_height:
            player_y = screen_height - spaceship_height

        # Clear the screen
        screen.fill((0, 0, 0))  # Fill with black color

        # Draw player spaceship (image instead of rectangle)
        screen.blit(spaceship_image, (player_x, player_y))

        # Draw shield if active
        if shield_active:
            pygame.draw.circle(screen, (0, 0, 255), (player_x + spaceship_width // 2, player_y + spaceship_height // 2), 60, 2)

        # Draw opponent spaceships (image instead of rectangle)
        current_time = pygame.time.get_ticks()
        for opponent in opponents:
            if opponent['hit']:
                if current_time - opponent['hit_time'] < explosion_duration:
                    screen.blit(opponent_image_red, (opponent['x'], opponent['y']))
                else:
                    opponents.remove(opponent)
            else:
                screen.blit(opponent_image, (opponent['x'], opponent['y']))

        # Draw player bullets
        for bullet in player_bullets:
            pygame.draw.rect(screen, bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

        # Draw player missiles
        for missile in player_missiles:
            pygame.draw.rect(screen, missile_color, (missile[0], missile[1], missile_width, missile_height))

        # Draw opponent bullets
        for opponent in opponents:
            for bullet in opponent['bullets']:
                pygame.draw.rect(screen, opponent_bullet_color, (bullet[0], bullet[1], bullet_width, bullet_height))

        # Draw explosions
        new_explosions = []
        for explosion in explosions:
            if current_time - explosion['start_time'] < explosion_duration:
                radius = (current_time - explosion['start_time']) // 5
                pygame.draw.circle(screen, (255, 165, 0), (explosion['x'], explosion['y']), radius)
                new_explosions.append(explosion)
        explosions = new_explosions

        # Draw player health bar
        draw_health_bar(screen, 10, 10, player_health)

        # Draw player score
        draw_score(screen, score)

        # Update the display
        pygame.display.flip()

        # Spawn a new opponent if there are 4less than the maximum number
        if len(opponents) < max_opponents:
            spawn_opponent()

    # Display game over message if health is zero
    if player_health <= 0:
        display_game_over(screen)

# Quit Pygame
pygame.quit()

