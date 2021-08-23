import pygame
import os
from color_settings import *
from event.event_setting import *
from event.data_wfh import wfh_problem,wfh_decision,wfh_impact,wfh_notify,wfh_hint,wfh_impact2,wfh_notify2,wfh_text,wfh_message1,wfh_message2
   
def set_wfh(num:int):
    event_img = wfh_problem[num-1]
    event_text = wfh_text[num-1]

    event_select_img = wfh_decision[num-1]
    event_hint = wfh_hint[num-1]
    event_notify = wfh_notify[num-1]
    event_notify2 = wfh_notify2[num-1]
    event_message1 = wfh_message1[num-1]
    event_message2 = wfh_message2[num-1]
    
    event_impact = wfh_impact[num-1]
    event_impact2 = wfh_impact2[num-1]
    if num == 4:
        move = True
    else:
        move = False
    event_question = an_question(0,event_img,move)
    event_decision = [an_decision(1,event_select_img[0],event_impact[0],event_notify[0],event_hint[0],event_impact2[0],event_notify2[0],event_text[0],event_message1[0],event_message2[0],2),
                      an_decision(2,event_select_img[1],event_impact[1],event_notify[1],event_hint[1],event_impact2[1],event_notify2[1],event_text[1],event_message1[1],event_message2[1],2),
                      an_decision(3,event_select_img[2],event_impact[2],event_notify[2],event_hint[2],event_impact2[2],event_notify2[2],event_text[2],event_message1[2],event_message2[2],2)]
    return an_event(event_question,event_decision[0],event_decision[1],event_decision[2])
    



