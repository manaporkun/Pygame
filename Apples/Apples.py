import pygame
import random

pygame.init()

width = 600
height = 400
red = (255,0,0)
white = (255,255,255)
objectVolume = 20
numberHorizontal = width // objectVolume
numberVertical = height // objectVolume
screen = pygame.display.set_mode((width,height))
soundBeep = pygame.mixer.Sound("beep.wav")


def Add_Trophy(trophies):
    trophy = pygame.sprite.Sprite()
    trophy.image = pygame.Surface([objectVolume-10,objectVolume-10])
    trophy.image.fill(red)
    trophy.rect = trophy.image.get_rect()
    trophy.rect.left = random.randint(0,numberHorizontal-1)*objectVolume
    trophy.rect.top = random.randint(0,numberVertical-1)*objectVolume
    trophies.add(trophy)

player = pygame.sprite.Sprite()
player.image = pygame.Surface([objectVolume-10,objectVolume-10])
player.image.fill(white)
player.rect = player.image.get_rect()
player_group = pygame.sprite.GroupSingle(player)
trophies = pygame.sprite.OrderedUpdates()

for i in range(10):
    Add_Trophy(trophies)

pygame.time.set_timer(pygame.USEREVENT,1000)

gameOver = False
score = 0

while (gameOver != True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_ESCAPE:
                gameOver = True
        if event.type == pygame.USEREVENT:
            Add_Trophy(trophies)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            player.rect.x = (pos[0] // objectVolume)*objectVolume
            player.rect.y = (pos[1] // objectVolume)*objectVolume


    screen.fill((0,0,0))
    trophies.draw(screen)
    player_group.draw(screen)
    pygame.display.update()
    collides = pygame.sprite.groupcollide(player_group,trophies,False,True)

    if len(collides)> 0:
        soundBeep.play()
        score += len(collides)*10
        print(score)
        print(pygame.time.get_ticks()// 1000)
    elif len(trophies) == 0:
        soundBeep.play()
        soundBeep.play()
        soundBeep.play()
        score+=1000
        print("Win")
        print("Score: ",score)
        gameOver = True


pygame.quit()
