import pygame as pg
from steady_cons import *
from sprite_reg import *
import random


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.sound_sys()
        '''transfer to menu'''
        pg.mixer.music.load(music_list[0])
        pg.mixer.music.play(loops=-1)
        

    def sound_sys(self):
        for snd in shoot_list:
            shoot_snds.append(pg.mixer.Sound(snd))
        for snd in coin_list:
            coin_snds.append(pg.mixer.Sound(snd))
        for snd in explosion_list:
            expl_snds.append(pg.mixer.Sound(snd))
        for snd in hit_list:
            hit_snds.append(pg.mixer.Sound(snd))

        self.soundChannel_shoot = pg.mixer.Channel(0)
        self.soundChannel_explosion = pg.mixer.Channel(1)
        self.soundChannel_coin = pg.mixer.Channel(2)
        self.soundChannel_hit = pg.mixer.Channel(3)
        self.soundChannel_click = pg.mixer.Channel(4)

        open_user_pref = open(user_data, 'r')
        read_user_pref = open_user_pref.readlines()
        prev_m_vol = read_user_pref[0]
        prev_s_vol = read_user_pref[1]
        pg.mixer.music.set_volume(float(prev_m_vol))
        pg.mixer.Channel(0).set_volume(float(prev_s_vol))
        pg.mixer.Channel(1).set_volume(float(prev_s_vol))
        pg.mixer.Channel(2).set_volume(float(prev_s_vol))
        pg.mixer.Channel(3).set_volume(float(prev_s_vol))
        pg.mixer.Channel(4).set_volume(float(prev_s_vol))
        open_user_pref.close()


    def mute(self):
        vol = 0
        with open(user_data, 'r') as music_open:
            music_readline = music_open.readlines()
            music_readline[0] = str(vol) + "\n"
        with open(user_data, 'w') as music_open:
            music_open.writelines(music_readline)
        music_open.close()
        pg.mixer.music.set_volume(vol)

    def unmute(self):
        vol = 1
        with open(user_data, 'r') as music_open:
            music_readline = music_open.readlines()
            music_readline[0] = str(vol) + "\n"
        with open(user_data, 'w') as music_open:
            music_open.writelines(music_readline)
        music_open.close()
        pg.mixer.music.set_volume(vol)

    def mute2(self):
        vol = 0
        with open(user_data, 'r') as sound_open:
            sound_readline = sound_open.readlines()
            sound_readline[1] = str(vol) + "\n"
        with open(user_data, 'w') as sound_open:
            sound_open.writelines(sound_readline)
        sound_open.close()
        pg.mixer.Channel(0).set_volume(vol)
        pg.mixer.Channel(1).set_volume(vol)
        pg.mixer.Channel(2).set_volume(vol)
        pg.mixer.Channel(3).set_volume(vol)
        pg.mixer.Channel(4).set_volume(vol)

    def unmute2(self):
        vol = 1
        with open(user_data, 'r') as sound_open:
            sound_readline = sound_open.readlines()
            sound_readline[1] = str(vol) + "\n"
        with open(user_data, 'w') as sound_open:
            sound_open.writelines(sound_readline)
        sound_open.close()
        pg.mixer.Channel(0).set_volume(vol)
        pg.mixer.Channel(1).set_volume(vol)
        pg.mixer.Channel(2).set_volume(vol)
        pg.mixer.Channel(3).set_volume(vol)
        pg.mixer.Channel(4).set_volume(vol)

    def increase_volume(self, new_vol):
        vol = new_vol
        with open(user_data, 'r') as music_open:
            music_readline = music_open.readlines()
            music_readline[0] = str(vol) + "\n"
        with open(user_data, 'w') as music_open:
            music_open.writelines(music_readline)
        music_open.close()
        pg.mixer.music.set_volume(vol)

    def increase_volume2(self, new_vol):
        vol = new_vol
        with open(user_data, 'r') as sound_open:
            sound_readline = sound_open.readlines()
            sound_readline[1] = str(vol) + "\n"
        with open(user_data, 'w') as sound_open:
            sound_open.writelines(sound_readline)
        sound_open.close()
        pg.mixer.Channel(0).set_volume(vol)

    def updateFile(self):
        with open(results_data, 'r') as score_open:
            score_readline = score_open.readlines()
            last = int(score_readline[0])
            score_readline[1] = str(self.coin_count) + "\n"
        with open(results_data, 'w') as score_open:
            score_open.writelines(score_readline)
        if last < int(self.score):
            score_readline[0] = str(self.score) + "\n"
            with open(results_data, 'w') as score_open:
                score_open.writelines(score_readline)
            return self.score
        score_open.close()
        return last

    def draw_text(self, text, size, x, y, font_type, color, antialias, alignment_0_topleft__1_midtop__2_topright__3_center):
        font = pg.font.Font(font_type, size)
        text_surface = font.render(text, antialias, color)
        text_rect = text_surface.get_rect()
        text_align = alignment_0_topleft__1_midtop__2_topright__3_center
        if text_align == 0:
            text_rect.topleft = (x, y)
        if text_align == 1:
            text_rect.midtop = (x, y)
        if text_align == 2:
            text_rect.topright = (x, y)
        if text_align == 3:
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def shield_bar(self, x, y, percentage):
        if self.player.shield <= 0:
            self.player.shield = 1
        bar_length = 100
        bar_height = 12
        fill = (percentage / 100) * bar_length
        outline_rect = pg.Rect(x, y, bar_length, bar_height)
        fill_rect = pg.Rect(x, y, fill, bar_height)
        pg.draw.rect(self.screen, GREEN, fill_rect)
        pg.draw.rect(self.screen, WHITE, outline_rect, 2)

    def new_mob(self):
        m = Mob()
        self.game_sprites.add(m)
        self.mob_sprites.add(m)

    def new_coin(self):
        c = Coin()
        self.game_sprites.add(c)
        self.coin_sprites.add(c)

    def start_game(self):
        self.game_sprites = pg.sprite.Group()
        self.pow_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.mob_sprites = pg.sprite.Group()
        self.coin_sprites = pg.sprite.Group()
        self.explosion_sprites = pg.sprite.Group()
        '''classes'''
        # coin count
        self.open_user_data = open(results_data, 'r')
        self.read_user_data = self.open_user_data.readlines()
        self.coin_count = int(self.read_user_data[1])
        self.open_user_data.close()
        # skin_type
        self.open_skin_type = open(user_data, 'r')
        self.read_ship = self.open_skin_type.readlines()
        self.plyr_skinxpos = player_list[int(self.read_ship[2])]
        self.open_skin_type.close()
        self.player = Player(self, self.plyr_skinxpos)
        '''add to sprite groups'''
        self.game_sprites.add(Bg_sprite_1())
        self.game_sprites.add(Bg_sprite_2())
        self.game_sprites.add(self.pow_sprites)
        self.game_sprites.add(self.bullet_sprites)
        self.game_sprites.add(self.mob_sprites)
        self.game_sprites.add(self.coin_sprites)
        self.game_sprites.add(self.player)
        self.game_sprites.add(self.explosion_sprites)

        for i in range(7):
            self.new_mob()
        for i in range(4):
            self.new_coin()
        self.score = 0
        game_running = True

        while game_running:
            self.clock.tick(FPS_MAIN)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.updateFile()
                    pg.quit()

            self.game_sprites.update()
            shots = pg.sprite.groupcollide(self.mob_sprites, self.bullet_sprites, True, True, pg.sprite.collide_mask)
            for shot in shots:
                if random.random() > 0.95:
                    pow = Pow(shot.rect.center)
                    self.game_sprites.add(pow)
                    self.pow_sprites.add(pow)
                if shot.radius <= 16:
                    self.score += 10
                    expl1 = Explosion_sprite_sml(shot.rect.center)
                    self.game_sprites.add(expl1)
                if shot.radius > 16 and shot.radius <= 32:
                    self.score += 15
                    expl2 = Explosion_sprite_mid(shot.rect.center)
                    self.game_sprites.add(expl2)
                if shot.radius > 32 and shot.radius <= 48:
                    self.score += 30
                    expl3 = Explosion_sprite_larg(shot.rect.center)
                    self.game_sprites.add(expl3)

                self.new_mob()

                self.soundChannel_explosion.play(random.choice(expl_snds))

            shots1 = pg.sprite.groupcollide(self.coin_sprites, self.bullet_sprites, True, True, pg.sprite.collide_rect)
            for shot in shots1:
                self.coin_count += 5
                coin_sp = Coin_splash(shot.rect.center)
                self.game_sprites.add(coin_sp)
                self.new_coin()
                self.soundChannel_coin.play(random.choice(coin_snds))

            hits = pg.sprite.spritecollide(self.player, self.mob_sprites, True, pg.sprite.collide_mask)

            for hit in hits:
                self.player.shield -= hit.radius * 1.8
                self.new_mob()
                expl4 = Explosion_sprite_sml(hit.rect.center)
                self.game_sprites.add(expl4)
                self.soundChannel_hit.play(random.choice(hit_snds))
                if self.player.shield <= 0:
                    death_expl = Explosion_sprite_mid(self.player.rect.center)
                    self.soundChannel_explosion.play(random.choice(expl_snds))
                    self.game_sprites.add(death_expl)
                    self.player.kill()
            if not self.player.alive() and not death_expl.alive():
                self.updateFile()
                game_running = False

            hits2 = pg.sprite.spritecollide(self.player, self.pow_sprites, True, pg.sprite.collide_mask)
            for hit in hits2:
                if hit.type == 3:
                    self.player.shield += random.randrange(10, 15)
                    if self.player.shield >= 100:
                        self.player.shield = 100
                if hit.type == 2:
                    self.player.powerup()
                if hit.type == 1:
                    self.player.powerup_2()

            self.screen.fill(BLACK)
            self.game_sprites.draw(self.screen)
            self.shield_bar(5, 5, self.player.shield)
            self.draw_text(str(self.score), 20, WIDTH / 2, 10, FONT[0], WHITE, True, 3)
            self.draw_text(str(self.coin_count), 20, 445, 0, FONT[0], WHITE, True, 2)
            pg.display.flip()

    def main_menu(self):
        '''running bool'''
        self.game_running = False
        self.option_running = False
        self.shop_running = False
        self.credits_running = False
        self.help_running = False
        '''sprite groups'''
        self.menu_sprites = pg.sprite.Group()
        menu_but = [
            Button_1(self, 0, (WIDTH / 2, 270)),
            Button_1(self, 2, (WIDTH / 2 + 2, 335)),
            Button_1(self, 4, (WIDTH / 2 + 2, 400)),
            Button_1(self, 6, (WIDTH / 2, 465)),
            Button_1(self, 10, (WIDTH - 40, HEIGHT - 40))
        ]
        for i in menu_but:
            self.menu_sprites.add(i)
        waiting = True
        while waiting:
            self.screen.fill(BLACK)
            title = pg.image.load("cov.png").convert()
            title.set_colorkey(BLACK)
            self.screen.blit(title, (WIDTH / 2 - 160, 130))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                if menu_but[0].is_clicked(event, 1, 0):
                    self.game_running = True
                    waiting = False
                if menu_but[1].is_clicked(event, 3, 2):
                    self.option()
                if menu_but[2].is_clicked(event, 5, 4):
                    self.shop()
                if menu_but[3].is_clicked(event, 7, 6):
                    self.credits()
                if menu_but[4].is_clicked(event, 11, 10):
                    self.help()

            self.menu_sprites.draw(self.screen)
            pg.display.update()
            pg.display.flip()
            self.clock.tick(FPS_MIN)

    def go_screen(self):
        self.go_sprites = pg.sprite.Group()
        go_but_list = [
            Button_1(self, 8, (WIDTH / 2, 370)),
            Button_1(self, 12, (WIDTH / 2, 315)),
        ]
        for i in go_but_list:
            self.go_sprites.add(i)
        waiting = True

        while waiting:
            self.screen.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.updateFile()
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pass
                if go_but_list[0].is_clicked(event, 9, 8):
                    waiting = False
                if go_but_list[1].is_clicked(event, 13, 12):
                    self.start_game()
            self.draw_text("GAME", 60, WIDTH / 2, 180, FONT[0], WHITE, True, 3)
            self.draw_text("OVER", 60, WIDTH / 2, 230, FONT[0], WHITE, True, 3)
            self.high_score_check()
            self.go_sprites.draw(self.screen)
            pg.display.update()
            self.clock.tick(FPS_MIN)

    def high_score_check(self):
        with open(results_data, 'r') as score_open:
            score_readline = score_open.readlines()
            last = int(score_readline[0])
        if last <= int(self.score):
            self.draw_text("NEW HIGH SCORE!", 30, WIDTH / 2, 450, FONT[0], WHITE, True, 3)
            self.draw_text(str(self.score), 25, WIDTH / 2, 480, FONT[0], WHITE, True, 3)
        elif last > int(self.score):
            self.draw_text("SCORE: " + str(self.score), 25, WIDTH / 2, 450, FONT[0], WHITE, True, 3)
            self.draw_text("HIGH SCORE: " + str(last), 20, WIDTH / 2, 480, FONT[0], WHITE, True, 3)
            return self.score
        score_open.close()
        return last

    def option(self):
        sett_sprites = pg.sprite.Group()
        m_onoff = Music_onoff_but(self, 0, (WIDTH / 2, 210))
        s_onoff = Sound_onoff_but(self, 0, (WIDTH / 2, 405))
        back = Button_1(self, 8, (35, 560))
        reset = Button_1(self, 14, (400, 560))
        sett_list = [
            m_onoff,
            s_onoff,
            back,
            reset
        ]
        for i in sett_list:
            sett_sprites.add(i)
        waiting = True
        slid1 = pg.Rect(270, 250, 30, 40)
        slid2 = pg.Rect(270, 440, 30, 40)
        while waiting:
            self.screen.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                m_onoff.is_clicked(event, 1, 0)
                s_onoff.is_clicked(event, 1, 0)
                if reset.is_clicked(event, 15, 14):
                    with open(results_data, 'r') as score_open:
                        score_readline = score_open.readlines()
                        score_readline[0] = str(0) + "\n"
                        score_readline[1] = str(0) + "\n"
                    with open(results_data, 'w') as score_open:
                        score_open.writelines(score_readline)
                    score_open.close()
                if back.is_clicked(event, 9, 8):
                    waiting = False
            slid_box = pg.Rect(WIDTH / 2 - 75, 250, 150, 40)
            slid_box2 = pg.Rect(WIDTH / 2 - 75, 440, 150, 40)
            but_slid = slid1
            but_slid2 = slid2
            inbi_box = pg.Rect(0, HEIGHT / 2 - 60, 450, 60)
            inbi_box2 = pg.Rect(0, 430, 450, 60)
            mx, my = pg.mouse.get_pos()
            button = pg.mouse.get_pressed()
            if button[0] != 0 and inbi_box.collidepoint((mx, my)):
                x = mx
                a = x - 10
                if a <= 150:
                    a = 150
                if a >= 270:
                    a = 270
                n = a - 150
                b = n / 120
                self.increase_volume(b)
                new = pg.Rect(a, 250, 30, 40)
                slid1 = new

            if button[0] != 0 and inbi_box2.collidepoint((mx, my)):
                x = mx
                a = x - 10
                if a <= 150:
                    a = 150
                if a >= 270:
                    a = 270
                n = a - 150
                b = n / 120
                self.increase_volume2(b)
                new = pg.Rect(a, 440, 30, 40)
                slid2 = new

            if pg.mixer.music.get_volume() > 0:
                a = pg.mixer.music.get_volume()
                b = a * 120
                c = b + 150
                if c <= 150:
                    c = 150
                if c >= 270:
                    c = 270
                new = pg.Rect(c, 250, 30, 40)
                slid1 = new
            elif pg.mixer.music.get_volume() <= 0:
                a = pg.mixer.music.get_volume()
                b = a * 120
                c = b + 150
                if c <= 150:
                    c = 150
                if c >= 270:
                    c = 270
                new = pg.Rect(c, 250, 30, 40)
                slid1 = new

            if pg.mixer.Channel(0).get_volume() > 0:
                a = pg.mixer.Channel(0).get_volume()
                b = a * 120
                c = b + 150
                if c <= 150:
                    c = 150
                if c >= 270:
                    c = 270
                new = pg.Rect(c, 440, 30, 40)
                slid2 = new
            elif pg.mixer.Channel(0).get_volume() <= 0:
                a = pg.mixer.Channel(0).get_volume()
                b = a * 120
                c = b + 150
                if c <= 150:
                    c = 150
                if c >= 270:
                    c = 270
                new = pg.Rect(c, 440, 30, 40)
                slid2 = new
            self.draw_text("MUSIC", 50, WIDTH / 2, 145, FONT[0], WHITE, True, 3)
            self.draw_text("SOUND", 50, WIDTH / 2, 345, FONT[0], WHITE, True, 3)
            sett_sprites.draw(self.screen)
            pg.draw.rect(self.screen, WHITE, slid_box, 2)
            pg.draw.rect(self.screen, WHITE, but_slid)
            pg.draw.rect(self.screen, WHITE, slid_box2, 2)
            pg.draw.rect(self.screen, WHITE, but_slid2)
            pg.display.update()
            self.clock.tick(FPS_MAIN)

    def shop(self):
        ship1 = Player_shop(0, (WIDTH / 4, 200))
        ship2 = Player_shop(64, (WIDTH / 4, 270))
        ship3 = Player_shop(128, (WIDTH / 4, 340))
        ship4 = Player_shop(192, (WIDTH / 4, 410))
        select_1 = Select_but(0, (WIDTH * 3 / 4, 200))
        select_2 = Select_but(0, (WIDTH * 3 / 4, 270))
        select_3 = Select_but(0, (WIDTH * 3 / 4, 340))
        select_4 = Select_but(0, (WIDTH * 3 / 4, 410))
        self.shop_sprite = pg.sprite.Group()
        shop_list = [
            ship1,
            ship2,
            ship3,
            ship4,
            select_1,
            select_3,
            select_2,
            select_4
        ]
        for i in shop_list:
            self.shop_sprite.add(i)
        waiting = True
        back = Button_1(self, 8, (35, 560))
        self.shop_sprite.add(back)
        while waiting:
            self.screen.fill(BLACK)
            open_user_data = open(results_data, 'r')
            read_user_data = open_user_data.readlines()
            prev_coin_count = read_user_data[1]
            coin_count = int(prev_coin_count)
            coin_dis1 = Coin_display((WIDTH / 2 - len(str(coin_count)) * 12, 100), str(coin_count), 30)
            open_text_mes = open(user_data, 'r')
            read_text_mes = open_text_mes.readlines()
            prev_text_mes = read_text_mes[7]
            show_txt = str(prev_text_mes)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.updateFile()
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                if back.is_clicked(event, 9, 8):
                    waiting = False
                select_1.is_clicked(event, 1, 0, "0\n", "Batoidea selected", "NULL", 0, 3)
                select_2.is_clicked(event, 1, 0, "1\n", "Dictator selected", "Sorry, it cost 4,000 coins",
                                    4000, 4)
                select_3.is_clicked(event, 1, 0, "2\n", "Limulidae selected",
                                    "Sorry, it cost 10,000 coins", 10000, 5)
                select_4.is_clicked(event, 1, 0, "3\n", "The eggplant selected",
                                    "Sorry, it cost 100,000 coins", 100000, 6)
            self.draw_text("Batoidea", 14, WIDTH / 2, 200, FONT[0], WHITE, True, 3)
            self.draw_text("Dictator", 14, WIDTH / 2, 270, FONT[0], WHITE, True, 3)
            self.draw_text("Limulidae", 14, WIDTH / 2, 340, FONT[0], WHITE, True, 3)
            self.draw_text("The eggplant", 14, WIDTH / 2, 410, FONT[0], WHITE, True, 3)
            self.draw_text(show_txt, 16, WIDTH / 2, 480, FONT[0], WHITE, True, 3)
            coin_dis1.draw(self.screen)

            self.shop_sprite.draw(self.screen)
            self.shop_sprite.update()
            pg.display.flip()
            pg.display.update()
            self.clock.tick(FPS_MAIN)

    def credits(self):
        waiting = True
        back = Button_1(self, 8, (35, 560))
        while waiting:
            self.screen.fill(BLACK)
            self.draw_text("zak dion lyon", 30, WIDTH / 2, 240, FONT[0], WHITE, True, 3)
            self.draw_text("Music", 20, WIDTH / 2, 310, FONT[0], WHITE, True, 3)
            self.draw_text("Waka Flocka Flame - Game On Pixels Retro Remix", 12, WIDTH / 2, 340, FONT[0], WHITE, True,
                           3)
            self.draw_text("Sunchipp Studio", 14, WIDTH / 2, 360, FONT[0], WHITE, True,
                           3)
            self.draw_text("Annex", 20, WIDTH / 2, 410, FONT[0], WHITE, True,
                           3)
            self.draw_text("Jason Kottke", 12, WIDTH / 2, 440, FONT[0], WHITE, True, 3)
            self.draw_text("morgan3d", 12, WIDTH / 2, 460, FONT[0], WHITE, True,
                           3)
            img = pg.image.load('ZAKDIONLYON.png').convert()
            img.set_colorkey(BLACK)
            img_scale = pg.transform.scale(img, (100, 100))
            self.screen.blit(img_scale, (WIDTH / 2 - 50, 110))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                if back.is_clicked(event, 9, 8):
                    waiting = False
            back.draw(self.screen)
            pg.display.update()
            self.clock.tick(FPS_MIN)

    def help(self):
        waiting = True
        back = Button_1(self, 8, (35, 560))
        while waiting:
            self.screen.fill(BLACK)
            img = pg.image.load('Instra.png').convert()
            img.set_colorkey(BLACK)
            self.screen.blit(img, (0, 0))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                if back.is_clicked(event, 9, 8):
                    waiting = False
            back.draw(self.screen)
            pg.display.update()
            self.clock.tick(FPS_MIN)


g = Game()

g.main_menu()

while g.game_running:
    g.start_game()
    g.go_screen()
    g.main_menu()

pg.quit()
