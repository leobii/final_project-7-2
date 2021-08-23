import pygame
import os
from color_settings import *
from event.event_setting import *
from event.data_gov import gov_problem,gov_decision,gov_impact,gov_notify,gov_hint,gov_impact2,gov_notify2,gov_text,gov_message1,gov_message2
   
def set_gov(num:int):
    event_img = gov_problem[num-1]
    event_text = gov_text[num-1]

    event_select_img = gov_decision[num-1]
    event_hint = gov_hint[num-1]
    event_notify = gov_notify[num-1]
    event_notify2 = gov_notify2[num-1]
    event_message1 = gov_message1[num-1]
    event_message2 = gov_message2[num-1]
    
    event_impact = gov_impact[num-1]
    event_impact2 = gov_impact2[num-1]

    event_question = an_question(0,event_img)
    event_decision = [an_decision(1,event_select_img[0],event_impact[0],event_notify[0],event_hint[0],event_impact2[0],event_notify2[0],event_text[0],event_message1[0],event_message2[0],1),
                      an_decision(2,event_select_img[1],event_impact[1],event_notify[1],event_hint[1],event_impact2[1],event_notify2[1],event_text[1],event_message1[1],event_message2[1],1),
                      an_decision(3,event_select_img[2],event_impact[2],event_notify[2],event_hint[2],event_impact2[2],event_notify2[2],event_text[2],event_message1[2],event_message2[2],1)]
    return an_event(event_question,event_decision[0],event_decision[1],event_decision[2])
    



