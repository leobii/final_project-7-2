from typing import Tuple
import pygame
import os

from pygame.mixer import pause
from tower.towers import Tower, Vacancy
from tower.bullets import BulletGroup
from enemy.enemies import EnemyGroup
from menu.menus import Menu, UpgradeMenu, BuildMenu, MainMenu
from game.user_request import RequestSubject, TowerFactory,  TowerDeveloper, TowerKiller,  Music,Show_Hide_Notify,Ability,Play
from settings import WIN_WIDTH, WIN_HEIGHT, BACKGROUND_IMAGE,TOWER_POSITION, MESSAGE_CONTINUE, SHRINK_IMAGE


class GameModel:
    def __init__(self,player:int):
        self.player = player
        # data
        self.bg_image = pygame.transform.scale(BACKGROUND_IMAGE[self.player], (WIN_WIDTH, WIN_HEIGHT))
        self.__towers = []
        self.__enemies = EnemyGroup(self.player)
        self.__menu = None
        self.__main_menu = MainMenu(self.player)
        
        self.__plots = []
        for pos in TOWER_POSITION[self.player]:
            x,y = pos
            self.__plots.append(Vacancy(x+20,y+20))
        
        self.__bullet = BulletGroup()
        self.message = None
        # selected item
        self.selected_plot = None
        self.selected_tower = None
        self.touched_tower = None
        self.selected_button = None
        self.selected_continue_game = False
        # apply observer pattern
        self.subject = RequestSubject(self)
        self.play_req = Play(self.subject)
        self.seller = TowerKiller()
        self.developer = TowerDeveloper(self.subject)
        self.factory = TowerFactory(self.subject)

        #self.muse = Muse(self.subject)
        self.music = Music(self.subject)
        self.ctrl_notify = Show_Hide_Notify(self.subject)
        self.ability = Ability(self.subject)
        #
        self.wave = 0
        self.money = 0
        self.tower_money = 0
        self.max_hp = 10
        self.hp = self.max_hp
        self.sound = pygame.mixer.Sound(os.path.join("music", "attack_se.wav"))
        self.notify = None
        self.notify2 = None
        self.had_occur = False
        self.show_notify = True
        self.mute = False
        self.pause = False
        self.stage = 0
        self.show_ability = False
        
        self.message_continue_rect = MESSAGE_CONTINUE.get_rect()
        self.message_continue_rect.center = (880, 421)
        self.message_move_count = 0
        self.message_move_max = 6

        self.click_to_shrink = SHRINK_IMAGE
        self.click_to_shrink_rect = SHRINK_IMAGE.get_rect()
        self.click_to_shrink_rect.center = (118, 580)
        self.click_message_move_count = 0
        self.click_message_move_max = 5
        
        self.add_clock = 0
        self.add_delay = 7
        self.add_interval = 1
        self.add_times = [0,0,0]
        self.add_amount = 1
        self.add_which = 0
        self.animate_state = "Undone"
        self.add_1 = [0,0,0]        #第一次的影響
        self.add_value = [0, 0, 0]
        self.add_2 = [0,0,0]        #突發事件的影響
        self.occur_time = 0

    def user_request(self, user_request: str):
        """ add tower, sell tower, upgrade tower"""
        self.subject.notify(user_request)

    def get_request(self, events: dict) -> str:
        """get keyboard response or button response"""
        # initial
        self.selected_button = None
        # key event
        if events["keyboard key"] is not None:
            return "start new wave"
        # mouse event
        if events["mouse position"] is not None:
            x, y = events["mouse position"]
            self.select(x, y)

            if self.selected_button is not None:
                return self.selected_button.response
            return "nothing"
        
        x,y = events["mouse move"]
        self.touch_tower(x,y)
            
        return "nothing"

    def touch_tower(self,x,y):
        for tw in self.__towers:
            if tw.touched(x, y):
                self.touched_tower = tw
                return
        self.touched_tower = None

    def select(self, mouse_x: int, mouse_y: int) -> None:
        """change the state of whether the items are selected"""
        # if the item is clicked, select the item
        for tw in self.__towers:
            if tw.clicked(mouse_x, mouse_y):
                self.selected_tower = tw
                self.selected_plot = None
                return
        for pt in self.__plots:
            if pt.clicked(mouse_x, mouse_y):
                self.selected_tower = None
                self.selected_plot = pt
                return
        for en in self.enemies.get():
            if en.clicked(mouse_x,mouse_y):
                #en.selected_count += 1
                if en.selected_count >= 5:
                    en.slow_count = 0
                    en.selected_count = 0
                else:
                    en.selected_count += 1
                break

        # if the button is clicked, get the button response.
        # and keep selecting the tower/plot.
        if self.__menu is not None:
            for btn in self.__menu.buttons:
                if btn.clicked(mouse_x, mouse_y):
                    self.selected_button = btn
            if self.selected_button is None:
                self.selected_tower = None
                self.selected_plot = None
        # menu btn
        for btn in self.__main_menu.buttons:
            if btn.clicked(mouse_x, mouse_y):
                self.selected_button = btn

        # when the mouse is clicked on continue in message window
        if self.message is not None and self.animate_state == "Done":
            if self.message_continue_rect.collidepoint(mouse_x, mouse_y):
                self.selected_continue_game = True
                self.animate_state = "Undone"
                self.add_which = 0
                self.add_times = [0,0,0]
            else:
                self.selected_continue_game = False

    def call_menu(self):
        if self.selected_tower is not None:
            x, y = self.selected_tower.rect.center
            self.__menu = UpgradeMenu(x, y)
        elif self.selected_plot is not None:
            x, y = self.selected_plot.rect.center
            self.__menu = BuildMenu(x, y)
        else:
            self.__menu = None
    def get_main_menu(self):
        return self.__main_menu.buttons


    def towers_attack(self,bullet_list):
        for tw in self.__towers:
            tw.attack(self.__enemies.get(),bullet_list,self.mute)

    def enemies_advance(self):
        self.__enemies.advance(self)
    def enemies_empty(self):
        return True if self.enemies.is_empty() else False
    def bullets_update(self):
        self.bullets.update()

    def put_message(self, message):
        if message is not None:
            self.message = message
        else:
            self.message = None

    def get_message_continue(self):
        return MESSAGE_CONTINUE

    def impact_animate(self):
        self.add_times[self.add_which] += 1
        if self.add_times[self.add_which] <= abs(self.add_value[self.add_which]):
            if not self.mute:
                self.sound.play()
            # decide to +1 or -1
            if self.add_value[self.add_which] > 0:
                self.add_amount = 1
            elif self.add_value[self.add_which] < 0:
                self.add_amount = -1
            # change hp, tower_money and money
            if self.add_which == 0:
                self.hp += self.add_amount
                if self.hp == 0:
                    self.hp = 1
            elif self.add_which == 1:
                if self.tower_money == 0 and self.add_value[self.add_which]<-1 and abs(self.add_value[self.add_which])-self.add_times[self.add_which] >1:
                    for tw in self.__towers:
                        x,y = tw.rect.center
                        self.plots.append(Vacancy(x, y))
                        self.towers.remove(tw)
                        self.add_value[self.add_which]=0
                        break
                self.tower_money += self.add_amount
                if self.tower_money <= 0:
                    self.tower_money = 0
            elif self.add_which == 2:
                self.money += self.add_amount
                if self.money <= 0:
                    self.money = 0
        else:
            self.add_clock = 0
            if self.add_which == 2:
                self.animate_state = "Done"
            else:
                self.add_which += 1

    def impact_animate_get_start(self):
        self.add_clock += 1
        if self.add_clock >= self.add_delay and self.add_clock % self.add_interval == 0:
            self.impact_animate()

    @property
    def enemies(self):
        return self.__enemies
    @property
    def bullets(self):
        return self.__bullet
    @property
    def towers(self):
        return self.__towers

    @property
    def menu(self):
        return self.__menu

    @menu.setter
    def menu(self, new_menu:Menu):
        self.__menu = new_menu

    @property
    def plots(self):
        return self.__plots

    @property
    def get_progress(self):
        return self.__enemies.count2


    











