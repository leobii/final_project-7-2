from __future__ import annotations

from pygame import mixer
from tower.attack_strategy import AOE, SingleAttack, Snipe,AttackStrategy
import os
import pygame
from pygame import mixer

PLOT_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "space.png")), (40, 40))
TOWER1_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_tv1.png")), (70, 70)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_atm1.png")), (70, 70))]
TOWER2_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_tv2.png")), (70, 70)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_atm2.png")), (70, 70))]
TOWER3_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_tv3.png")), (70, 70)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "tower_atm3.png")), (70, 70))]

class Vacancy:
    def __init__(self, x:int, y:int):
        self.image = PLOT_IMAGE
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def clicked(self, x: int, y: int) -> bool:
        """
        :param x: mouse pos x
        :param y: mouse pos y
        :return: bool
        """
        return True if self.rect.collidepoint(x, y) else False


# tower (product)
class Tower:
    """ super class of towers """
    def __init__(self, x: int, y: int, attack_strategy:AttackStrategy, image:pygame.Surface):
        self.image = image  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-10)  # center of the tower
        self.level = 0  # level of the tower
        self._range = [130, 160,190]  # tower attack range
        self._damage = [1.5,  2, 2.5]  # tower damage
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.attack_strategy = attack_strategy  # chose an attack strategy (AOE, single attack ....)
        self.value = [100, 140, 200, 300, 380, 460]
        self.player = 0
    @classmethod
    def TV(cls, x:int, y:int,player:int):
        tv = cls(x, y, SingleAttack(), TOWER1_IMAGE[player])
        tv._range = [130, 180,230]
        tv._damage = [1.5,  2, 2.5]
        tv.value = [100, 140, 200, 280, 360, 450]
        tv.player = player
        return tv
    

    def attack(self, enemy_group: list,bullet_list,mute):
        # cd
        if self.level < 1:
            self.image = TOWER1_IMAGE[self.player]
        elif self.level < 2:
            self.image = TOWER2_IMAGE[self.player]
        else:
            self.image = TOWER3_IMAGE[self.player]
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return
        # syntax: attack_strategy().attack(tower, enemy_group, cd_count)
        # It's something like you hire a "Strategist" to decide how to attack the enemy
        # You can add other ways of attack just by expanding the "attack_strategy.py"
        self.cd_count = self.attack_strategy.attack(enemy_group, self, self.cd_count,bullet_list,mute)


    def get_upgrade_cost(self):
        
        return self.value[self.level+1] - self.value[self.level]

    def get_cost(self):
        return self.value[self.level]

    @property
    def range(self):
        return self._range[self.level]

    @property
    def damage(self):
        return self._damage[self.level]

    def clicked(self, x: int, y: int) -> bool:
        """
        :param x: mouse pos x
        :param y: mouse pos y
        :return: bool
        """
        return True if self.rect.collidepoint(x, y) else False
    def touched(self, x: int, y: int) -> bool:
        """
        :param x: mouse pos x
        :param y: mouse pos y
        :return: bool
        """
        return True if self.rect.collidepoint(x, y) else False




