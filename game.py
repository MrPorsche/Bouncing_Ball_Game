import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 20
PLATFORM_WIDTH, PLATFORM_HEIGHT = 100, 10
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)  # Light blue color for the level indicator

# Initializes the Pygame library
pygame.init()

# Creating a screen for the Game
# Creates the game window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))

# Sets the title of the game window.
pygame.display.set_caption("Bouncing Ball Game")

# Initializes a font object for rendering text
font = pygame.font.Font(None, 36)

# Creates a clock object to control the frame rate.
clock = pygame.time.Clock()

# Initializing game variables
# Starting position of the ball at the center of the screen
ball_pos = [WIDTH // 2, HEIGHT // 2]

# Starting speed of the ball with random values
ball_speed = [random.uniform(2, 4), random.uniform(2, 4)] # Faster starting speed

# Starting position of the platform
platform_pos = [WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - PLATFORM_HEIGHT - 10]

# Starting platform moves speed
platform_speed = 10

# Player's score
score = 0

# Number of lives the player has
lives = 3

# Current level of the game
current_level = 1

# Color of the platform.
platform_color = ORANGE

# Fullscreen toggle function

def toggle_fullscreen():
    # Toggles between fullscreen and windowed mode
    global screen, WIDTH, HEIGHT
    if screen.get_flags() & pygame.FULLSCREEN:
        screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
    else:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Functions for screens

def start_screen():
    # Clearing the screen with a black background using..,
    screen.fill(BLACK)
    # Displaying Game title
    show_text_on_screen("Bouncing Ball Game", 50, HEIGHT // 4)
    show_text_on_screen("Press any key to start...", 30, HEIGHT // 3)
    show_text_on_screen("Move the platform with arrow keys...", 30, HEIGHT // 2)
    # Flips the display to make the changes visible with..,
    pygame.display.flip()
    # Waiting for a key press before proceeding
    wait_for_key()

def game_over_screen():
    # Clearing the screen with a black background using..,
    screen.fill(BLACK)
    # Displays the game over message, the final score, and instructions for restarting.
    show_text_on_screen("Game Over", 50, HEIGHT // 3)
    show_text_on_screen(f"Your final score: {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to restart...", 20, HEIGHT * 2 // 3)
    # Flips the display
    pygame.display.flip()
    # Waiting for a key press before proceeding
    wait_for_key()

def victory_screen():
    # Clearing the screen with a black background using..,
    screen.fill(BLACK)
    # Displays a congratulatory message, the final score, and instructions for exiting.
    show_text_on_screen("Congratulations!", 50, HEIGHT // 3)
    show_text_on_screen(f"You've won with a score of {score}", 30, HEIGHT // 2)
    show_text_on_screen("Press any key to exit...", 20, HEIGHT * 2 // 3)
    # Flips the display
    pygame.display.flip()
    # Waiting for a key press before proceeding
    wait_for_key()

def wait_for_key():
    # Waits for either a quit event (closing the game window) or a key press event.

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # If the event is quitting, it exits the game using..,
                pygame.quit()
                sys.exit()
                # If the event is a key press, it breaks out of the waiting loop.
            elif event.type == pygame.KEYDOWN:
                waiting = False

# Renders text on the screen with the specified font size and Y position.
def show_text_on_screen(text, font_size, y_position):
    # Creating a font object using pygame.font.Font.
    font = pygame.font.Font(None, font_size)
    # Renders the text onto a surface with the specified color (white in this case)
    text_render = font.render(text, True, WHITE)
    # Positions the text in the center of the screen at the specified Y position.
    text_rect = text_render.get_rect(center=(WIDTH // 2, y_position))
    # Blits (draws) the text onto the game screen
    screen.blit(text_render, text_rect)

# Returns a random RGB color for changing the platform color.
def change_platform_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# These functions handle different aspects of the game screens, user
# interactions, and display of text. They contribute to the overall
# structure and user experience of the game.


# Main game loop

# displaying the initial screen with instruction
start_screen()
# Setting TRUE to initiate the main game loop
game_running = True

while game_running:

    # Event Handling:

    # Checking for events using pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Setting FALSE to exit the loop when quit event detected (Game Window closes)
            game_running = False
    
    # Reading the state of the arrow keys using..,
    keys = pygame.key.get_pressed()

    # Platform Movment:

    # Adjusting the platform position based on arrow key inputs
    
    platform_pos[0] += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * platform_speed

    # Ensure the platform stays within the screen boundaries
    platform_pos[0] = max(0, min(platform_pos[0], WIDTH - PLATFORM_WIDTH))
    platform_pos[1] = max(0, min(platform_pos[1], HEIGHT - PLATFORM_HEIGHT))

    # Ball Movement and Bouncing:

    # Updating the ball's position based on its speed
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Implements bouncing off the walls by reversing the speed when reaching the screen edges
    if ball_pos[0] <= 0 or ball_pos[0] >= WIDTH:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= 0:
        ball_speed[1] = -ball_speed[1]
    
    # Collision Detection:
        
    # Check if the Ball hits the platform
    
    if (
        platform_pos[0] <= ball_pos[0] <= platform_pos[0] + PLATFORM_WIDTH
        and platform_pos[1] - BALL_RADIUS <= ball_pos[1] <= platform_pos[1] + PLATFORM_HEIGHT
    ):
        # If a collision occurs, the ball's vertical speed is reversed, and the player scores a point
        ball_speed[1] = -ball_speed[1]
        score += 1
    
    # Level Progression:

    # Checks if the player has scored enough points to advance to the next level
    if score >= current_level * 10:
        # If so, increments the level, resets the ball's position, randomizes its speed, and changes the platform color
        current_level += 1
        ball_pos = [random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)]
        ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]  # Randomize the ball speed
        platform_color = change_platform_color()
    
    # Checking for Game Over:

    # Monitors if the ball falls off the screen
    if ball_pos[1] >= HEIGHT:
        # Decreases the number of lives if the ball is below the screen
        lives -= 1
        if lives == 0:
            # If lives run out, displays the game over screen, restarts the game, and resets score, lives, and level
            game_over_screen()
            start_screen() # Restart the game after game over
            score = 0
            lives = 3
            current_level = 1
        else:
            # Reset the ball position
            ball_pos = [WIDTH // 2, HEIGHT // 2]
            # Randomize the ball speed
            ball_speed = [random.uniform(2, 4), random.uniform(2, 4)]
    
    # Screen Rendering:

    # Clearing the screen with a black background
    screen.fill(BLACK)

    # Draws the ball and platform on the screen
    # The Ball
    pygame.draw.circle(screen, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # The platform
    pygame.draw.rect(screen, platform_color, (int(platform_pos[0]), int(platform_pos[1]), PLATFORM_WIDTH, PLATFORM_HEIGHT))

    # Displays score, level, and lives information in rectangles with specific colors
    info_line_y = 10 # Adjusting the vertical position
    info_spacing = 75 # Adjusting the spacing

    # Draw the score in an orange rectangle at the top left
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(10, info_line_y))
    pygame.draw.rect(screen, ORANGE, score_rect.inflate(10, 5))
    screen.blit(score_text, score_rect)

    # Draw the level indicator in a light-blue rectangle at the top left (next to the score)
    level_text = font.render(f"Level: {current_level}", True, WHITE)
    level_rect = level_text.get_rect(topleft=(score_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, LIGHT_BLUE, level_rect.inflate(10, 5))
    screen.blit(level_text, level_rect)

    # Draw the lives in a red rectangle at the top left (next to the level)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topleft=(level_rect.topright[0] + info_spacing, info_line_y))
    pygame.draw.rect(screen, RED, lives_rect.inflate(10, 5))
    screen.blit(lives_text, lives_rect)

    # Display Update and Frame Rate Control:
    pygame.display.flip()

    clock.tick(FPS)

# Game Termination:
# Exits PyGame and terminates the program when the main loop is exited
pygame.quit()

# This structure ensures continuous gameplay, handling user input, updating
# game state, and providing visual feedback to the player

# Conclusion

# The start_screen() function clears the screen with a black background, displays
# the game title and instructions, flips the display for visibility, and waits for
# a key press using wait_for_key().

# The game_over_screen() function clears the screen with a black background, displays
# the game over message, final score, and restart instructions, flips the display, and
# waits for a key press with wait_for_key().

# The victory_screen() function clears the screen with a black background, displays a
# congratulatory message, final score, and exit instructions, flips the display, and
# waits for a key press with wait_for_key().

# The wait_for_key() function waits for either a quit event (closing the game window)
# or a key press event. It exits the game if quitting, and breaks out of the waiting
# loop if a key is pressed.

# The show_text_on_screen(text, font_size, y_position) function renders text on the
# screen with specified attributes, utilizes the pygame.font.Font class for creating
# a font object, and positions and draws the text in the center of the screen.

# And the change_platform_color() function returns a random RGB color for changing the
# platform color.