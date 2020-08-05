import pygame as pg
from steady_cons import *
from random import choice, randint, randrange


class SpriteSheet(object):

    def __init__(self, file_name):
        self.sprite_sheet = pg.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface([width, height], ).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image


class Bg_sprite_1(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pg.image.load("BG.png").convert()
        self.rect = self.image.get_rect()
        self.last_update = pg.time.get_ticks()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 600
        self.y_change = 5

    def update(self):
        self.rect.y += self.y_change
        if self.rect.top >= 600:
            self.rect.bottom = 0


class Bg_sprite_2(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        self.image = pg.image.load("BG.png").convert()
        self.rect = self.image.get_rect()
        self.last_update = pg.time.get_ticks()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 0
        self.y_change = 5

    def update(self):
        self.rect.y += self.y_change
        if self.rect.top >= 600:
            self.rect.bottom = 0


class Player(pg.sprite.Sprite):
    def __init__(self, game, skinx_pos):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("ship_spr_0.png")
        self.game = game
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 0, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 64, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 128, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 192, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 256, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 320, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 384, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 448, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 512, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 576, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 640, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 704, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 768, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 832, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 896, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 960, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 1024, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 1088, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 1152, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skinx_pos, 1216, 64, 64))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.shield = 100
        self.normal_delay = 250
        self.normal_delay_2 = 100
        self.last_shot = pg.time.get_ticks()
        self.power = 1
        self.power_2 = 1
        self.power_timer = pg.time.get_ticks()
        self.power_time_2 = pg.time.get_ticks()

    def update(self):
        if self.power_2 == 1:
            self.normal_delay = 250
            if self.game.score >= 1000:
                self.normal_delay = 225
            elif self.game.score >= 2500:
                self.normal_delay = 200
            elif self.game.score >= 4000:
                self.normal_delay = 180
        if self.power_2 >= 2:
            self.normal_delay = 150
        if self.power_2 >= 2 and pg.time.get_ticks() - self.power_timer_2 > POWER_TIMER:
            self.power_2 -= 1
            self.power_timer_2 = pg.time.get_ticks()
        if self.power >= 2 and pg.time.get_ticks() - self.power_timer > POWER_TIMER:
            self.power -= 1
            self.power_timer = pg.time.get_ticks()

        self.current_sprite += 1

        if self.current_sprite >= 18:
            self.current_sprite = 0

        self.x_change = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RIGHT]:
            self.x_change = 8
        if keystate[pg.K_LEFT]:
            self.x_change = -8
        if keystate[pg.K_SPACE]:
            self.shoot()
        self.rect.x += self.x_change
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.image = self.sprite[int(self.current_sprite)]

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.normal_delay:
            self.last_shot = now
            if self.power == 1:
                b0 = Bullet(self.rect.centerx, self.rect.top)
                self.game.game_sprites.add(b0)
                self.game.bullet_sprites.add(b0)
                self.game.soundChannel_shoot.play(choice(shoot_snds))
            if self.power >= 2:
                b1 = Bullet(self.rect.left + 12, self.rect.centery)
                b2 = Bullet(self.rect.right - 12, self.rect.centery)
                self.game.game_sprites.add(b1)
                self.game.bullet_sprites.add(b1)
                self.game.game_sprites.add(b2)
                self.game.bullet_sprites.add(b2)
                self.game.soundChannel_shoot.play(choice(shoot_snds))

    def powerup(self):
        self.power += 1
        self.power_timer = pg.time.get_ticks()

    def powerup_2(self):
        self.power_2 += 1
        self.power_timer_2 = pg.time.get_ticks()


class Player_shop(pg.sprite.Sprite):
    def __init__(self, skin_index, pos):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("ship_spr_0.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(skin_index, 0, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 64, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 128, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 192, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 256, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 320, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 384, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 448, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 512, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 576, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 640, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 704, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 768, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 832, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 896, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 960, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 1024, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 1088, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 1152, 64, 64))
        self.sprite.append(sprite_sheet.get_image(skin_index, 1216, 64, 64))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.current_sprite += 1

        if self.current_sprite >= 18:
            self.current_sprite = 0

        self.image = self.sprite[int(self.current_sprite)]


class Mob(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("asteroid_spr_0.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 96, 96))
        self.sprite.append(sprite_sheet.get_image(96, 0, 96, 96))
        self.sprite.append(sprite_sheet.get_image(192, 0, 96, 96))
        self.sprite.append(sprite_sheet.get_image(288, 0, 96, 96))
        self.sprite.append(sprite_sheet.get_image(0, 96, 64, 64))
        self.sprite.append(sprite_sheet.get_image(64, 96, 64, 64))
        self.sprite.append(sprite_sheet.get_image(128, 96, 64, 64))
        self.sprite.append(sprite_sheet.get_image(192, 96, 64, 64))
        self.sprite.append(sprite_sheet.get_image(0, 160, 32, 32))
        self.sprite.append(sprite_sheet.get_image(32, 160, 32, 32))
        self.sprite.append(sprite_sheet.get_image(64, 160, 32, 32))
        self.sprite.append(sprite_sheet.get_image(96, 160, 32, 32))
        self.current_sprite = randint(0, 11)
        self.image_orig = self.sprite[self.current_sprite]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .95 / 2)
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        self.rect.y = randrange(-200, -100)
        self.y_change = randrange(5, 8)
        self.x_change = randrange(-3, 3)
        self.rotation = 0
        self.rotation_change = randint(-8, 8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        current_tick = pg.time.get_ticks()
        if current_tick - self.last_update > 60:
            self.last_update = current_tick
            self.rotation = (self.rotation + self.rotation_change) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.y_change
        self.rect.x += self.x_change
        if self.rect.right < 0:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)
        if self.rect.left > WIDTH:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)
        if self.rect.top > HEIGHT:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)


class Coin(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("coin.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(32, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(64, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(96, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(128, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(160, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(192, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(224, 0, 32, 32))
        self.sprite.append(sprite_sheet.get_image(256, 0, 32, 32))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -100)
        self.y_change = randrange(5, 8)
        self.x_change = randrange(-3, 3)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.current_sprite += 0.1

        if self.current_sprite > 7:
            self.current_sprite = 0
        self.image = self.sprite[int(self.current_sprite)]
        self.rect.y += self.y_change
        self.rect.x += self.x_change
        if self.rect.right < 0:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)
        if self.rect.left > WIDTH:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)
        if self.rect.top > HEIGHT:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-200, -100)


class Coin_display(pg.sprite.Sprite):
    def __init__(self, pos, amount_txt, txt_size):
        pg.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("coin_dis.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(48, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(96, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(144, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(192, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(240, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(288, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(336, 0, 48, 48))
        self.sprite.append(sprite_sheet.get_image(384, 0, 48, 48))
        self.current_sprite = 4
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.last_update = pg.time.get_ticks()
        self.font = pg.font.Font(FONT[0], txt_size)
        self.text_surface = self.font.render(amount_txt, False, WHITE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.midleft = self.rect.midright
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)
    #def update(self):
        #self.current_sprite += 1
        #if self.current_sprite > 7:
            #self.current_sprite = 0
        #self.image = self.sprite[int(self.current_sprite)]


class Explosion_sprite_sml(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("expl_spr_0.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(34, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(68, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(102, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(136, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(170, 0, 34, 34))
        self.sprite.append(sprite_sheet.get_image(204, 0, 34, 34))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pg.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_frame > self.frame_rate:
            self.last_frame = now
            self.current_sprite += 1
        if self.current_sprite > 6:
            self.kill()
        else:
            center = self.rect.center
            self.image = self.sprite[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = center


class Explosion_sprite_mid(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("expl_spr_1.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(68, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(136, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(204, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(272, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(340, 0, 68, 68))
        self.sprite.append(sprite_sheet.get_image(408, 0, 68, 68))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pg.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_frame > self.frame_rate:
            self.last_frame = now
            self.current_sprite += 1
        if self.current_sprite > 6:
            self.kill()
        else:
            center = self.rect.center
            self.image = self.sprite[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = center


class Explosion_sprite_larg(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("expl_spr_2.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(98, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(196, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(294, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(292, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(490, 0, 98, 98))
        self.sprite.append(sprite_sheet.get_image(588, 0, 98, 98))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pg.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_frame > self.frame_rate:
            self.last_frame = now
            self.current_sprite += 1
        if self.current_sprite > 6:
            self.kill()
        else:
            center = self.rect.center
            self.image = self.sprite[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = center


class Coin_splash(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("cn_splash.png")
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(40, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(80, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(120, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(160, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(200, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(240, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(280, 0, 40, 40))
        self.sprite.append(sprite_sheet.get_image(320, 0, 40, 40))
        self.current_sprite = 0
        self.image = self.sprite[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_frame = pg.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_frame > self.frame_rate:
            self.last_frame = now
            self.current_sprite += 1
        if self.current_sprite > 8:
            self.kill()
        else:
            center = self.rect.center
            self.image = self.sprite[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.center = center


class Button_1(pg.sprite.Sprite):
    def __init__(self, game, main_img_index, pos):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("but_spr_0.png")
        self.sprite = []
        '''start(0,1)'''
        self.sprite.append(sprite_sheet.get_image(0, 0, 160, 60))
        self.sprite.append(sprite_sheet.get_image(160, 0, 160, 60))
        '''option(2,3)'''
        self.sprite.append(sprite_sheet.get_image(0, 60, 188, 60))
        self.sprite.append(sprite_sheet.get_image(188, 60, 188, 60))
        '''shop(4,5)'''
        self.sprite.append(sprite_sheet.get_image(0, 120, 134, 60))
        self.sprite.append(sprite_sheet.get_image(134, 120, 134, 60))
        '''credits(6,7)'''
        self.sprite.append(sprite_sheet.get_image(0, 180, 193, 60))
        self.sprite.append(sprite_sheet.get_image(193, 180, 193, 60))
        '''back(8,9)'''
        self.sprite.append(sprite_sheet.get_image(200, 240, 30, 30))
        self.sprite.append(sprite_sheet.get_image(230, 240, 30, 30))
        '''help(10,11)'''
        self.sprite.append(sprite_sheet.get_image(308, 240, 32, 32))
        self.sprite.append(sprite_sheet.get_image(340, 240, 32, 32))
        '''retry(12,13)'''
        self.sprite.append(sprite_sheet.get_image(0, 300, 103, 50))
        self.sprite.append(sprite_sheet.get_image(103, 300, 103, 50))
        '''reset(14,15)'''
        self.sprite.append(sprite_sheet.get_image(262, 300, 62, 30))
        self.sprite.append(sprite_sheet.get_image(324, 300, 62, 30))

        self.game = game
        self.image = self.sprite[main_img_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event, button_down_index, button_up_index):

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.image = self.sprite[button_down_index]
                    self.game.soundChannel_click.play(pg.mixer.Sound(click_snds))
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.image = self.sprite[button_up_index]
                return self.rect.collidepoint(event.pos)


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("blt.png")
        super().__init__()
        self.sprite = []
        self.sprite.append(sprite_sheet.get_image(0, 0, 3, 8))
        self.sprite.append(sprite_sheet.get_image(3, 0, 3, 8))
        self.sprite.append(sprite_sheet.get_image(6, 0, 3, 8))
        self.sprite.append(sprite_sheet.get_image(9, 0, 3, 8))
        self.sprite.append(sprite_sheet.get_image(12, 0, 3, 8))
        self.current_sprite = randint(0, 4)
        self.image = self.sprite[self.current_sprite]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.y_change = -10

    def update(self):
        self.rect.y += self.y_change
        if self.rect.bottom < 0:
            self.kill()


class Pow(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        super().__init__()
        sprite_sheet = SpriteSheet("power_ups.png")

        self.type = randint(1, 3)
        self.regen = []
        self.dec_delay = []
        self.dual_wielding = []
        self.regen.append(sprite_sheet.get_image(0, 0, 32, 32))
        self.regen.append(sprite_sheet.get_image(0, 32, 32, 32))
        self.dec_delay.append(sprite_sheet.get_image(32, 0, 32, 32))
        self.dec_delay.append(sprite_sheet.get_image(32, 32, 32, 32))
        self.dual_wielding.append(sprite_sheet.get_image(64, 0, 32, 32))
        self.dual_wielding.append(sprite_sheet.get_image(64, 32, 32, 32))
        self.current_sprite = 0
        if self.type == 3:
            self.image = self.regen[self.current_sprite]
        elif self.type == 1:
            self.image = self.dec_delay[self.current_sprite]
        elif self.type == 2:
            self.image = self.dual_wielding[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.y_change = 3
        self.prev = pg.time.get_ticks()
        self.framerate = 2000

    def update(self):
        now = pg.time.get_ticks()
        self.rect.y += self.y_change
        if now - self.prev > self.framerate:
            self.current_sprite += 1
            if self.current_sprite > 1:
                self.current_sprite = 0
        if self.type == 3:
            self.image = self.regen[self.current_sprite]
        elif self.type == 1:
            self.image = self.dec_delay[self.current_sprite]
        elif self.type == 2:
            self.image = self.dual_wielding[self.current_sprite]
        if self.rect.top > HEIGHT:
            self.kill()


class Select_but(pg.sprite.Sprite):
    def __init__(self, main_img_index, pos):
        pg.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("but_spr_1.png")
        self.sprite = [
            sprite_sheet.get_image(0, 0, 59, 20),
            sprite_sheet.get_image(59, 0, 59, 20)
        ]

        self.image = self.sprite[main_img_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event, button_down_index, button_up_index, index, shop_message_T, shop_message_F, ship_value, ship_line):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.image = self.sprite[button_down_index]
                    with open(user_data, 'r') as user_pref_ship:
                        user_ship_readline = user_pref_ship.readlines()
                        x = int(user_ship_readline[ship_line]) #bool
                        if x == 1:
                            Bought = True
                        else:
                            Bought = False

                        if Bought:
                            user_ship_readline[7] = shop_message_T
                            user_ship_readline[2] = index
                        if not Bought:
                            open_user_data = open(results_data, 'r')
                            read_user_data = open_user_data.readlines()
                            prev_coin_count = read_user_data[1]
                            coin_count = int(prev_coin_count)
                            if coin_count >= ship_value:
                                user_ship_readline[7] = shop_message_T
                                user_ship_readline[2] = index
                                user_ship_readline[ship_line] = "1\n"
                                with open(results_data, 'r') as coin_changer:
                                    coin_readline = coin_changer.readlines()
                                    coin_tval = coin_readline[1]
                                    coin_f = int(coin_tval) - ship_value
                                    coin_readline[1] = str(coin_f)
                                with open(results_data, 'w') as coin_changer:
                                    coin_changer.writelines(coin_readline)
                                coin_changer.close()
                            else:
                                user_ship_readline[7] = shop_message_F
                    with open(user_data, 'w') as user_pref_ship:
                        user_pref_ship.writelines(user_ship_readline)
                    user_pref_ship.close()

        else:
            self.image = self.sprite[button_up_index]


class Music_onoff_but(pg.sprite.Sprite):
    def __init__(self, game, main_img_index, pos):
        pg.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("but_spr_0.png")
        self.game = game
        self.sprite = [
            sprite_sheet.get_image(0, 240, 100, 60),
            sprite_sheet.get_image(100, 240, 100, 60),
        ]
        self.image = self.sprite[main_img_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event, button_down_index, button_up_index):

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if pg.mixer.music.get_volume() > 0:
                        self.image = self.sprite[button_down_index]
                        self.game.mute()
                    else:
                        self.image = self.sprite[button_up_index]
                        self.game.unmute()
        if pg.mixer.music.get_volume() > 0:
            self.image = self.sprite[button_up_index]
        else:
            self.image = self.sprite[button_down_index]


class Sound_onoff_but(pg.sprite.Sprite):
    def __init__(self, game, main_img_index, pos):
        pg.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("but_spr_0.png")
        self.game = game
        self.sprite = [
            sprite_sheet.get_image(0, 240, 100, 60),
            sprite_sheet.get_image(100, 240, 100, 60),
        ]
        self.image = self.sprite[main_img_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event, button_down_index, button_up_index):

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if pg.mixer.Channel(0).get_volume() > 0:
                        self.image = self.sprite[button_down_index]
                        self.game.mute2()
                    else:
                        self.image = self.sprite[button_up_index]
                        self.game.unmute2()
        if pg.mixer.Channel(0).get_volume() > 0:
            self.image = self.sprite[button_up_index]
        else:
            self.image = self.sprite[button_down_index]
