from __future__ import annotations
from menu.menus import Menu
from tower.towers import Tower
from enemy.enemies import EnemyGroup
import pygame
from settings import *
from color_settings import *
import math
from event.event_setting import *
from pygame import mixer



class GameView:
    def __init__(self,player:int):
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        
        self.player = player
    def draw_stage(self,stage:int):
        font = pygame.font.Font(FONT, 22)
        text = font.render('level  ' + str(stage), True, WHITE)
        text_rect = text.get_rect(midright=(300, 535))
        self.win.blit(text, text_rect)
    
    def draw_progress(self,num:int,total:int):
        self.win.blit(PROGRESS_LINE,(350,525))  #進度條的底
        color = (210, 209, 209)
        pygame.draw.rect(self.win, color, pygame.Rect(358, 532, 305 * num / total, 13))  # 劃出進度條(起點X, 起點Y, 寬度, 高度)
        self.win.blit(pygame.transform.scale(ENEMY_IMAGE1[self.player], (37, 48)),((350 + 305 * num / total), 526 - 18))  # enemy icon
        
    def draw_bg(self):
        self.win.blit(BACKGROUND_IMAGE[self.player], (0, 0))
    def draw_wait(self,wait:int):
        font = pygame.font.Font(FONT, 100)
        text = font.render(str(wait), True, BROWNGRAY)
        text_rect = text.get_rect()
        surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
        transparency = 200
        pygame.draw.circle(surface, (244, 244, 244, transparency), (512,300),139)
        self.win.blit(surface, (0, 0))
        text_rect.center = (512,300)
        self.win.blit(text, text_rect)

    def draw_notify(self,after,before:pygame.Surface,had_occur,shrink=SHRINK_IMAGE, y=580):
        if had_occur:
            if after.get_height()>800:
                notify_image = pygame.transform.scale(after,(180,180))
                notify_image_rect = notify_image.get_rect()
                notify_image_rect.center = (120,485-8)
            else:
                notify_image = pygame.transform.scale(after,(180,160))
                notify_image_rect = notify_image.get_rect()
                notify_image_rect.center = (120,475-8)
            self.win.blit(notify_image,notify_image_rect)
        else:
            notify_image = pygame.transform.scale(before,(180,160))
            notify_image_rect = notify_image.get_rect()
            notify_image_rect.center = (120,475-8)
            self.win.blit(notify_image,notify_image_rect)
        # shrink_animation
        shrink_image = pygame.transform.scale(shrink, (129, 11))
        shrink_image_rect = shrink_image.get_rect()
        shrink_image_rect.center = (118, y)
        self.win.blit(shrink_image, shrink_image_rect)


    def draw_enemies(self, enemies:EnemyGroup):
        for en in enemies.get():
            
            if en.slow_count < en.slow_max:
                en.ice_rect.centerx, en.ice_rect.centery = en.rect.centerx+10,en.rect.centery+10 
                self.win.blit(en.ice,en.ice_rect)
            self.win.blit(en.image, en.rect)
            # draw health bar
            bar_width = en.rect.w * (en.health / en.max_health)
            max_bar_width = en.rect.w
            bar_height = 5
            pygame.draw.rect(self.win, RED, [en.rect.x, en.rect.y - 10, max_bar_width, bar_height])
            pygame.draw.rect(self.win, GREEN, [en.rect.x, en.rect.y - 10, bar_width, bar_height])
    def draw_bullets(self,bullets):
        for bullet in bullets.get():
            self.win.blit(bullet.image,bullet.rect)
    def draw_towers(self, towers:list):
        # draw tower
        for tw in towers:
            self.win.blit(tw.image, tw.rect)

    def draw_range(self, selected_tower:Tower):
        # draw tower range
        if selected_tower is not None:
            tw = selected_tower
            # create a special surface that is able to render semi-transparent image
            surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            transparency = 26
            pygame.draw.circle(surface, (244, 244, 244, transparency), tw.rect.center, tw.range)
            self.win.blit(surface, (0, 0))

    def draw_menu(self, menu:Menu):
        self.win.blit(menu.image, menu.rect)
        for btn in menu.buttons:
            self.win.blit(btn.image, btn.rect)

    def draw_plots(self, plots:list):
        for pt in plots:
            self.win.blit(pt.image, pt.rect)

    def draw_money(self, money: int):
        money_menu_image = MONEY_MENU_IMAGE
        money_menu_image_rect = money_menu_image.get_rect()
        money_menu_image_rect.center = (815, 22)
        self.win.blit(money_menu_image, money_menu_image_rect.center)
        # draw money
        font = pygame.font.Font(FONT, 22)
        text = font.render('# ' + str(money), True, BROWNGRAY)
        text_rect = text.get_rect(midright=(960, 46))
        self.win.blit(text, text_rect)
    def draw_tower_money(self, tower_money: int):
        money_menu_image = TOWER_MONEY_MENU_IMAGE
        money_menu_image_rect = money_menu_image.get_rect()
        money_menu_image_rect.center = (615, 22)
        self.win.blit(money_menu_image, money_menu_image_rect.center)
        # draw tower money
        font = pygame.font.Font(FONT, 22)
        text = font.render('* ' + str(tower_money), True, BROWNGRAY)
        text_rect = text.get_rect(midright=(750, 46))
        self.win.blit(text, text_rect)
    
    def draw_main_menu(self,main_menu:list,mute:bool,pause:bool,ability:bool):
        self.win.blit(main_menu[4].image,main_menu[4].rect)
        self.win.blit(main_menu[5].image,main_menu[5].rect)
        if ability:
            self.win.blit(main_menu[6].image,main_menu[6].rect)
            self.win.blit(main_menu[7].image,main_menu[7].rect)
        if mute:
            self.win.blit(main_menu[0].image,main_menu[0].rect)
        else:
            self.win.blit(main_menu[1].image,main_menu[1].rect)
        if pause:
            self.win.blit(main_menu[2].image,main_menu[2].rect)
        else:
            self.win.blit(main_menu[3].image,main_menu[3].rect)
        
  
    def draw_hp(self, hp:int,max_hp:int):
        # draw_lives
        hp_image_rect = HEART_FULL_IMAGE.get_rect()
        for i in range(1, 16, 2):
            hp_image_rect.center = (62 + ((i - 1) / 2) * (HEART_WIDTH + 13), 35 + (HEART_HEIGHT / 2))
            if i < hp:
                self.win.blit(HEART_FULL_IMAGE, hp_image_rect)
            elif i == hp:
                if hp == 0:
                    self.win.blit(HEART_EMPTY_IMAGE, hp_image_rect)
                else:
                    self.win.blit(HEART_HALF_IMAGE, hp_image_rect)
            else:
                self.win.blit(HEART_EMPTY_IMAGE, hp_image_rect)
    def draw_message(self, message, continue_btn, continue_btn_rect):
        self.win.blit(message, (0, 0))
        self.win.blit( continue_btn, continue_btn_rect)

