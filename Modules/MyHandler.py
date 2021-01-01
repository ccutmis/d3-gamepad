from Modules.XInput import *
from pynput.keyboard import Key, Controller
import Modules.mouse_api as Mouse
from math import pi,sin,cos,atan2

class MyHandler(EventHandler):
    def process_button_event(self,event):
        keyboard = Controller()
        #print(event.button)
        if event.button in self.global_var.key_config.keys():
            key_val=self.global_var.key_config[event.button]
            if key_val!="" and self.global_var.in_active_win==True: #不是空白才繼續動作
                x=self.global_var.btn_dict[event.button]
                if event.type==3:
                    if self.global_var.key_onoff_mode[event.button]==1 and key_val in self.global_var.onoff_list: #先前已按
                            self.global_var.onoff_list.remove(key_val)
                    else:
                        if self.global_var.key_onoff_mode[event.button]==1:
                            #檢查current_onoff[x]是否為0
                            if key_val not in self.global_var.onoff_list:
                                self.global_var.onoff_list.append(key_val)
                                self.kb_press_eval_key(key_val)
                                self.kb_release_eval_key(key_val)
                        if key_val not in ["LM","RM"]:
                            if len(key_val)==1:
                                keyboard.press(key_val)
                            else:
                                keyboard.press(eval("Key."+key_val))
                        else:
                            self.global_var.cx,self.global_var.cy=Mouse.get_pos()
                            if key_val=="LM":
                                Mouse.click("left",self.global_var.cx,self.global_var.cy)
                            else:
                                Mouse.click("right",self.global_var.cx,self.global_var.cy)
                        self.global_var.keys_stat_last[x]=True
                else:
                    if self.global_var.key_onoff_mode[event.button]==1 and self.global_var.btn2_dict[x] in self.global_var.onoff_list:
                        self.kb_press_eval_key(key_val)
                        self.kb_release_eval_key(key_val)
                    if self.global_var.keys_stat_last[x]==True: #先前已按目前沒按
                        if key_val not in ["LM","RM"]:
                            if len(key_val)==1:
                                keyboard.release(key_val)
                            else:
                                keyboard.release(eval("Key."+key_val))
                        else:
                            self.global_var.cx,self.global_var.cy=Mouse.get_pos()
                            if key_val=="LM":
                                Mouse.click("left",self.global_var.cx,self.global_var.cy,0)
                            else:
                                Mouse.click("right",self.global_var.cx,self.global_var.cy,0)
                        self.global_var.keys_stat_last[x]=False
            else:
                self.global_var.onoff_list=[]

    def process_stick_event(self, event):
        #print(event)
        if event.stick == LEFT:
            self.global_var.stick_info[0]={"x":event.x,"y":event.y,"val":event.value,"dir":event.dir}
        else:
            self.global_var.stick_info[1]={"x":event.x,"y":event.y,"val":event.value,"dir":event.dir}

    def process_trigger_event(self, event):
        if self.global_var.in_active_win==True:
            keyboard = Controller()
            if event.trigger == LEFT:
                scroll_val=int(round(40 * event.value, 0))
                key_val=self.global_var.key_config["LEFT_TRIGER"]
                if key_val!="": #不是空白才繼續動作
                    if scroll_val>0:
                        self.global_var.triger_stat[0]=1
                        self.kb_press_eval_key(key_val)
                    else:
                        self.global_var.triger_stat[0]=0
                        self.kb_release_eval_key(key_val)
            elif event.trigger == RIGHT:
                scroll_val=int(round(40 * event.value, 0))
                key_val=self.global_var.key_config["RIGHT_TRIGER"]
                if key_val!="": #不是空白才繼續動作
                    if scroll_val>0:
                        self.global_var.triger_stat[1]=1
                        self.kb_press_eval_key(key_val)
                    else:
                        self.global_var.triger_stat[1]=0
                        self.kb_release_eval_key(key_val)

    def process_connection_event(self, event):
        if event.type == EVENT_CONNECTED:
            pass
        elif event.type == EVENT_DISCONNECTED:
            pass
        else:
            print("Unrecognized controller event type")

    def gent_degree_dict(self,divisions=360,radius=10):
        #divisions,radius=360,10
        out_dict={}
        # the difference between angles in radians -- don't bother with degrees
        angle = 2 * pi / divisions
        # a list of all angles using a list comprehension
        angles = [i*angle for i in range(divisions)]
        oi=0
        for a in angles:
            out_dict[oi]=[round(radius*sin(a)),(round(radius*cos(a)))]
            oi+=1
        return out_dict

    def deg_to_xy(self,deg_dict,deg):
        #deg_dict must be a dictionary
        xy_list=deg_dict[deg]
        return xy_list[0],-xy_list[1]
    
    def kb_press_eval_key(self,key_val):
        keyboard = Controller()
        if key_val!="": #不是空白才繼續動作
            if key_val not in ["LM","RM"]:
                if len(key_val)==1:
                    keyboard.press(key_val)
                else:
                    keyboard.press(eval("Key."+key_val))
            else:
                cx,cy=Mouse.get_pos()
                if key_val=="LM":
                    Mouse.click("left",cx,cy)
                else:
                    Mouse.click("right",cx,cy)

    def kb_release_eval_key(self,key_val):
        keyboard = Controller()
        if key_val!="": #不是空白才繼續動作
            if key_val not in ["LM","RM"]:
                if len(key_val)==1:
                    keyboard.release(key_val)
                else:
                    keyboard.release(eval("Key."+key_val))
            else:
                cx,cy=Mouse.get_pos()
                if key_val=="LM":
                    Mouse.click("left",cx,cy,0)
                else:
                    Mouse.click("right",cx,cy,0)
