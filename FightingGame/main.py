import pygame
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting Game")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Characters variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load audio
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.3)

magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.3)

# Load images
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

warrior_sheet = pygame.image.load("assets/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/wizard/wizard.png").convert_alpha()

# Number of animation steps
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Load fonts
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
victory_font = pygame.font.Font("assets/fonts/turok.ttf", 60)

# Function of drawing text
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

# Function of drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Function of drawing health bar
def draw_health_bar(health, x, y, player):
    ratio = health / 100
    if player == 1:
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))
    else:
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x + 400 - (400 * ratio), y, 400 * ratio, 30))

# Instances of fighters
fighter1 = Fighter(1,200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
fighter2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Main game loop
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    draw_health_bar(fighter1.health, 20, 20, 1)
    draw_health_bar(fighter2.health, 580, 20, 2)

    # Draw actual score
    draw_text(str(score[0]) + ":" + str(score[1]), score_font, RED, (SCREEN_WIDTH / 2) - 15, 12)

    # Game countdown
    if intro_count <= 0:
        fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter2, round_over)
        fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter1, round_over)
    else:
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    # Update fighters
    fighter1.update()
    fighter2.update()

    # Draw fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    # Check if round is over
    if round_over == False:
        if fighter1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()


    # Check if one of players win 2 rounds or round is over
    else:
        if score[0] == 2:
            draw_text("Player 1 wins!", victory_font, RED, 325, 100)
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                score[0] = 0
                score[1] = 0
        elif score[1] == 2:
            draw_text("Player 2 wins!", victory_font, RED, 325, 100)
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                fighter1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                fighter2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)
                score[0] = 0
                score[1] = 0
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            fighter2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


    # Quit the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update display
    pygame.display.update()

pygame.quit()