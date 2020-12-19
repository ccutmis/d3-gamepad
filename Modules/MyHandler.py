from Modules.XInput import *
from pynput.keyboard import Key, Controller
import Modules.mouse_api as Mouse
from Modules.WindowMgr import *
import time,math

class MyHandler(EventHandler):
    def process_button_event(self,event):
        w=WindowMgr()
        if self.global_var.active_win_title in w.active_window_title():
            keyboard = Controller()
            if event.button in self.global_var.key_config.keys():
                key_val=self.global_var.key_config[event.button]
                if event.type==3:
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
                else:
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

    def process_stick_event(self, event):
        w=WindowMgr()
        if self.global_var.active_win_title in w.active_window_title():
            win_pos_size=w.get_window_pos_size() #[x,y,w,h]
            time.sleep(self.global_var.delay_second)
            self.global_var.x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
            self.global_var.y_center=int(win_pos_size[1]+(win_pos_size[3]/2)+(self.global_var.y_center_offset))
            if event.stick == LEFT:
                if self.global_var.stick_stat[0]==0 and (abs(event.x)!=0 or abs(event.y)!=0):
                    self.global_var.stick_stat[0]=1
                elif abs(event.x)==0 and abs(event.y)==0:
                    self.global_var.stick_stat[0]=0
                else:
                    self.global_var.stick_stat[0]=2
                if self.global_var.stick_stat[0]==2:
                    #移動滑鼠
                    deg=int(math.atan2(event.x,event.y)/math.pi*180)
                    if deg<0: deg=180+(180+deg)
                    self.global_var.stick_degree[0]=deg
                    xx,yy=self.deg_to_xy(self.global_var.deg_dict,deg)
                    Mouse.set_pos(self.global_var.x_center+xx*self.global_var.xy_offset_unit*2,self.global_var.y_center+yy*self.global_var.xy_offset_unit*2)
                    if self.global_var.set_left_controller_move_and_click==True:
                        self.kb_press_eval_key(self.global_var.left_controller_click_val)
                        self.kb_release_eval_key(self.global_var.left_controller_click_val)
            elif event.stick == RIGHT:
                if self.global_var.stick_stat[1]==0 and (abs(event.x)!=0 or abs(event.y)!=0):
                    self.global_var.stick_stat[1]=1
                elif abs(event.x)==0 and abs(event.y)==0:
                    self.global_var.stick_stat[1]=0
                else:
                    self.global_var.stick_stat[1]=2
                if self.global_var.stick_stat[1]==2:
                    #移動滑鼠
                    deg=int(math.atan2(event.x,event.y)/math.pi*180)
                    if deg<0: deg=180+(180+deg)
                    self.global_var.stick_degree[1]=deg
                    xx,yy=self.deg_to_xy(self.global_var.deg_dict,deg)
                    Mouse.move_to(xx,yy)

    def process_trigger_event(self, event):
        keyboard = Controller()
        if event.trigger == LEFT:
            scroll_val=int(round(40 * event.value, 0))
            key_val=self.global_var.key_config["LEFT_TRIGER"]
            if self.global_var.triger_stat[0]==0:
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
                self.global_var.triger_stat[0]=1
            elif scroll_val==0:
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
                self.global_var.triger_stat[0]=0
            
        elif event.trigger == RIGHT:
            scroll_val=int(round(40 * event.value, 0))
            key_val=self.global_var.key_config["RIGHT_TRIGER"]
            if self.global_var.triger_stat[1]==0:
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
                self.global_var.triger_stat[1]=1
            elif scroll_val==0:
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
                self.global_var.triger_stat[1]=0

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
        angle = 2 * math.pi / divisions
        # a list of all angles using a list comprehension
        angles = [i*angle for i in range(divisions)]
        oi=0
        for a in angles:
            out_dict[oi]=[int(radius*math.sin(a)),(int(radius*math.cos(a)))]
            oi+=1
        return out_dict

    def deg_to_xy(self,deg_dict,deg):
        #deg_dict must be a dictionary
        xy_list=deg_dict[deg]
        return xy_list[0],-xy_list[1]
    
    def kb_press_eval_key(self,key_val):
        global cx,cy
        keyboard = Controller()
        if key_val not in ["LM","RM"]:
            if len(key_val)==1:
                keyboard.press(key_val)
            else:
                keyboard.press(eval("Key."+key_val))
        else:
            cx,cy=Mouse.get_pos()
            if key_val=="LM":
                Mouse.click("left",cx,cy)
                #Mouse.click("left",cx,cy,0)
            else:
                Mouse.click("right",cx,cy)
                #Mouse.click("right",cx,cy,0)
    
    def kb_release_eval_key(self,key_val):
        global cx,cy
        keyboard = Controller()
        if key_val not in ["LM","RM"]:
            if len(key_val)==1:
                keyboard.release(key_val)
            else:
                keyboard.release(eval("Key."+key_val))
        else:
            cx,cy=Mouse.get_pos()
            if key_val=="LM":
                #Mouse.click("left",cx,cy)
                Mouse.click("left",cx,cy,0)
            else:
                #Mouse.click("right",cx,cy)
                Mouse.click("right",cx,cy,0)