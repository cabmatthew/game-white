import pygame
import os

pygame.init()
width = 1000;
height = 700;
window = pygame.display.set_mode((width, height))
done = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (130, 130, 130)

rectX = width / 2 - 30
rectY = height / 2 - 30

game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir, "assets")
img_dir = os.path.join(assets_dir, "images")
fnt_dir = os.path.join(assets_dir, "fonts")

# Importing images for sprites & bullets
green_circle = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
red_circle = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()

green_circle.set_colorkey(WHITE)
red_circle.set_colorkey(WHITE)

# SOUNDS
pygame.mixer.init()
snd_dir = os.path.join(assets_dir, "sounds")
pew_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'pew.wav'))
oof_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'oof.wav'))
reload_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'reload.wav'))
ded_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'ded.wav'))
aggro_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'aggro.wav'))
shot_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'shot.wav'))
busstart_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'busstart.wav'))

# FONT
custom_font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"))



class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, twidth, theight):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([twidth, theight])
        self.image.fill(GREY)  # DELETE WHEN WANT INVISIBLE
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(player_sprites, texts, False, False)
        collisions1 = pygame.sprite.groupcollide(projectiles, walls, True, False)




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        # self.rect = self.image_scaled.get_rect()

        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = 30
        self.rect.bottom = 120
        self.speed_x = 0.0
        self.speed_y = 0.0

        # FIRING DELAY
        self.firing_delay = 300
        self.last_fired = pygame.time.get_ticks()
        # ammo stuff
        self.clip_size = 8
        self.ammo = self.clip_size
        # use for play reload sound only once
        self.reload_a = 0

    def update(self):
        # self.textRender(window, str(self.rect.centerx), 25, self.rect.centerx - 50, self.rect.centery + 50)
        # self.textRender(window, str(self.rect.centery), 25, self.rect.centerx + 50, self.rect.centery + 50)

        self.speed_x = 0
        self.speed_y = 0
        speed = 3

        # key_state = pygame.key.get_pressed()
        # mouse_state = pygame.mouse.get_pressed()
        # if key_state[pygame.K_a]:
        #     self.speed_x = -speed
        # if key_state[pygame.K_d]:
        #     self.speed_x = speed
        # if key_state[pygame.K_s]:
        #     self.speed_y = speed
        # if key_state[pygame.K_w]:
        #     self.speed_y = -speed
        # self.rect.x += self.speed_x
        # self.rect.y += self.speed_y

        key_state = pygame.key.get_pressed()
        mouse_state = pygame.mouse.get_pressed()
        for obstacle in obstacles:
            collided = self.rect.colliderect(obstacle)
            # SELF ABOVE OBSTACLE
            if self.rect.centery < obstacle.rect.centery:
                if self.rect.left > obstacle.rect.left and self.rect.right < obstacle.rect.right:
                    if collided:
                        self.rect.y -= 3
            # SELF BELOW OBSTACLE
            if self.rect.centery > obstacle.rect.centery:
                if self.rect.left > obstacle.rect.left and self.rect.right < obstacle.rect.right:
                    if collided:
                        self.rect.y += 3
            # SELF LEFT OF OBSTACLE
            if self.rect.centerx < obstacle.rect.centerx:
                if self.rect.top > obstacle.rect.top and self.rect.bottom < obstacle.rect.bottom:
                    if collided:
                        self.rect.x -= 3
            # SELF RIGHT OF OBSTACLE
            if self.rect.centerx > obstacle.rect.centerx:
                if self.rect.top > obstacle.rect.top and self.rect.bottom < obstacle.rect.bottom:
                    if collided:
                        self.rect.x += 3

            if key_state[pygame.K_a]:
                self.speed_x = -speed
            if key_state[pygame.K_d]:
                self.speed_x = speed
            if key_state[pygame.K_s]:
                self.speed_y = speed
            if key_state[pygame.K_w]:
                self.speed_y = -speed
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

        # FIRING
        if mouse_state[0]:
            self.fire()

        # RELOADING
        if key_state[pygame.K_r]:
            self.reload()
            # stuff to have reload sound just once
            self.reload_a += 1
            if self.reload_a == 1:
                reload_sound.play()

        # t1 = TextSprite(100, 100, 200, 200, "Ugh, how long was I out for?")
        # texts.add(t1)
        # t2 = TextSprite(400, 100, 200, 200, "Oh, sweet! I have a gun in my pocket!")
        # texts.add(t2)

        if self.rect.colliderect(t1):
            self.textRender(window, "Ugh, how long was I out for?", 15, width / 2, height - 100)
            self.textRender(window, "Where is everyone?", 15, width / 2, height - 50)
            self.textRender(window, "Move with WASD", 20, width / 2, 300)
        if self.rect.colliderect(t2):
            self.textRender(window, "Oh, sweet! I have a gun in my pocket!", 15, width / 2, height - 150)
            self.textRender(window, "I should shoot that zombie with LMB", 15, width / 2, height - 100)
            self.textRender(window, "I think I can reload using R", 15, width / 2, height - 50)
        if self.rect.colliderect(t3):
            self.textRender(window, "Can I sneak up on that one? I wonder.", 15, width / 2, height - 150)
            self.textRender(window, "I should be ready to run away, just in case", 15, width / 2, height - 100)
        if self.rect.colliderect(t4):
            self.textRender(window, "I see another one. Easy kill.", 15, width / 2, height - 150)
        if self.rect.colliderect(t5):
            self.textRender(window, "A bus? I should get in.", 15, width / 2, height - 150)
            self.textRender(window, "Hopefully I can find my friends.", 15, width / 2, height - 100)
        if self.rect.colliderect(t6):
            self.textRender(window, "A zombie? I'd better not touch it", 15, width / 2, height - 150)
            self.textRender(window, "or else I'll die.", 15, width / 2, height - 100)


        # AMMO TEXT
        self.textRender(window, str(self.ammo), 20, 30, 10)
        self.textRender(window, "/", 20, 50, 10)
        self.textRender(window, str(self.clip_size), 20, 70, 10)
        if self.ammo == 0:
            self.textRender(window, "No more ammo in this clip!", 25, width / 2, 80)
            self.textRender(window, "Reload using R!", 25, width / 2, 120)

        # NO GOING OUT OF WINDOW
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

        # DEAD
        dead = pygame.sprite.groupcollide(player_sprites, enemy_sprites, False, False)
        if dead:
            global dead_screen
            dead_screen = True

    def fire(self):
        # get current time
        time_now = pygame.time.get_ticks()

        # fire at rate of self.firing_delay
        # fire only if ammo available
        if self.ammo > 0:
            # if time between last shot and now is MORE than delay, FIRE
            if time_now - self.last_fired > self.firing_delay:
                # update time of last fired shot
                self.last_fired = time_now
                # spawn projectile
                mouse_pos = pygame.mouse.get_pos()
                projectile = Projectile(self.rect.centerx, self.rect.centery, 10, 10)  # MAKE TO CURSOR
                # projectile = Projectile(mouse_pos[0], mouse_pos[1], enemy, 10, 10)  # MAKE TO CURSOR
                game_sprites.add(projectile)
                projectiles.add(projectile)
                # use 1 ammo, play pew
                self.ammo -= 1
                pew_sound.play()
        # used to make reload sound play just once, RESET reload ct when firing
        self.reload_a = 0

    def reload(self):
        self.ammo = self.clip_size

    def textRender(self, surface, text, size, x, y):
        # font_match = pygame.font.match_font('arial')
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, coord):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = coord[0]
        self.rect.centery = coord[1]
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.speed = 0
        self.chase = False
        self.aggro = False

        self.health = 100
        self.display_hurt = False
        self.time_to_stop_display_hurt = 0
        self.time_to_die = 0
        self.oof = 0

    def update(self):
        if self.chase:
            self.speed = 1

        x_d = self.rect.centerx - player.rect.centerx
        y_d = self.rect.centery - player.rect.centery
        self.dist = (x_d ** 2 + y_d ** 2) ** .5
        # self.textRender(window, str(self.dist), 30, self.rect.centerx, self.rect.top - 60)
        if self.dist < 150:
            self.chase = True

        if self.chase == True:
            if self.aggro == False:
                aggro_sound.play()
                self.aggro = True

        self.speed_x = 0.0
        self.speed_y = 0.0
        if player.rect.x > self.rect.x:
            self.speed_x = self.speed
        if player.rect.y > self.rect.y:
            self.speed_y = self.speed
        if player.rect.x < self.rect.x:
            self.speed_x = -self.speed
        if player.rect.y < self.rect.y:
            self.speed_y = -self.speed

        # move speed units every update
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # collisions GROUP variable, DELETE any projectiles that collide with enemy sprite
        collisions = pygame.sprite.groupcollide(projectiles, enemy_sprites, True, False)

        time_now = pygame.time.get_ticks()
        # when ENEMY collides with any PROJECTILE
        if collisions:
            # oof_sound.play()
            shot_sound.play()
            # SET TIME to stop displaying hurt text
            self.time_to_stop_display_hurt = time_now + 600
            self.health -= 10
            self.chase = True

        # if ALIVE aka health above 0
        if self.health > 0:
            # when alive, display health
            self.textRender(window, str(self.health), 10, self.rect.centerx, self.rect.top - 25)
            # DISPLAY FOR CERTAIN AMT OF TIME
            # time now, time now + length
            # display if (time now) < (time now + length)
            # if time_now < self.time_to_stop_display_hurt:
                # self.textRender(window, "o no i got shot", 30, self.rect.centerx, self.rect.top - 60)
            # else:
                # self.textRender(window, "haha can't shoot me loser", 15, self.rect.centerx, self.rect.top - 50)
        else:
            self.kill()
            ded_sound.play()

        if self.oof == 1:
            oof_sound.play()

    def textRender(self, surface, text, size, x, y):
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)


projectiles = pygame.sprite.Group()


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, xscale, yscale):
        pygame.sprite.Sprite.__init__(self)
        # self.targ = targ

        mouse_pos = pygame.mouse.get_pos()
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert_alpha()
        # self.image.fill(WHITE)
        self.image = pygame.transform.scale(self.image, (xscale, yscale))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 15
        # finding x & y distance
        # x_d = self.rect.centerx - self.targ.rect.centerx
        # y_d = self.rect.centery - self.targ.rect.centery
        x_d = self.rect.centerx - mouse_pos[0]
        y_d = self.rect.centery - mouse_pos[1]
        dist = (x_d ** 2 + y_d ** 2) ** .5
        # calculating velocity x & y components from distance
        self.speed_x = x_d / dist * self.speed
        self.speed_y = y_d / dist * self.speed

        # self.time_alive = time_alive

    def update(self):
        self.rect.centerx -= self.speed_x
        self.rect.centery -= self.speed_y

        if self.rect.right > width:
            self.kill()
        if self.rect.left < 0:
            self.kill()
        if self.rect.bottom > height:
            self.kill()
        if self.rect.top < 0:
            self.kill()



# # game sprite group
# game_sprites = pygame.sprite.Group()
# enemy_sprites = pygame.sprite.Group()
# player_sprites = pygame.sprite.Group()
#
# # create player object
# player = Player()
# enemy = Enemy(600, 50)
# # add sprite to game's sprite group
# game_sprites.add(player)
# game_sprites.add(enemy)
# enemy_sprites.add(enemy)
# player_sprites.add(player)

clock = pygame.time.Clock()

pause_screen = False  # HANDLING PAUSE
title_screen = True
global dead_screen
dead_screen = False

def dead():
    window.fill((0, 0, 0))
    # Create a text surface with "Game is Paused"
    text_surface = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 48).render("You died.",
                                                                                                  True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 - 50)

    text_surface1 = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 30).render("Restart the game to try again.",
                                                                                                  True, (255, 0, 0))
    text_rect1 = text_surface1.get_rect()
    text_rect1.center = (width // 2, height // 2 + 25)
    # Draw the text surface to the screen
    window.blit(text_surface, text_rect)
    window.blit(text_surface1, text_rect1)

    # Update the screen
    pygame.display.flip()


def paused():
    window.fill((0,0,0))
    # Create a text surface with "Game is Paused"
    text_surface = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 48).render("Game is Paused",
                                                                                                  True, (255, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2)

    # Draw the text surface to the screen
    window.blit(text_surface, text_rect)

    # Update the screen
    pygame.display.flip()


def title():
    title_text = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 80).render("Daybreak", True,
                                                                                                BLACK)
    subtitle_text = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 15).render("Press [SPACEBAR] "
                                                                                                   "To Start", True,
                                                                                                   BLACK)
    title_background = pygame.image.load(os.path.join(img_dir, "title_bckgnd.png"))
    title_background = pygame.transform.scale(title_background, (width, height))
    title_rect = title_text.get_rect()
    subtitle_rect = subtitle_text.get_rect()
    title_rect.center = (width / 2, height / 2)
    subtitle_rect.center = (width / 2, height / 2 + 70)
    window.blit(title_background, (0, 0))
    window.blit(title_text, title_rect)
    window.blit(subtitle_text, subtitle_rect)
    pygame.display.flip()


global map_screen
map_screen = False

global bus_started
bus_started = False


class Bus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = 50
        self.rect.bottom = height / 2
        self.speed_x = 0.0
        self.speed_y = 0.0


    def update(self):
        # self.textRender(window, str(self.rect.centerx), 20, self.rect.centerx-50, self.rect.top-25)
        # self.textRender(window, str(self.rect.centery), 20, self.rect.centerx + 50, self.rect.top - 25)

        self.speed_x = 0
        self.speed_y = 0
        speed = 3

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_a]:
            self.speed_x = -speed
        if key_state[pygame.K_d]:
            self.speed_x = speed
        if key_state[pygame.K_s]:
            self.speed_y = speed
        if key_state[pygame.K_w]:
            self.speed_y = -speed
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if key_state[pygame.K_a]:
            self.image = pygame.image.load(os.path.join(img_dir, "busA.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))
        if key_state[pygame.K_d]:
            self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (150, 150))


        # NO GOING OUT OF WINDOW
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

    def textRender(self, surface, text, size, x, y):
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)




class MapLocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "city.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        # pygame.draw.rect(self.image,WHITE,pygame.Rect(x, y, width, height))

        self.rect.centerx = 500
        self.rect.centery = height / 2
    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(bussy, city1group, False, False)
        # when  collides
        if collisions:
            self.textRender(window, "Press SPACE to enter this city.", 15, width / 2, height - 50)
            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
    def textRender(self, surface, text, size, x, y):
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)

class BusPortal(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "busD.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = width - 100
        self.rect.centery = height - 100

    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(player_sprites, bustransport, False, False)
        # when  collides
        if collisions:
            self.textRender(window, "Press SPACE to enter this vehicle.", 15, width / 2, height - 50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        global map_screen
                        map_screen = True
                        busstart_sound.play()


    def textRender(self, surface, text, size, x, y):
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)

# game sprite group
game_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()

# create player object
player = Player()
# add sprite to game's sprite group
game_sprites.add(player)
# game_sprites.add(enemy)
player_sprites.add(player)

bussy = pygame.sprite.Group()
bus = Bus()
bussy.add(bus)

city1group = pygame.sprite.Group()
city1 = MapLocation()
city1group.add(city1)

bustransport = pygame.sprite.Group()
busportal = BusPortal()
bustransport.add(busportal)


def showmap():
    window.fill((138, 98, 65))
    # Create a text surface with "Game is Paused"
    text_surface = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), 48).render("World Map",
                                                                                                  True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, 50)

    # Draw the text surface to the screen
    window.blit(text_surface, text_rect)



spawnfirstenemies = True


walls = pygame.sprite.Group()
w1 = Wall(250, 230, 1050, 50)
walls.add(w1)
w3 = Wall(600, 480, 800, 50)
walls.add(w3)
# w3 = Wall(600, 450, 800, 50)
# walls.add(w3)
obstacles = [w1, w3]

def firstlevel():
    # enemy_locations = ([100, 100], [200, 100], [300, 100])
    enemy_locations = (850, 120), (850, 400), (100, 370), (650, 620),
    # for location in enemy_locations:
    #     newEnemy = Enemy(location)
    #     enemy_sprites.add(newEnemy)
    #     game_sprites.add(newEnemy)

    e1 = Enemy(enemy_locations[0])
    e2 = Enemy(enemy_locations[1])
    e3 = Enemy(enemy_locations[2])
    e4 = Enemy(enemy_locations[3])
    enemy_sprites.add(e1)
    enemy_sprites.add(e2)
    enemy_sprites.add(e3)
    enemy_sprites.add(e4)
    game_sprites.add(e1)
    game_sprites.add(e2)
    game_sprites.add(e3)
    game_sprites.add(e4)


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, twidth, theight, text2):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([twidth, theight])
        self.image.fill(BLUE) # DELETE WHEN WANT INVISIBLE
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.text = text2

    def update(self):
        # collisions GROUP variable
        collisions = pygame.sprite.groupcollide(player_sprites, texts, False, False)
        # when  collides
        # if collisions:
            # self.textRender(window, self.text, 15, width / 2, height - 50)

    def textRender(self, surface, text, size, x, y):
        # font_match = pygame.font.match_font('arial')
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(os.path.join(fnt_dir, "PressStart2P-Regular.ttf"), size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)


texts = pygame.sprite.Group()
t1 = TextSprite(40, 100, 100, 200, "Ugh, how long was I out for?")
texts.add(t1)
t2 = TextSprite(400, 100, 200, 200, "Oh, sweet! I have a gun in my pocket!")
texts.add(t2)
t3 = TextSprite(870, 100, 200, 200, "Oh, sweet! I have a gun in my pocket!")
texts.add(t3)
t4 = TextSprite(600, 350, 200, 200, "Oh, sweet! I have a gun in my pocket!")
texts.add(t4)
t5 = TextSprite(350, 600, 200, 200, "Oh, sweet! I have a gun in my pocket!")
texts.add(t5)
t6 = TextSprite(170, 100, 100, 200, "asdf")
texts.add(t6)

while not done:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if event.key == pygame.K_p and not map_screen:  # HANDLING PAUSE
                pause_screen = not pause_screen
            if event.key == pygame.K_SPACE and title_screen:
                title_screen = not title_screen
            # if event.key == pygame.K_m and not pause_screen and not title_screen:
            #     map_screen = not map_screen


    # window.fill((0,155,0))

    # HANDLING PAUSE, title, and play states
    if title_screen:
        title()
    elif not (pause_screen or map_screen or dead_screen) :
        if spawnfirstenemies:
            firstlevel()
            spawnfirstenemies = False

        window.fill((0, 155, 0))
        texts.update()
        texts.draw(window)
        game_sprites.update()
        game_sprites.draw(window)
        bustransport.update()
        bustransport.draw(window)
        walls.update()
        walls.draw(window)

    elif pause_screen and not map_screen and not title_screen:
        paused()
    elif map_screen and not pause_screen and not title_screen:
        showmap()
        bussy.update()
        bussy.draw(window)
        city1group.update()
        city1group.draw(window)

    # global dead_screen
    if dead_screen:
        dead()

    clock.tick(60)
    pygame.display.flip()
