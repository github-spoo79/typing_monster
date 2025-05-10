import pygame
from config import Config as cfg
from util import Util as util

class Resources:
    def __init__(self):
        self.zombie_walk_images = util.render_sheet("zombie_walk_sheet.png", 51, 84, 7, 1)
        self.zombie_die_images = util.render_sheet("zombie_die_sheet.png", 51, 84, 8, 1)
        self.zombie_attack_images = util.render_sheet("zombie_attack_sheet.png", 51, 84, 7, 1)
                        
        self.zombie_woman_walk_images = util.render_sheet("zombie_woman_walk_sheet.png", 57, 93, 7, 1)
        self.zombie_woman_die_images = util.render_sheet("zombie_woman_die_sheet.png", 57, 93, 7, 1)
        self.zombie_woman_attack_images = util.render_sheet("zombie_woman_attack_sheet.png", 57, 93, 7, 1)
        
        self.player_idle_images = util.render_sheet("solider_idle_sheet.png", 72, 93, 7, 1)        
        self.player_left_attack_images = util.render_sheet("solider_left_attack_sheet.png", 72, 93, 8, 1)
        self.player_right_attack_images = util.render_sheet("solider_right_attack_sheet.png", 72, 93, 8, 1)
        self.player_death_images = util.render_sheet("solider_death_sheet.png", 72, 93, 7, 1)
        
        self.fence_middle_images = util.render_sheet("fence_middle.png", 90, 125, 7, 2)
                
        self.menu_bar = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "menu_bar.wav")
        self.menu_bar.set_volume(0.3)
        self.menu_negative_bar = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "menu_negative_bar.wav")
        self.menu_negative_bar.set_volume(0.3)
        self.machinegun = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "machinegun.wav")
        self.machinegun.set_volume(0.3)
        self.male_scream = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "male_scream.wav")
        self.male_scream.set_volume(0.3)
        self.female_scream = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "female_scream.wav")
        self.female_scream.set_volume(0.3)
        self.crash = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "crash.wav")
        self.crash.set_volume(0.3)
        self.stage_up = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "stage_up.wav")
        self.stage_up.set_volume(0.3)
        self.player_scream = pygame.mixer.Sound(cfg.GAME_SOUND_DIR + "player_scream.ogg")
        self.player_scream.set_volume(0.3)

        self.font24 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 24)
        self.font30 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 30)
        self.font32 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 32)
        self.font34 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 34)
        self.font48 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 48)
        self.font54 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 54)
        self.font72 = pygame.font.Font(cfg.GAME_FONT_DIR + "HBIOS-SYS.ttf", 72)
        self.stage_info = util.load_json(cfg.GAME_DATA_DIR + "stage.dat")
        self.env_info = util.load_json(cfg.GAME_DATA_DIR + "env.dat")

    def sfx_set_volume(self, sfx_vol):
        self.menu_bar.set_volume(sfx_vol)
        self.menu_negative_bar.set_volume(sfx_vol)
        self.machinegun.set_volume(sfx_vol)
        self.male_scream.set_volume(sfx_vol)
        self.female_scream.set_volume(sfx_vol)
        self.crash.set_volume(sfx_vol)
        self.stage_up.set_volume(sfx_vol)
        self.player_scream.set_volume(sfx_vol)
        self.male_scream.play()

        