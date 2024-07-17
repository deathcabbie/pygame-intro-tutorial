import pygame
from sys import exit

def display_score():
    current_time = pygame.time.get_ticks()
    score_surface = test_font.render(f'{current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)

pygame.init()

game_active = True

# creating display surface
screen = pygame.display.set_mode((800, 400)) #tuple
# think about window size as coordinate system (origin point top left)

# give game a title in window bar
pygame.display.set_caption('Runner Game')

# creating a clock obejct for time and frame rate
clock = pygame.time.Clock()

# plain colour surface
# test_surface = pygame.Surface((800,400)) # create a size
# test_surface.fill('White') # colour fill (different types of arguments)

# background image
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# font
test_font = pygame.font.Font('fonts/Pixeltype.ttf', 75) # 2 arguments (font type, font size)
# score_surface = test_font.render('My Game', False, (64,64,64)) # 3 arguments ('text to be displayed', AA True or false (smooths edges), colour)
# score_rect = score_surface.get_rect(center = (400,50))

# snail character
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomleft = (800, 270))

# player
player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80,270)) # draws rectangle around surface

player_gravity = 0

# how to keep our code running forever
while True:
# draw all the elements
# update everything
    for event in pygame.event.get(): #loops through all the possible events
        if event.type == pygame.QUIT: # this event is a constant that is synonymous with the X button
            pygame.quit() # opposite of init
            exit() # system exit
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 270:
                        player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800

    if game_active:
        # attach surfaces to display surface
        screen.blit(sky_surface,(0,0)) # blit commman stands for block image transfer (put one surface on another surface)
                                        # -> 2 arguments are 'surface you want to place' and 'position'
        screen.blit(ground_surface,(0,268))

        #pygame.draw.rect(screen,'#c0e8ec',score_rect)
        #screen.blit(score_surface,score_rect)
    
        snail_rect.x -= 3
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surface,snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 270:
            player_rect.bottom = 270
        screen.blit(player_surface,player_rect)
        
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('Yellow')

    pygame.display.update() # updates the display surface from above
    clock.tick(60) # 60 is telling game that the loop should not run faster than 60 times per second:
