from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.model import GameModel
    from game.view import GameView
import pygame


# controller
class GameControl:
    def __init__(self, game_model:GameModel, game_view:GameView):
        self.model = game_model
        self.view = game_view
        self.events = {"game quit": False,
                       "mouse position": [0, 0],
                       "keyboard key": 0
                       }
        self.request = None  # response of user input
        self.keep_going = False
        self.fail = False
        self.wait = 3
        self.count = 0
    def update_model(self):
        """update the model and the view here"""
        if self.model.hp <= 0:
            self.fail = True
        if self.model.enemies_empty() and self.wait <0:
            self.wait = 3
            self.keep_going = True
        self.request = self.model.get_request(self.events)
        self.model.user_request(self.request)
        if self.model.pause:
            return
        self.model.call_menu()
        self.model.towers_attack(self.model.bullets)
        self.model.enemies_advance()
        self.model.bullets_update()
    def receive_user_input(self):
        """receive user input from the events"""
        # event initialization
        self.events = {"game quit": False,
                       "mouse position": None,
                       "keyboard key": None,
                       "mouse move":None
                       }
        # update event
        x, y = pygame.mouse.get_pos()
        self.events["mouse move"] = [x,y]
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.events["game quit"] = True
            # player press action
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.events["keyboard key"] = pygame.K_n
            # player click action
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.events["mouse position"] = [x, y]
        
        
        

    def update_view(self):
        # render background
        self.view.draw_bg()
        self.view.draw_towers(self.model.towers)
        self.view.draw_hp(self.model.hp,self.model.max_hp)
        self.view.draw_enemies(self.model.enemies)
        self.view.draw_bullets(self.model.bullets)
        self.view.draw_range(self.model.touched_tower)
        self.view.draw_range(self.model.selected_tower)
        self.view.draw_plots(self.model.plots)
        self.view.draw_money(self.model.money)
        self.view.draw_tower_money(self.model.tower_money)
        self.view.draw_main_menu(self.model.get_main_menu(),self.model.mute,self.model.pause,self.model.show_ability)

        if self.model.show_notify:
            self.view.draw_notify(self.model.notify,self.model.notify2,self.model.had_occur,self.model.click_to_shrink, self.model.click_to_shrink_rect.centery)
            # click_animation
            '''
            if self.model.click_message_move_count < self.model.click_message_move_max:
                self.model.click_to_shrink_rect.centery += 1
                self.model.click_message_move_count += 1
            else:
                self.model.click_to_shrink_rect.centery = 580
                self.model.click_message_move_count = 0
            '''
        self.view.draw_stage(self.model.stage)

        """(Q2) Controller request View to render something"""
        if self.model.menu is not None:
            self.view.draw_menu(self.model.menu)

        
       
        # 畫出通知
        if self.model.message is not None:
            continue_btn = self.model.get_message_continue()
            self.view.draw_message(self.model.message, continue_btn, self.model.message_continue_rect)
            if self.model.animate_state == "Undone":
                self.model.impact_animate_get_start()
            #print(self.model.add_which)
            #print(self.model.add_times)
            #print(self.model.animate_state)
            else:
                if self.model.message_move_count < self.model.message_move_max:
                    self.model.message_continue_rect.centerx += 1
                    self.model.message_move_count += 1
                else :
                    self.model.message_continue_rect.centerx = 880
                    self.model.message_move_count = 0

            if self.model.selected_continue_game == False:
                return False
            else:
                self.model.selected_continue_game = False
                return True
            
        # 倒數
        if self.wait > 0:
            self.view.draw_progress(0,10)
            self.view.draw_wait(self.wait)
            if self.count >= 25:
                self.wait -=1
                self.count = 0
            else:
                if not self.model.pause:
                    self.count += 1
               
        elif self.wait == 0:
            self.view.draw_wait(self.wait)
            self.model.enemies.add(10,self.model.stage)
            self.model.stage += 1
            self.view.draw_progress(self.model.get_progress,10)
            self.wait -= 1
        else:
            self.view.draw_progress(self.model.get_progress,10)
            pass

    @property
    def quit_game(self):
        return self.events["game quit"]
    


