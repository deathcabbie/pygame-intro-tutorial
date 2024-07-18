import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png')
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png')
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png')
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 270:
            self.gravity = -20
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom <= 270:
            self.rect.bottom = 270
    def update(self):
        self.player_input()
        self.apply_gravity

    def animation_state(self):
        if self.rect.bottom < 270:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = large_font.render(f'Score:  {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 270:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def player_animation():
    global player_surface, player_index
    if player_rect.bottom < 270:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
        
pygame.init()

game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
# player.add(Player())

# creating display surface
screen = pygame.display.set_mode((800, 400)) #tuple

# give game a title in window bar
pygame.display.set_caption('Runner Game')

# creating a clock object for time and frame rate
clock = pygame.time.Clock()

# plain colour surface
# test_surface = pygame.Surface((800,400)) # create a size
# test_surface.fill('White') # colour fill (different types of arguments)

# background image
sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# font
large_font = pygame.font.Font('fonts/Pixeltype.ttf', 75)
med_font = pygame.font.Font('fonts/Pixeltype.ttf', 50) # 2 arguments (font type, font size)
#score_surface = test_font.render('My Game', False, (64,64,64)) # 3 arguments ('text to be displayed', AA True or false (smooths edges), colour)
#score_rect = score_surface.get_rect(center = (400,50))

# obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 # use later to choose which walk image
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,270)) # draws rectangle around surface
player_gravity = 0

# intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand= pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = large_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = med_font.render('Press space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,340))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

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
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomleft = (randint(900,1100),270)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomleft = (randint(900,1100),180)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        # attach surfaces to display surface
        screen.blit(sky_surface,(0,0)) # blit commman stands for block image transfer (put one surface on another surface)
                                        # -> 2 arguments are 'surface you want to place' and 'position'
        screen.blit(ground_surface,(0,268))

        score = display_score()

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 270:
            player_rect.bottom = 270
        player_animation()
        screen.blit(player_surface,player_rect)
        player.draw(screen)
        player.update()

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = med_font.render(f'Your Score: {score}', False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name,game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    
    pygame.display.update() # updates the display surface from above
    clock.tick(60) # 60 is telling game that the loop should not run faster than 60 times per second:
