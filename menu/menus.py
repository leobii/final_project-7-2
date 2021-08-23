import pygame
import os
from event.event_setting import MUTE_IMAGE,PLAY_IMAGE,SOUND_IMAGE,PAUSE_IMAGE
from settings import FONT
pygame.init()
BUY_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "buy.png")), (135, 70))
UPGRADE_MENU_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "upgrade.png")), (135,70 ))
GREEN_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "green_yes.png")), (130, 30))

NOTIFY_IMAGE_SHOW = pygame.transform.scale(pygame.image.load(os.path.join("images1/notify_message", "message_shrink.png")),(169,25))



ABILITY_MENU_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "ability_menu_icon.png")), (100, 100)),
                    pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "special_skill_wfh_icon.png")), (100, 100))]
ABILITY_BTN_IMAGE = [pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "special_skill.png")), (130, 120)),
                    pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "special_skill_wfh.png")), (130, 120))]
YELLOW_BTN_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/game_page", "yellow_yes.png")), (125, 28))

muse_button_image = pygame.transform.scale(MUTE_IMAGE, (34, 29))
music_button_image = pygame.transform.scale(SOUND_IMAGE, (34, 29))
continue_button_image = pygame.transform.scale(PLAY_IMAGE, (17, 24))
pause_button_image = pygame.transform.scale(PAUSE_IMAGE, (17, 24))


class Button:
    def __init__(self, image, name: str, x: int, y: int):
        self.image = image
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def clicked(self, x, y):
        return True if self.rect.collidepoint(x, y) else False

    @property
    def response(self):
        return self.name


class Menu:
    def __init__(self, x: int, y: int,image ):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x-105, y-5)
        if x-105 < 0:
            self.rect.center = (x+105, y-5)
        self._buttons = []

    @property
    def buttons(self):
        return self._buttons



class BuildMenu(Menu):
    def __init__(self, x, y):
        super().__init__(x, y,BUY_MENU_IMAGE)
        self._buttons = [Button(GREEN_BTN_IMAGE, "TV", self.rect.centerx, self.rect.centery+20)
        ]

class UpgradeMenu(Menu):
    def __init__(self, x, y):
        super().__init__(x, y,UPGRADE_MENU_IMAGE)
        self._buttons = [Button(GREEN_BTN_IMAGE, "upgrade", self.rect.centerx, self.rect.centery+20 )
                         ]
class MainMenu:
    def __init__(self,player):
        
        self._buttons = [Button(muse_button_image, "mute", 760, 540),
                        Button(music_button_image, "music", 760, 540),
                         Button(continue_button_image, "continue", 716, 540),
                         Button(pause_button_image, "pause", 716, 540),
                         Button(NOTIFY_IMAGE_SHOW,"show_notify", 120, 560-5),
                         Button(ABILITY_MENU_IMAGE[player],"show_ability",935,510),
                         Button(ABILITY_BTN_IMAGE[player],"nothing",935,385),
                         Button(YELLOW_BTN_IMAGE,"use_ability",935,385+45)]

    @property
    def buttons(self):
        return self._buttons







