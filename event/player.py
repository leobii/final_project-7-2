import pygame
import os
from settings import *
dict_temp = {}
# 打开文本文件
file = open('dict.txt','r')
# 遍历文本文件的每一行，strip可以移除字符串头尾指定的字符（默认为空格或换行符）或字符序列
for line in file.readlines():
    line = line.strip()
    k = line.split(' ')[0]
    v = line.split(' ')[1]
    dict_temp[k] = v

# 依旧是关闭文件
file.close()

pygame.init()
my_font = pygame.font.Font('OtsutomeFont.ttf',36)
GOV_ICON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/choice_page", "btn_gover_icon.png")),(CHOOSE_PLAYER_ICON_WIDTH, CHOOSE_PLAYER_ICON_HEIGHT))
GOV_WORD_IMAGE = my_font.render('政府',True,(80, 61, 50, 1))
WFH_ICON_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("images1/choice_page", "btn_wfh_icon.png")),(CHOOSE_PLAYER_ICON_WIDTH, CHOOSE_PLAYER_ICON_HEIGHT))

LOCK_IMAGE= pygame.transform.scale(pygame.image.load(os.path.join("images1/choice_page", "unlock_character.png")),(CHOOSE_PLAYER_ICON_WIDTH+50, CHOOSE_PLAYER_ICON_HEIGHT))
 
WFH_WORD_IMAGE = my_font.render('居家工作者',True,(80, 61, 50, 1))

class Players:
    def __init__(self,gov:str,wfh:str):
        self.player=0
        if gov == '1':
            self.gov = True
        else:
            self.gov = False
        if wfh == '1':
            self.wfh = True
        else:
            self.wfh = False
        
        self.player_rect_list=['',]
        self.player_btn = [Player_btn(1,'gov',GOV_ICON_IMAGE,LOCK_IMAGE,GOV_WORD_IMAGE,300,300,self.gov,1),
                            Player_btn(2,'wfh',WFH_ICON_IMAGE,LOCK_IMAGE,WFH_WORD_IMAGE,720,300,self.wfh,50)]
        pass

    def get_click_choose_player(self,x:int,y:int):
        if self.player_btn[1].icon_image_rect.collidepoint(x,y):
            self.player = 1
        elif self.player_btn[2].icon_image_rect.collidepoint(x,y):
            self.player = 2

class Player_btn:
    def __init__(self,num:int,name:str,icon_image:pygame.Surface,lock_image:pygame.Surface,word_image:pygame.Surface,x:int,y:int,unlock:bool,cost:int):
        self.num = num
        self.name=name
        self.icon_image=icon_image
        self.lock_image = lock_image
        self.word_image=word_image
        self.icon_image_rect=self.icon_image.get_rect()
        self.lock_image_rect = self.icon_image.get_rect()
        self.word_image_rect=self.word_image.get_rect()
        self.lock_image_rect.center=(x-40,y)
        self.icon_image_rect.center=(x,y)
        self.word_image_rect.center=(x,y+85)
        self.show_buy = False
        self.buy_message = pygame.transform.scale(pygame.image.load(os.path.join("images1/choice_page", "buy_question.png")), (280, 156))
        self.buy_message_rect = self.buy_message.get_rect()
        self.buy_message_rect.center = (512,318)
        self.buy = pygame.transform.scale(pygame.image.load(os.path.join("images1/choice_page", "buy_yes.png")), (106, 41))
        self.buy_rect =  self.buy.get_rect()
        self.buy_rect.center = (512,355)
        self.selected = False
        self.unlock =  unlock
        self.cost = cost
        w, h = 200,200
        self.frame = pygame.Rect(x - 105, y - 95, w + 10, h + 10)
        pass
