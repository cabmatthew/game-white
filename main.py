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

rectX = width/2-30
rectY = height/2-30

game_dir = os.path.dirname(__file__)
assets_dir = os.path.join(game_dir, "assets")
img_dir = os.path.join(assets_dir, "images")

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "green circle.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        # self.rect = self.image_scaled.get_rect()

        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speed_x = 0.0
        self.speed_y = 0.0

        # FIRING DELAY
        self.firing_delay = 100
        self.last_fired = pygame.time.get_ticks()
        # ammo stuff
        self.clip_size = 8
        self.ammo = self.clip_size
        # use for play reload sound only once
        self.reload_a = 0

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        speed = 7

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


        # FIRING
        if key_state[pygame.K_SPACE]:
            self.fire()

        # RELOADING
        if key_state[pygame.K_r]:
            self.reload()
            # stuff to have reload sound just once
            self.reload_a += 1
            if self.reload_a == 1:
                reload_sound.play()

        # NO GOING OUT OF WINDOW
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

        # AMMO TEXT
        self.textRender(window, str(self.ammo), 30, 30, 10)
        self.textRender(window, "/", 30, 50, 10)
        self.textRender(window, str(self.clip_size), 30, 70, 10)
        if self.ammo == 0:
            self.textRender(window, "trash player got no ammo, RELOAD", 50, width / 2, 80)

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
                projectile = Projectile(self.rect.centerx, self.rect.centery, enemy, 10, 10)
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
        font_match = pygame.font.match_font('arial')
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(font_match, size)
        # surface for text pixels - TRUE = anti-aliased
        text_surface = font.render(text, True, WHITE)
        # get rect for text surface rendering
        text_rect = text_surface.get_rect()
        # specify a relative location for text
        text_rect.midtop = (x, y)
        # add text surface to location of text rect
        surface.blit(text_surface, text_rect)

    def meleeHit(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery, enemy, 50, 10)
        # projectile = Projectile(self.rect.centerx, self.rect.centery, player)
        #     game_sprites.add(projectile)
        #     projectiles.add(projectile)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = width / 2
        self.rect.bottom = height - 20
        self.speed_x = 0.0
        self.speed_y = 0.0
        self.speed = 7

        self.health = 100
        self.display_hurt = False
        self.time_to_stop_display_hurt = 0
        self.oof = 0

    def update(self):
        self.speed_x = 0.0
        self.speed_y = 0.0

        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_j]:
            self.speed_x = -self.speed
        if key_state[pygame.K_l]:
            self.speed_x = self.speed
        if key_state[pygame.K_k]:
            self.speed_y = self.speed
        if key_state[pygame.K_i]:
            self.speed_y = -self.speed

        # move speed units every update
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # stop when reaching window boundary
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0

        # collisions GROUP variable, DELETE any projectiles that collide with enemy sprite
        collisions = pygame.sprite.groupcollide(enemy_sprites, projectiles, False, True)

        time_now = pygame.time.get_ticks()
        # when ENEMY collides with any PROJECTILE
        if collisions:
            oof_sound.play()
            # SET TIME to stop displaying hurt text
            self.time_to_stop_display_hurt = time_now + 600
            self.health -= 10

        # if ALIVE aka health above 0
        if self.health > 0:
            # when alive, display health
            self.textRender(window, str(self.health), 20, self.rect.centerx, self.rect.top - 25)
            # DISPLAY FOR CERTAIN AMT OF TIME
            # time now, time now + length
            # display if (time now) < (time now + length)
            if time_now < self.time_to_stop_display_hurt:
                self.textRender(window, "o no i got shot", 30, self.rect.centerx, self.rect.top - 60)
            else:
                self.textRender(window, "haha can't shoot me loser", 15, self.rect.centerx, self.rect.top - 50)
        else:
            self.textRender(window, "rip im dead", 60, self.rect.centerx, self.rect.top - 50)
            self.speed = 0
            self.oof += 1

        if self.oof == 1:
            oof_sound.play()

    # def fire(self):
    #
    #     projectile = Projectile(self.rect.centerx, self.rect.centery, player)
    #     game_sprites.add(projectile)
    #     projectiles.add(projectile)

    def textRender(self, surface, text, size, x, y):
        font_match = pygame.font.match_font('arial')
        # specify font for text render - uses found font and size of text
        font = pygame.font.Font(font_match, size)
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
    def __init__(self, x, y, targ, xscale, yscale):
        pygame.sprite.Sprite.__init__(self)
        self.targ = targ

        # self.image = pygame.Surface((30, 30)) # how sprite looks in game window
        self.image = pygame.image.load(os.path.join(img_dir, "red circle.png")).convert()
        # self.image.fill(WHITE)
        self.image = pygame.transform.scale(self.image, (xscale, yscale))
        self.rect = self.image.get_rect()  # boundary for sprite, for moving, collision

        self.rect.centerx = x
        self.rect.bottom = y

        self.speed = 15
        x_d = self.rect.centerx - self.targ.rect.centerx
        y_d = self.rect.centery - self.targ.rect.centery
        dist = (x_d ** 2 + y_d ** 2) ** .5

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



# game sprite group
game_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

# create player object
player = Player()
enemy = Enemy()
# add sprite to game's sprite group
game_sprites.add(player)
game_sprites.add(enemy)
enemy_sprites.add(enemy)

clock = pygame.time.Clock()

while not done:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    key_state = pygame.key.get_pressed()
    if key_state[pygame.K_ESCAPE]:
        done = True

    window.fill(BLACK)

    game_sprites.update()
    game_sprites.draw(window)

    pygame.display.flip()
    clock.tick(60)
    pygame.display.flip()

