from color_settings import BLACK
import pygame
import os
from math import atan2, degrees, pi,sqrt
class BulletGroup():
    def __init__(self) -> None:
        self.bullet_list = []

        pass
    def generate(self,tower,enemy,start,end):
        self.bullet_list.append(Bullet(tower,enemy,start,end))
    def get(self):
        return self.bullet_list
    def update(self):
        for bullet in self.bullet_list:
            bullet.move(self)
    def remove(self,bullet):
        self.bullet_list.remove(bullet)
BULLET1_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet1.png")), (30, 30)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet_money1.png")), (30, 30))]
BULLET2_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet2.png")), (30, 30)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet_money2.png")), (30, 30))]
BULLET3_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet3.png")), (30, 30)),
                pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "bullet_money3.png")), (30, 30))]
class Bullet():
    def __init__(self,enemy,tower,start,end) -> None:
        self.tower = tower
        self.enemy = enemy
        self.start = start
        self.end = end
        if tower.level == 0:
            self.image = BULLET1_IMAGE[tower.player]
        elif tower.level == 1:
            self.image = BULLET2_IMAGE[tower.player]
        elif tower.level == 2:
            self.image = BULLET3_IMAGE[tower.player]
        self.rect = self.image.get_rect()
        self.rect.center = start
        self.move_count = 0
        x1,y1 = self.start
        x2,y2 = self.end
        dx = x2 - x1
        dy = y2 - y1
        rads = atan2(-dy,dx)
        rads %= 2*pi
        degs = degrees(rads)-90
        self.image=pygame.transform.rotate(self.image,degs)
        pass
    def move(self,bullet_list):
        x1,y1 = self.start
        x2,y2 = self.end
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        max_count = int(distance / 10)
        # compute the unit vector
        unit_vector_x = (x2 - x1) / distance
        unit_vector_y = (y2 - y1) / distance
        # compute the movement
        delta_x = unit_vector_x * 10 * self.move_count
        delta_y = unit_vector_y * 10 * self.move_count
        # update the position and counter
        if self.move_count <= max_count:
            self.rect.center = (x1 + delta_x, y1 + delta_y)
            self.move_count += 1
        else:
            self.enemy.health -= self.tower.damage
            bullet_list.remove(self)