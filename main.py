import pygame
import sys
import time
from config import Config as cfg
from player import PlayerText, Player, Cartridge
from background import Background
from resources import Resources
from barrier import Barrier
from sap import SAP
from spawn import Spawn
from util import Util

class Main():
    def __init__(self):     
        pygame.mixer.pre_init(44100, -16, 2, 512)  
        pygame.init()        
        pygame.mixer.set_num_channels(cfg.MAX_MIXER)  # 동시에 재생할 수 있는 채널 수 증가
        
        pygame.display.set_caption("Typing Monster")        
        icon = pygame.image.load(cfg.GAME_DIR + "\keycab.ico")
        pygame.display.set_icon(icon)

        self.screen = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        self.background_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.player_text_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.enemy_text_sprites = pygame.sprite.Group()
        self.barrier_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()

        self.orig_stage_idx = 0
        self.resources = Resources()
        self.typing_speed = 0
        self.typing_correct_cnt = 0
        self.typing_error_cnt = 0
        self.typing_speed_avg = 0
        self.typing_total_speed = 0
        self.stage_hit_goal_cnt = 0
        self.stage_hit_cnt = 0

        self.background = Background()
        self.sap = SAP()
        self.clock = pygame.time.Clock()
        self.spawn = None
        self.game_status = cfg.GAME_MENU
        self.menu_idx = 0
        self.try_again = True
        self.ing = True
        self.menu_ing = True
        self.game_ending = False
        self.warning_message = False

        self.bgm_vol = self.resources.env_info["bgm_vol"]
        self.sfx_vol = self.resources.env_info["sfx_vol"]
        self.stage_idx = self.resources.env_info["stage_idx"]

    def reset(self):

        self.screen.fill((0, 0, 0))
        self.player_sprites.empty()
        self.player_text_sprites.empty()
        self.enemy_sprites.empty()
        self.enemy_text_sprites.empty()
        self.barrier_sprites.empty()

        self.typing_speed = 0
        self.typing_correct_cnt = 0
        self.typing_error_cnt = 0
        self.typing_speed_avg = 0
        self.typing_total_speed = 0
        self.stage_hit_cnt = 0
        self.stage_hit_goal_cnt = self.resources.stage_info[self.stage_idx]["mobCnt"]
        self.try_again = True
        self.ing = True
        self.spawn = Spawn(self.stage_idx, self.resources.stage_info)
        self.init_barrier()

    def menu(self):
        pygame.mixer.music.load(cfg.GAME_SOUND_DIR + "house_in_a_forest_loop.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)
        self.stage_no = self.resources.stage_info[self.stage_idx]["stage"]
        self.stage_hit_goal_cnt = self.resources.stage_info[self.stage_idx]["mobCnt"]
        self.spawn = Spawn(self.stage_idx, self.resources.stage_info)

        while self.menu_ing:
            self.clock.tick(cfg.FPS)
            
            self.background.draw_tile(self.screen)
            self.spawn.spawn_mob(self) 

            sorted_sprites = sorted(self.enemy_sprites.sprites(), key=lambda sprite: sprite.rect.y)
            self.enemy_sprites = pygame.sprite.Group(*sorted_sprites)
            self.enemy_sprites.update()
            self.enemy_sprites.draw(self.screen)
            
            self.enemy_text_sprites.update()
            self.enemy_text_sprites.draw(self.screen)

            if self.game_status == cfg.GAME_ENVIORMENT:
                self.display_game_env()
            elif self.game_status == cfg.GAME_MENU:
                self.display_game_menu()
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                    
                    self.menu_ing = False
                    self.game_status = cfg.GAME_END

                if self.game_status == cfg.GAME_ENVIORMENT:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu_idx = (self.menu_idx - 1) % len(cfg.ENV_ITEM)

                        elif event.key == pygame.K_DOWN:
                            self.menu_idx = (self.menu_idx + 1) % len(cfg.ENV_ITEM)

                        elif event.key == pygame.K_LEFT and self.menu_idx == 0:
                            self.bgm_vol -= 0.1 if self.bgm_vol > 0 else 0
                            pygame.mixer.music.set_volume(self.bgm_vol)

                        elif event.key == pygame.K_RIGHT and self.menu_idx == 0:
                            self.bgm_vol += 0.1 if self.bgm_vol < 1.0 else 0
                            pygame.mixer.music.set_volume(self.bgm_vol)

                        elif event.key == pygame.K_LEFT and self.menu_idx == 1:
                            self.sfx_vol -= 0.1 if self.sfx_vol > 0 else 0
                            self.resources.sfx_set_volume(self.sfx_vol)

                        elif event.key == pygame.K_RIGHT and self.menu_idx == 1:
                            self.sfx_vol += 0.1 if self.sfx_vol < 1.0 else 0
                            self.resources.sfx_set_volume(self.sfx_vol)

                        if event.key == pygame.K_RETURN:
                            if self.menu_idx == 2:
                                self.menu_idx = 0
                                self.game_status = cfg.GAME_MENU
                                self.resources.env_info["bgm_vol"] = self.bgm_vol
                                self.resources.env_info["sfx_vol"] = self.sfx_vol
                                Util.save_json(self.resources.env_info, cfg.GAME_DATA_DIR + "env.dat")
                                self.display_game_menu()

                elif self.game_status == cfg.GAME_MENU:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.menu_idx = (self.menu_idx - 1) % len(cfg.MENU_ITEM)
                        elif event.key == pygame.K_DOWN:
                            self.menu_idx = (self.menu_idx + 1) % len(cfg.MENU_ITEM)
                        elif event.key == pygame.K_LEFT and self.menu_idx == 0:
                            self.orig_stage_idx = self.stage_idx
                            self.stage_idx -= 1 if self.stage_idx > 0 else 0
                        elif event.key == pygame.K_RIGHT and self.menu_idx == 0:
                            self.orig_stage_idx = self.stage_idx
                            self.stage_idx += 1 if self.stage_idx < len(self.resources.stage_info) - 1 else 0

                        self.stage_no = self.resources.stage_info[self.stage_idx]["stage"]
                        self.openYn = self.resources.stage_info[self.stage_idx]["openYn"]
                        if self.openYn == "N":
                            self.warning_message = True
                            self.stage_idx = self.orig_stage_idx
                            self.stage_no = self.resources.stage_info[self.stage_idx]["stage"]
                            self.resources.menu_negative_bar.play()
                        else:
                            self.warning_message = False
                            self.resources.menu_bar.play()


                        if event.key == pygame.K_RETURN:
                            if self.menu_idx == 3:
                                self.menu_ing = False
                                self.game_status = cfg.GAME_END
                                self.resources.env_info["bgm_vol"] = self.bgm_vol
                                self.resources.env_info["sfx_vol"] = self.sfx_vol
                                self.resources.env_info["stage_idx"] = self.stage_idx
                                Util.save_json(self.resources.env_info, cfg.GAME_DATA_DIR + "env.dat")

                            elif self.menu_idx == 2:
                                self.game_status = cfg.GAME_ENVIORMENT
                                self.menu_idx = 0
                                self.display_game_env()

                            elif self.menu_idx == 0 or self.menu_idx == 1:                                
                                self.stage_no = self.resources.stage_info[self.stage_idx]["stage"]
                                self.stage_hit_goal_cnt = self.resources.stage_info[self.stage_idx]["mobCnt"]
                                self.spawn.init_stage(self.stage_idx)
                                self.game_status = cfg.GAME_PLAYING
                                self.menu_ing = False
                                self.resources.env_info["bgm_vol"] = self.bgm_vol
                                self.resources.env_info["sfx_vol"] = self.sfx_vol
                                self.resources.env_info["stage_idx"] = self.stage_idx
                                Util.save_json(self.resources.env_info, cfg.GAME_DATA_DIR + "env.dat")
                                self.reset()

            pygame.display.flip()

    def play(self):
        idle = self.resources.player_idle_images
        left_attack = self.resources.player_left_attack_images
        right_attack = self.resources.player_right_attack_images
        death = self.resources.player_death_images

        self.player = Player(self, cfg.START_POS, idle, left_attack, right_attack, death)
        self.player_text = PlayerText(self, cfg.START_TEXT_POS)
        self.player_sprites.add(self.player)
        self.player_text_sprites.add(self.player_text)
        self.spawn = Spawn(self.stage_idx, self.resources.stage_info)
        self.init_barrier()

        while self.ing:
            self.clock.tick(cfg.FPS)
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:                    
                    self.menu_ing = False
                    self.game_status = cfg.GAME_END

                if self.game_status == cfg.GAME_PLAYING or \
                    self.game_status == cfg.GAME_OVER:
                    if self.player.live:
                        self.player_text.key_event_handler(event)
                    else:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                                self.try_again = not(self.try_again)
                            
                            if event.key == pygame.K_RETURN:
                                if time.time() - self.player.death_time > 3:
                                    self.game_status = cfg.GAME_PLAYING if self.try_again else cfg.GAME_MENU
                                    self.ing = False
                                    if self.game_status == cfg.GAME_MENU:
                                        self.menu_ing = True

                            if event.key == pygame.K_SPACE:
                                if self.game_ending:
                                    self.try_again = False
                                    self.menu_ing = True
                                    self.ing = False
                                    self.game_ending = False
                                    self.game_status = cfg.GAME_MENU
            
            if self.game_status == cfg.GAME_PLAYING or \
                self.game_status == cfg.GAME_OVER:
                self.sap.add_sprites(self.player_sprites)
                self.sap.add_sprites(self.enemy_sprites)
                self.sap.add_sprites(self.barrier_sprites)

                self.sap.check_collision()
                self.spawn.spawn_mob(self)
                self.background.draw_tile(self.screen)

                self.display_stage()
                self.display_stage_goal()
                self.display_typing_speed()

                sorted_sprites = sorted(self.enemy_sprites.sprites(), key=lambda sprite: sprite.rect.y)
                self.enemy_sprites = pygame.sprite.Group(*sorted_sprites)
                self.enemy_sprites.update()
                self.enemy_sprites.draw(self.screen)
                
                self.enemy_text_sprites.update()
                self.enemy_text_sprites.draw(self.screen)

                self.player_sprites.update()
                self.player_sprites.draw(self.screen)
                
                self.player_text_sprites.update()
                self.player_text_sprites.draw(self.screen)
                
                self.background.draw_fence(self.screen)
                
                self.barrier_sprites.update()
                self.barrier_sprites.draw(self.screen)

                self.effect_sprites.update()
                self.effect_sprites.draw(self.screen)

                if self.game_ending:                    
                    self.display_game_ending()

            
            if self.game_status == cfg.GAME_OVER:
                if time.time() - self.player.death_time > 3:
                    self.display_game_over()
                
            pygame.display.flip()
            
            if self.game_status == cfg.GAME_END:
                self.ing = False

    def display_game_ending(self):
        text_surface = self.resources.font54.render("축하드립니다.", True, cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = 280
        self.screen.blit(text_surface, text_rect) 
        
        text_surface = self.resources.font30.render("좀비로부터 당신은 생존했습니다.", True, cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = 350
        self.screen.blit(text_surface, text_rect) 

        text_surface = self.resources.font30.render("Spacebar를 누르면 메뉴로 돌아갑니다.", True, cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = 400
        self.screen.blit(text_surface, text_rect) 

    def display_game_env(self):
        text_surface = self.resources.font54.render("타이핑 몬스터", True, cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = 150
        self.screen.blit(text_surface, text_rect) 

        for i, (text, y) in enumerate(cfg.ENV_ITEM):
            color = cfg.YELLOW if i == self.menu_idx else cfg.WHITE
            if i == 0:
                text_surface = self.resources.font34.render(text.format(int(self.bgm_vol * 10)), True, color)
            elif i == 1:
                text_surface = self.resources.font34.render(text.format(int(self.sfx_vol * 10)), True, color)
            else:
                text_surface = self.resources.font34.render(text, True, color)

            text_rect = text_surface.get_rect()
            text_rect.centerx = cfg.SCREEN_WIDTH / 2
            text_rect.centery = y + 200
            self.screen.blit(text_surface, text_rect)

    def display_game_menu(self):
        text_surface = self.resources.font54.render("타이핑 몬스터", True, cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = 150
        self.screen.blit(text_surface, text_rect) 

        for i, (text, y) in enumerate(cfg.MENU_ITEM):
            color = cfg.YELLOW if i == self.menu_idx else cfg.WHITE
            if i == 0:
                text_surface = self.resources.font34.render(text.format(self.stage_no), True, color)
            else:
                text_surface = self.resources.font34.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = cfg.SCREEN_WIDTH / 2
            text_rect.centery = y + 200
            self.screen.blit(text_surface, text_rect)

        if self.warning_message:
            text_surface = self.resources.font24.render("스테이지 {0}을 아직 클리어하지 못했습니다.".format(self.stage_no), True, cfg.YELLOW)
            text_rect = text_surface.get_rect()
            text_rect.centerx = cfg.SCREEN_WIDTH / 2
            text_rect.centery = 700
            self.screen.blit(text_surface, text_rect) 

    def display_game_over(self):
        text_surface = self.resources.font72.render("GAME OVER", True, cfg.RED)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = cfg.SCREEN_HEIGHT / 2 - 150
        self.screen.blit(text_surface, text_rect) 

        text_surface = self.resources.font48.render("Try Again?", True, cfg.RED)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2
        text_rect.centery = cfg.SCREEN_HEIGHT / 2 - 60
        self.screen.blit(text_surface, text_rect) 

        text_surface = self.resources.font48.render("Yes", True, cfg.WHITE if self.try_again else cfg.RED)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2 - 50
        text_rect.centery = cfg.SCREEN_HEIGHT / 2 - 5
        self.screen.blit(text_surface, text_rect) 

        text_surface = self.resources.font48.render("No", True, cfg.RED if self.try_again else cfg.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.centerx = cfg.SCREEN_WIDTH / 2 + 50
        text_rect.centery = cfg.SCREEN_HEIGHT / 2 - 5
        self.screen.blit(text_surface, text_rect) 
            
    def display_stage_goal(self):
        text_stage_goal = "{0} / {1}".format(self.stage_hit_cnt, self.stage_hit_goal_cnt)        
        text_surface = self.resources.font24.render(text_stage_goal, True, cfg.WHITE)
        self.screen.blit(text_surface, (580, 670)) 

    def display_stage(self):
        if not(self.game_ending):
            text_typing_speed = "STAGE {0}".format(self.stage_no)
            text_surface = self.resources.font54.render(text_typing_speed, True, cfg.WHITE)
            text_rect = text_surface.get_rect()
            text_rect.centerx = cfg.SCREEN_WIDTH / 2
            text_rect.top = 10
            self.screen.blit(text_surface, text_rect) 
    
    def display_typing_speed(self):
        text_typing_speed = "타수(분) {0}".format(self.typing_speed)
        text_surface = self.resources.font24.render(text_typing_speed, True, cfg.WHITE)
        self.screen.blit(text_surface, (580, 700)) 

        text_typing_speed_avg = "평균(분) {0}".format(self.typing_speed_avg)
        text_surface = self.resources.font24.render(text_typing_speed_avg, True, cfg.WHITE)
        self.screen.blit(text_surface, (580, 730)) 

        if self.typing_correct_cnt > 0:
            correct_rate = round((self.typing_correct_cnt / (self.typing_correct_cnt + self.typing_error_cnt)) * 100, 2)
        else:
            correct_rate = 0
        text_correct_rate = "정확도(%) : {0}".format(correct_rate)
        text_surface = self.resources.font24.render(text_correct_rate, True, cfg.WHITE)
        self.screen.blit(text_surface, (580, 760)) 
            
    def check_hit(self, text, typing_speed):
        if text == "":
            return
        
        hit_yn = False
        for e in self.enemy_text_sprites:
            if e.text == text:                
                hit_yn = True
                e.destroy()
                if e.rect.centerx >= cfg.SCREEN_WIDTH / 2:
                    self.player.attack("RIGHT")
                    cartridge_x = self.player.rect.centerx + 20
                    cartridge_y = self.player.rect.centery + 3
                    self.spawn_cartridge(cartridge_x, cartridge_y, 1)
                    self.resources.machinegun.play()
                else:
                    self.player.attack("LEFT")
                    cartridge_x = self.player.rect.centerx - 20
                    cartridge_y = self.player.rect.centery + 3
                    self.spawn_cartridge(cartridge_x, cartridge_y, -1)
                    self.resources.machinegun.play()
                break

        if hit_yn:
            self.stage_hit_cnt += 1
            self.typing_correct_cnt += 1
            self.typing_speed = typing_speed
            self.typing_total_speed += typing_speed
            self.typing_speed_avg = round(self.typing_total_speed / self.typing_correct_cnt, 2)
            if self.stage_hit_cnt >= self.stage_hit_goal_cnt:
                if self.stage_idx < len(self.resources.stage_info) - 1:
                    self.stage_idx += 1
                    self.stage_no = self.resources.stage_info[self.stage_idx]["stage"]
                    self.stage_hit_goal_cnt = self.resources.stage_info[self.stage_idx]["mobCnt"]
                    self.stage_hit_cnt = 0
                    self.resources.stage_up.play()
                    self.spawn.next_stage()
                else:
                    self.game_clear()

        else:
            self.typing_error_cnt += 1

    def spawn_cartridge(self, x, y, dir):
        delay_time = 0
        for _ in range(3):            
            self.effect_sprites.add(Cartridge(x, y, delay_time, dir))
            delay_time += 0.1

    def game_clear(self):
        self.spawn.stop_spawn_mob()
        for e in self.enemy_text_sprites:
            e.destroy()
        self.game_ending = True
        self.player.live = False

    def init_barrier(self):
        for i in range(cfg.BARRIER_COUNT):            
            self.barrier_sprites.add(Barrier(self, self.resources.fence_middle_images
                                                 , (cfg.BARRIER_WIDTH * i, cfg.BARRIER_Y)
                                                 , self.resources.crash))

if __name__ == "__main__":    
    gameMain = Main()    
    while True:
        gameMain.menu()
        gameMain.play()
        if gameMain.game_status == cfg.GAME_END:
            break
        else:
            gameMain.reset()
    pygame.quit()
    sys.exit()
        
