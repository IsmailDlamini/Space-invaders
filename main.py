import pygame
import random
from pygame import mixer


# initiate pygame module
pygame.init()
pygame.mixer.pre_init(4410, -16, 2, 512)

# defining screen variables
HEIGHT = 750
WIDTH = 600

# set the screen size
window = pygame.display.set_mode((WIDTH, HEIGHT))
# set the caption to be shown on the window
pygame.display.set_caption("SpaceInvaders by ismail")

# define all picture variables
bg = pygame.image.load("assets/background1.jpg")
# change size of image
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

player = pygame.image.load("assets/space-invaders.png")
player = pygame.transform.scale(player, (100, 100))

stone1 = pygame.image.load("assets/cave-painting (1).png")

bullet = pygame.image.load("assets/bullet.png")
bullet = pygame.transform.scale(bullet, (40, 40))

exp_sequence = [pygame.image.load("assets/exp1.png"), pygame.image.load("assets/exp2.png"), pygame.image.load("assets/exp3.png"), pygame.image.load("assets/exp4.png"), pygame.image.load("assets/exp5.png")]
master_ship = pygame.image.load("assets/master-ship.png")

master_ship = pygame.transform.scale(master_ship, (600, 100))
instruction = pygame.image.load("assets/My project-2.png")

# sound effects and music

#shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
#mixer.music.load("sounds/mixkit-space-game-668.mp3")
#mixer.music.play(-1)


# all game variables

start_posY = 0
FPS = 60
clock = pygame.time.Clock()
enemies = []
wave = 5
stone_vel = 0
bullet_state = "ready"
name = "ismail"
live = []
live_count = 5
points = 0
marquee_move1 = 300
marquee_move2 = 600
level = 0
current_time = 0
level_change_time = 0
image_count = 1
explosion_count = 1
life_width = 200
press_count = 0
angle = 180
started = False
changed_level = False
game_over = False
high_score = 0
font = "freesansbold.ttf"

# player class


class Player:
    def __init__(self, x, y, velX, velY, image):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.image = image

    def show(self):

        window.blit(self.image, (self.x - 50//2, self.y))

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

# meteor class


class Stone:
    def __init__(self, x, y, vel_Y):
        self.x = x
        self.y = y
        self.vel_Y = vel_Y

    def draw(self):
        window.blit(stone1, (self.x, self.y))


class Bullet:
    def __init__(self, x, y, state):
        self.x = x
        self.y = y
        self.state = state

    def position(self):

        window.blit(bullet, (self.x, self.y))

# define player and bullet objects


main_player = Player(300 - player.get_width()//2 + 20, 480, 10, 10, player)
bullet1 = Bullet(main_player.x + 3, 500, "ready")


def background():
    window.fill("black")
    window.blit(bg, (0, start_posY))


def move_background():

    background()

    global start_posY

    window.blit(bg, (0, - HEIGHT + start_posY))

    if start_posY == HEIGHT:  # if the position of the background picture
        window.blit(bg, (0, HEIGHT - start_posY))
        start_posY = 0

    start_posY += 1


def draw_enemy():

    for enemy1 in enemies:
        Stone.draw(enemy1)

# shoot


def fire(x, y):

    bullet1.state = "fire"
    window.blit(bullet, (x, y))


def health_bar():

    pygame.draw.rect(window, "red", (390, 5, 200, 30))
    pygame.draw.rect(window, "green", (390, 5, life_width, 30))


def marquee():  # this function creates the moving words at the bottom of the screen

    marquee_font = pygame.font.Font("freesansbold.ttf", 30)
    pygame.draw.rect(window, "white", (0,   HEIGHT - 30, 600, 30))

    credit1 = marquee_font.render("created by Ismail || ", False, "black")
    window.blit(credit1, (marquee_move1, HEIGHT - 28))

    credit2 = marquee_font.render("The cyber-ghost", False, "black")
    window.blit(credit2, (marquee_move2, HEIGHT - 28))

    pygame.draw.rect(window, "white", (300, HEIGHT - 30, 300, 30))


def move_marquee():  # this function moves the words created at the bottom of the screen by the  function above

    global marquee_move2, marquee_move1

    marquee_move1 -= 1
    marquee_move2 -= 1
    if marquee_move1 < -300:  # if the words are off the screen
        marquee_move1 = 400  # reset the position of the x value to the shown value
    if marquee_move2 < -300:
        marquee_move2 = marquee_move1 + 300  #


def level_change_text():  # shows a text on the screen everytime the level changes (e.g. LEVEL 2)

    level_change_font = pygame.font.Font("freesansbold.ttf", 60)
    show_level = level_change_font.render(f"Level {level}", False, "white")
    window.blit(show_level, (300 - show_level.get_width()/2, 300))


def show_explosion(x, y):  # does what the function name says
    global explosion_count

    for a in range(1, 4):
        explosion_count += 1

        window.blit(exp_sequence[explosion_count], (x, y))
        explosion_count += 1

        if explosion_count > 4:
            explosion_count = 1


def data_collection(data):

    # open a file and write the points in  a file closing the file at the end

    points_file = open("game data/points.txt", "a")
    points_file.write(f"{data}")
    points_file.close()


def intro():

    intro_message1 = "welcome to Space War by cyber-games"
    intro_message2 = "your task is to protect the main ship"
    intro_message3 = "press SPACE to start"

    intro_show1 = game_font.render(intro_message1, False, "white")
    intro_show2 = game_font.render(intro_message2, False, "white")
    intro_show3 = game_font.render(intro_message3, False, "white")

    window.blit(intro_show1, (300 - intro_show1.get_width()/2, 200))
    window.blit(intro_show2, (300 - intro_show2.get_width()/2, 230))
    window.blit(intro_show3, (300 - intro_show3.get_width() / 2, 260))


def game_over_texts():

    global game_over

    game_over_font = pygame.font.Font("freesansbold.ttf", 60)

    game_over_text = game_over_font.render("Game over", False, "white")
    window.blit(game_over_text, ((300 - game_over_text.get_width()//2), 300))
    exit_font = pygame.font.Font("freesansbold.ttf", 40)
    exit_text = exit_font.render("press 'e' to exit game", False, "red")
    points_font = pygame.font.Font("freesansbold.ttf", 30)
    points_text = points_font.render(f"Points:{points}", False, "white")

    window.blit(exit_text, ((300 - exit_text.get_width()//2), 400))
    window.blit(points_text, ((300 - points_text.get_width()//2), 490))


def test():
    pass

running = True

while running:

    clock.tick(FPS)

    game_font = pygame.font.SysFont('system', 40)
    start_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    if not game_over:

        if key[pygame.K_LEFT]:
            if main_player.x > 30:
                Player.move_left(main_player)
                if bullet1.state == "ready":
                    bullet1.x -= 5

        if key[pygame.K_RIGHT]:
            if main_player.x < 525:
                Player.move_right(main_player)
                if bullet1.state == "ready":
                    bullet1.x += 5

    if not game_over:
        move_background()

    window.blit(master_ship, (300 - master_ship.get_width()//2, 680))

    if started:
        Bullet.position(bullet1)
        Player.show(main_player)
        pygame.draw.line(window, "red", (main_player.x + 25, main_player.y + 95), (300, 690))

    if started and not game_over:

        if len(enemies) == 0:

            wave += 2
            stone_vel += 9
            level += 1
            changed_level = True

            if len(enemies) == 0:
                for i in range(wave):
                    stone = Stone(random.randint(0, 540), random.randint(-1000, -100), 5)
                    enemies.append(stone)

    if not game_over:
        draw_enemy()

    if not game_over:
        for enemy in enemies:
            enemy.y += 2

    for enemy in enemies:
        if enemy.y > 650:
            enemies.remove(enemy)

            show_explosion(enemy.x, enemy.y)
            life_width -= 10

            if points > 0:
                points -= 5

    if key[pygame.K_SPACE] and not game_over:
        press_count = 1

        if press_count > 0:
            bullet1.state = "fire"
        started = True

        for enemy in enemies:
            if enemy.y > 0:
                pass
                #shoot_sound.play()

    if bullet1.state == "fire":
        fire(bullet1.x, bullet1.y)
        bullet1.y -= 15

        # if the bullet goes off the screen
        if bullet1.y < -10:
            bullet1.y = 500
            bullet1.x = main_player.x + 3
            bullet1.state = "ready"

    # handling events of collusion of bullet with the meteors
    for enemy in enemies:
        if enemy.x - 20 < bullet1.x < enemy.x + stone1.get_width() - 5:
            if enemy.y + stone1.get_height() - 5 > bullet1.y > enemy.y:

                show_explosion(bullet1.x - 20, bullet1.y - 50)
                bullet1.y = 500
                bullet1.x = main_player.x + 4
                enemies.remove(enemy)
                bullet1.state = "ready"
                points += 2

    health_bar()

    point = game_font.render(f"points: {points}", False, "white")
    window.blit(point, (5, 0))

    health_text = game_font.render("Health:", False, "white")
    window.blit(health_text, (275, 5))

    level_text = game_font.render(f"Level: {level}", False, 'white')
    window.blit(level_text, (5, 32))

    marquee()
    move_marquee()

    if not game_over:
        pass
       # pygame.mixer.music.play(-1)

    if not started:
        intro()
        window.blit(instruction, (300 - instruction.get_width()//2, 300))

    if changed_level:
        level_change_text()

    for enemy in enemies:
        if enemy.y > 50:
            changed_level = False

    # prevent points from being negative
    if points < 0:
        points -= points

    # if health goes to zero
    if life_width < 1:
        game_over = True
        game_over_texts()

    if key[pygame.K_e]:
        running = False

    pygame.display.update()
pygame.quit()


# Space invaders v0.1 by the critical thinker studios
# This game is freely available to the public
# "we declare variables not war"


