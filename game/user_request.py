from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.model import GameModel
import pygame
from abc import ABC,abstractmethod
from tower.towers import Tower, Vacancy

"""This module is import in model.py"""

"""
Here we demonstrate how does the Observer Pattern work
Once the subject updates, if will notify all the observer who has register the subject
"""

class Observer(ABC):
    def __init__(self,subject:RequestSubject) -> None:
        subject.register(self)
    @abstractmethod
    def update(self,user_request:str,model:GameModel):
        raise 'Implement this method'
class RequestSubject:
    def __init__(self, model:GameModel):
        self.__observers = []
        self.model = model

    def register(self, observer:Observer):
        self.__observers.append(observer)

    def notify(self, user_request:str):
        for o in self.__observers:
            o.update(user_request, self.model)
            if self.model.pause and user_request!= 'music':
                return



class Show_Hide_Notify:
    def __init__(self,subject) -> None:
        subject.register(self)
    def update(self, user_request: str, model):
        if user_request == 'show_notify':
            model.show_notify = not model.show_notify
            
class TowerKiller:
    def __init__(self,):
        pass

    def update(self,model:GameModel):
        tw_list = model.towers
        for i in range(len(tw_list)-1,-1,-1):
            x,y = tw_list[i].rect.center
            model.plots.append(Vacancy(x,y))
            model.towers.remove(tw_list[i])
        
        
        model.selected_tower = None
            


class TowerDeveloper:
    def __init__(self, subject:RequestSubject):
        subject.register(self)

    def update(self, user_request: str, model:GameModel):
        if user_request == "upgrade" and model.selected_tower.level < 2:
            # if the money > upgrade cost of the selected tower , level+1
            # use model.selected_tower to access the selected tower data
            # use model.money to access to money data
            
            if model.tower_money >= 1:
                model.tower_money -= 1
                model.selected_tower.level += 1
            pass



class TowerFactory:
    def __init__(self, subject:RequestSubject):
        subject.register(self)
        self.tower_name = ["TV"]

    def update(self, user_request: str, model:GameModel):
        """add new tower"""
        for name in self.tower_name:
            if user_request == name:
                x, y = model.selected_plot.rect.center
                tower_dict = {"TV": Tower.TV(x, y,model.player)}
                new_tower = tower_dict[user_request]
                if model.tower_money > 1:
                    model.tower_money -= 2
                    model.towers.append(new_tower)
                    model.plots.remove(model.selected_plot)
                    model.selected_plot = None


class Music:
    def __init__(self, subject:RequestSubject):
        subject.register(self)

    def update(self, user_request: str, model:GameModel):
        """music on"""
        if user_request == "music":
            
            
            model.mute = not model.mute
            if model.mute:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            #model.sound.play()




class Ability:
    def __init__(self,subject:RequestSubject):
        subject.register(self)
    def update(self, user_request: str, model:GameModel):
        if user_request == 'use_ability' and model.show_ability:
            #print('use ability')
            #print(model.player)
            if model.player == 0:
                if model.money >= 30: 
                    model.money -= 30
                    en_list = model.enemies.get()
                    for i in range(len(en_list)-1,-1,-1):
                        if en_list[i].level == 1:
                            model.enemies.retreat(en_list[i])
                        #print('kill')
            if model.player == 1:
                if model.money >= 30: 
                    model.money -= 30
                    for en in model.enemies.get():
                        en.path_index = 0
        if user_request == 'show_ability':
            #print('show abiltiy')
            model.show_ability = not model.show_ability


        
        

class Play:
    def __init__(self, subject:RequestSubject):
        subject.register(self)

    def update(self, user_request: str, model:GameModel):
        """music on"""
        if user_request == "pause":
            model.pause = not model.pause
            #model.sound.play()
