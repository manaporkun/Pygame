import pygame
import time
import random

pygame.init()
width = 800
height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Car Game")
clock = pygame.time.Clock()

sound_score1 = pygame.mixer.Sound("piano1.wav")
sound_score2 = pygame.mixer.Sound("piano2.wav")
sound_score3 = pygame.mixer.Sound("piano3.wav")
sound_score4 = pygame.mixer.Sound("piano4.wav")
sound_gameover = pygame.mixer.Sound("gameover.flac")

car_width = 55
car_height = 108


def car(x, y):
    car_img = pygame.image.load('car.png')
    gameDisplay.blit(car_img, (x, y))


def thing1(thing_x, thing_y, thing_w, thing_h, thing_color):
    pygame.draw.rect(gameDisplay, thing_color, [thing_x, thing_y, thing_w, thing_h])


def thing2(thing_x, thing_y, thing_w, thing_h, thing_color):
    pygame.draw.rect(gameDisplay, thing_color, [thing_x, thing_y, thing_w, thing_h])


def text_objects(text, font, color):
    text_surface = font.render(str(text), True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, position, size):
    large_text = pygame.font.Font(None, size)
    text_surf, text_rect = text_objects(text, large_text, white)
    text_rect.center = position
    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()


def crash(score):
    message_display("Game Over", ((width * 0.5), (height * 0.2)), 60)
    message_display("SCORE: " + str(score), ((width * 0.5), (height * 0.4)), 30)
    sound_gameover.play()
    time.sleep(2)
    run()


def sound(decision):
    if decision == 0:
        sound_score1.play()
    elif decision == 1:
        sound_score2.play()


def run():
    score = 0
    car_x = (width * 0.45)
    car_y = (height * 0.8)
    car_x_change = 0
    car_y_change = 0

    thing_speed = 6

    thing1_start_x = random.randrange(0, width)
    thing1_start_y = 0
    thing1_width = random.randrange(50, 200)
    thing1_height = 10

    thing2_start_x = -100
    thing2_start_y = -100
    thing2_width = 10
    thing2_height = random.randrange(50, 200)

    if score > 4:
        thing2_start_x = 0
        thing2_start_y = random.randrange(0, height)

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    car_x_change = -7
                if event.key == pygame.K_d:
                    car_x_change = 7
                if event.key == pygame.K_w:
                    car_y_change = -7
                if event.key == pygame.K_s:
                    car_y_change = 7

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    car_x_change = 0
                if event.key == pygame.K_s or event.key == pygame.K_w:
                    car_y_change = 0

        if score < 15 or score > 17:
            car_x += car_x_change
            car_y += car_y_change
        else:
            message_display("KEYS ARE CHANGED", (width / 2, height - 50), 50)
            car_x -= car_x_change
            car_y -= car_y_change

        gameDisplay.fill(black)

        block_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))

        thing1(thing1_start_x, thing1_start_y, thing1_width, thing1_height, block_color)
        thing1_start_y += thing_speed
        thing1_start_x += (thing_speed * [-1, 1][random.randrange(2)])

        if score > 4:
            thing2(thing2_start_x, thing2_start_y, thing2_width, thing2_height, block_color)
            thing2_start_x += thing_speed
            thing2_start_y += (thing_speed * [-1, 1][random.randrange(2)])

        if score == 5:
            thing_speed = 5
            sound_score3.play()

        if score == 10:
            thing_speed = 6
            sound_score4.play()

        car(car_x, car_y)

        if car_x > width:
            car_x = -50
        if car_x + car_width < 0:
            car_x = width - 10
        if car_y > height:
            car_y = 5 - car_height
        if car_y + car_height < 0:
            car_y = height - 5

        if thing1_start_y > height:
            thing1_width = random.randrange(50, 200)
            thing1_start_y = 0
            thing1_start_x = random.randrange(0, width)
            score += 1
            thing_speed += 0.05
            sound(random.randrange(2))

        if thing2_start_x > width:
            thing2_height = random.randrange(50, 200)
            thing2_start_y = random.randrange(0, height)
            thing2_start_x = 0
            score += 1
            thing_speed += 0.05
            sound(random.randrange(2))

        if car_x <= thing1_start_x <= car_width + car_x or car_x <= thing1_start_x + thing1_width <= car_x + car_width:
            if car_y <= thing1_start_y <= car_height + car_y \
                    or car_y <= thing1_start_y + thing1_height <= car_y + car_height:
                crash(score)

        if thing1_start_x <= car_x <= thing1_start_x + thing1_width \
                or thing1_start_x <= car_x + car_width <= thing1_start_x + thing1_width:
            if thing1_start_y <= car_y <= thing1_height + thing1_start_y \
                    or thing1_start_y <= car_y + car_height <= thing1_height + thing1_start_y:
                crash(score)

        if car_x <= thing2_start_x <= car_width + car_x or car_x <= thing2_start_x + thing2_width <= car_x + car_width:
            if car_y <= thing2_start_y <= car_height + car_y \
                    or car_y <= thing2_start_y + thing2_height <= car_y + car_height:
                crash(score)

        if thing2_start_x <= car_x <= thing2_start_x + thing2_width \
                or thing2_start_x <= car_x + car_width <= thing2_start_x + thing2_width:
            if thing2_start_y <= car_y <= thing2_height + thing2_start_y \
                    or thing2_start_y <= car_y + car_height <= thing2_height + thing2_start_y:
                crash(score)

        message_display(score, (width / 2, 100), 115)
        pygame.display.update()
        clock.tick(60)


run()
pygame.quit()
quit()
