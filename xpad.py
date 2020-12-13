# resource url: https://github.com/Zuzu-Typ/XInput-Python
# 需安裝的套件 pypiwin32 XInput-Python pynput==1.6.8
import time
from XInput import *
from datetime import datetime
from time import sleep
from pynput.keyboard import Key, Controller
from Modules.WindowMgr import *
import Modules.mouse_api as Mouse
import traceback,sys,math,msvcrt

VERSION="0001C"

def gent_degree_dict(divisions=360,radius=10):
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
    #out_dict[divisions]=[0,10]
    return out_dict

def deg_to_xy(deg):
    global DEG_DICT
    xy_list=DEG_DICT[deg]
    return xy_list[0],-xy_list[1]

def kb_press_eval_key(key_val):
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

def kb_release_eval_key(key_val):
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

class Controller1:
    def __init__(self, center):
        self.center = center
        self.on_indicator_pos = (self.center[0], self.center[1] - 50)
        self.r_thumb_pos = (self.center[0] + 50, self.center[1] + 20)
        r_thumb_stick_pos = self.r_thumb_pos
        self.l_thumb_pos = (self.center[0] - 100, self.center[1] - 20)
        l_thumb_stick_pos = self.l_thumb_pos
        self.l_trigger_pos = (self.center[0] - 120, self.center[1] - 70)
        l_trigger_index_pos = (self.l_trigger_pos[0], self.l_trigger_pos[1] - 20)
        self.r_trigger_pos = (self.center[0] + 120, self.center[1] - 70)
        r_trigger_index_pos = (self.r_trigger_pos[0], self.r_trigger_pos[1] - 20)
        buttons_pos = (self.center[0] + 100, self.center[1] - 20)
        A_button_pos = (buttons_pos[0], buttons_pos[1] + 20)
        B_button_pos = (buttons_pos[0] + 20, buttons_pos[1])
        Y_button_pos = (buttons_pos[0], buttons_pos[1] - 20)
        X_button_pos = (buttons_pos[0] - 20, buttons_pos[1])
        dpad_pos = (self.center[0] - 50, self.center[1] + 20)
        back_button_pos = (self.center[0] - 20, self.center[1] - 20)
        start_button_pos = (self.center[0] + 20, self.center[1] - 20)
        l_shoulder_pos = (self.center[0] - 90, self.center[1] - 70)
        r_shoulder_pos = (self.center[0] + 90, self.center[1] - 70)
controllers = (Controller1((150., 100.)),
               Controller1((450., 100.)),
               Controller1((150., 300.)),
               Controller1((450., 300.)))
class MyHandler(EventHandler):
    def process_button_event(self,event):
        global KEY_CONFIG,cx,cy,ACTIVE_WIN_TITLE,w,win_pos_size,x_center,y_center
        if ACTIVE_WIN_TITLE in w.active_window_title():
            #win_pos_size=w.get_window_pos_size() #[x,y,w,h]
            #time.sleep(DELAY_SECOND)
            #x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
            #y_center=int(win_pos_size[1]+(win_pos_size[3]/2)+(Y_CENTER_OFFSET))
            keyboard = Controller()
            controller = controllers[event.user_index]
            if event.button in ["LEFT_SHOULDER","RIGHT_SHOULDER","BACK","START","DPAD_LEFT","DPAD_RIGHT","DPAD_UP","DPAD_DOWN","A","B","X","Y"]:
                key_val=KEY_CONFIG[event.button]
                if event.type==3:
                    #print("Button: "+event.button+"\t("+key_val+")\tPress")
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
                else:
                    #print("Button: "+event.button+"\t("+key_val+")\tRelease")
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

    def process_stick_event(self, event):
        global stick_stat,cx,cy,stick_degree,ACTIVE_WIN_TITLE,w,win_pos_size,x_center,y_center
        if ACTIVE_WIN_TITLE in w.active_window_title():
            win_pos_size=w.get_window_pos_size() #[x,y,w,h]
            time.sleep(DELAY_SECOND)
            x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
            y_center=int(win_pos_size[1]+(win_pos_size[3]/2)+(Y_CENTER_OFFSET))
            controller = controllers[event.user_index]
            if event.stick == LEFT:
                if stick_stat[0]==0 and (abs(event.x)!=0 or abs(event.y)!=0):
                    stick_stat[0]=1
                elif abs(event.x)==0 and abs(event.y)==0:
                    stick_stat[0]=0
                    #print(str(stick_stat[0])+"Stop LS")
                else:
                    stick_stat[0]=2
                if stick_stat[0]==2:
                    #移動滑鼠
                    deg=int(math.atan2(event.x,event.y)/math.pi*180)
                    if deg<0: deg=180+(180+deg)
                    stick_degree[0]=deg
                    xx,yy=deg_to_xy(deg)
                    #cx,cy=Mouse.get_pos()
                    Mouse.set_pos(x_center+xx*XY_OFFSET_UNIT*2,y_center+yy*XY_OFFSET_UNIT*2)
                    if SET_LEFT_CONTROLLER_MOVE_AND_CLICK==True:
                        kb_press_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                        kb_release_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                    #print(x_center+xx,y_center+yy)
                    #Mouse.move_to(xx,yy)
                    #print(str(stick_stat[0])+"Moving LS",event.x,event.y,"\tdegree:\t",deg)   
                #l_thumb_stick_pos = (int(round(controller.l_thumb_pos[0] + 25 * event.x,0)), int(round(controller.l_thumb_pos[1] - 25 * event.y,0)))
            elif event.stick == RIGHT:
                if stick_stat[1]==0 and (abs(event.x)!=0 or abs(event.y)!=0):
                    stick_stat[1]=1
                elif abs(event.x)==0 and abs(event.y)==0:
                    stick_stat[1]=0
                    #print(str(stick_stat[0])+"Stop LR")
                else:
                    stick_stat[1]=2
                if stick_stat[1]==2:
                    #移動滑鼠
                    deg=int(math.atan2(event.x,event.y)/math.pi*180)
                    if deg<0: deg=180+(180+deg)
                    stick_degree[1]=deg
                    xx,yy=deg_to_xy(deg)
                    #cx,cy=Mouse.get_pos()
                    Mouse.move_to(xx,yy)
                    #print(str(stick_stat[1])+"Moving RS",event.x,event.y,"\tdegree:\t",deg)
                #r_thumb_stick_pos = (int(round(controller.r_thumb_pos[0] + 25 * event.x,0)), int(round(controller.r_thumb_pos[1] - 25 * event.y,0)))

    def process_trigger_event(self, event):
        global triger_stat,KEY_CONFIG,cx,cy
        keyboard = Controller()
        controller = controllers[event.user_index]
        if event.trigger == LEFT:
            #l_trigger_index_pos = (controller.l_trigger_pos[0], controller.l_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
            scroll_val=int(round(40 * event.value, 0))
            key_val=KEY_CONFIG["LEFT_TRIGER"]
            if triger_stat[0]==0:
                #print("LEFT_TRIGER:\t("+key_val+")\tPress")
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
                triger_stat[0]=1
            elif scroll_val==0:
                #print("LEFT_TRIGER:\t("+key_val+")\tRelease")
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
                triger_stat[0]=0
            
        elif event.trigger == RIGHT:
            #r_trigger_index_pos = (controller.r_trigger_pos[0], controller.r_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
            scroll_val=int(round(40 * event.value, 0))
            key_val=KEY_CONFIG["RIGHT_TRIGER"]
            if triger_stat[1]==0:
                #print("RIGHT_TRIGER:\t("+key_val+")\tPress")
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
                triger_stat[1]=1
            elif scroll_val==0:
                #print("RIGHT_TRIGER:\t("+key_val+")\tRelease")
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
                triger_stat[1]=0

    def process_connection_event(self, event):
        controller = controllers[event.user_index]
        if event.type == EVENT_CONNECTED:
            pass
            #canvas.itemconfig(controller.on_indicator, fill="light green")
        elif event.type == EVENT_DISCONNECTED:
            pass
            #canvas.itemconfig(controller.on_indicator, fill="")
        else:
            print("Unrecognized controller event type")

class MyOtherHandler(EventHandler):
    def __init__(self, *controllers):
        super().__init__(*controllers, filter=BUTTON_A+FILTER_PRESSED_ONLY)

    def process_button_event(self, event):
        pass

    def process_stick_event(self, event):
        pass

    def process_trigger_event(self, event):
        pass

    def process_connection_event(self, event):
        pass

if __name__ == "__main__":
    try:
        ini_filename="xinput.ini"
        #讀取 xinput.ini參數
        with open(ini_filename,"r",encoding="utf-8") as f:
            tmp_content=f.read()
        f.close()
        exec(tmp_content)
        #print(KEY_CONFIG)
        set_deadzone(DEADZONE_TRIGGER,10)
        
        controller1=get_connected()
        if(controller1[0]==True):
            print("-------------------------------")
            print("偵測到控制器 按下 [←Backspace] 可關閉程式")
            print("程式版本:"+VERSION+"\t監控視窗:"+ACTIVE_WIN_TITLE)
            print("-------------------------------")
        else:
            print("未偵測到控制器，程式結束。")
            sys.exit()
        
        #有找到controller才做的事
        #全域變數區.START
        KEY_MAP={"alt":Key.alt,"alt_l":Key.alt_l,"alt_r":Key.alt_r,"backspace":Key.backspace,"caps_lock":Key.caps_lock,"cmd":Key.cmd,"cmd_r":Key.cmd_r,"ctrl":Key.ctrl,"ctrl_l":Key.ctrl_l,"ctrl_r":Key.ctrl_r,"delete":Key.delete,"down":Key.down,"end":Key.end,"enter":Key.enter,"esc":Key.esc,"f1":Key.f1,"f10":Key.f10,"f11":Key.f11,"f12":Key.f12,"f13":Key.f13,"f14":Key.f14,"f15":Key.f15,"f16":Key.f16,"f17":Key.f17,"f18":Key.f18,"f19":Key.f19,"f2":Key.f2,"f20":Key.f20,"f3":Key.f3,"f4":Key.f4,"f5":Key.f5,"f6":Key.f6,"f7":Key.f7,"f8":Key.f8,"f9":Key.f9,"home":Key.home,"insert":Key.insert,"left":Key.left,"menu":Key.menu,"num_lock":Key.num_lock,"page_down":Key.page_down,"page_up":Key.page_up,"pause":Key.pause,"print_screen":Key.print_screen,"right":Key.right,"scroll_lock":Key.scroll_lock,"shift":Key.shift,"shift_r":Key.shift_r,"space":Key.space,"tab":Key.tab,"up":Key.up}
        w=WindowMgr()
        fp=None
        cx,cy=Mouse.get_pos()
        triger_stat=[0,0]
        stick_stat=[0,0]
        stick_degree=[0,0]
        xy_offset=XY_OFFSET_UNIT
        xy_offset_bonus=0
        onoff_list=[]
        DEG_DICT=gent_degree_dict(360,XY_OFFSET_UNIT)
        last_thumb_dict={"l_thumb_x":0,"l_thumb_y":0,"r_thumb_x":0,"r_thumb_y":0}
        win_pos_size=-1
        x_center=-1
        y_center=-1
        win_pos_size=[0,0,0,0]
        #全域變數區.END

        handler = MyHandler(0, 1, 2, 3)        # initialize handler object
        thread = GamepadThread(handler)                 # initialize controller thread
        
        handler2 = MyOtherHandler(0)
        thread.add_event_handler(handler2)              # add another handler
        #handler2.set_filter(handler2.filter+TRIGGER_LEFT)
        while 1:
            if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode():
                sys.exit()
            #判斷當前視窗完整標題文字是否包含 ACTIVE_WIN_TITLE 設定之文字，若是才繼續後續處理...
            if ACTIVE_WIN_TITLE in w.active_window_title():
                win_pos_size=w.get_window_pos_size() #[x,y,w,h]
                time.sleep(DELAY_SECOND)
                x_center=int(win_pos_size[0]+(win_pos_size[2]/2))
                y_center=int(win_pos_size[1]+(win_pos_size[3]/2)+(Y_CENTER_OFFSET))
                if stick_stat[0]==2:
                    if xy_offset_bonus<20: xy_offset_bonus+=0.5
                    xx,yy=deg_to_xy(stick_degree[0])
                    Mouse.set_pos(x_center+xx*XY_OFFSET_UNIT*2,y_center+yy*XY_OFFSET_UNIT*2)
                    if SET_LEFT_CONTROLLER_MOVE_AND_CLICK==True:
                        kb_press_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                        kb_release_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                    #print("LS:force to move",xy_offset_bonus)

                elif stick_stat[1]==2:
                    if xy_offset_bonus<20: xy_offset_bonus+=0.5
                    xx,yy=deg_to_xy(stick_degree[1])
                    xx,yy=int(xx*xy_offset_bonus),int(yy*xy_offset_bonus)
                    #cx,cy=Mouse.get_pos()
                    Mouse.move_to(xx,yy)
                    #print("RS:force to move",xy_offset_bonus)
                else:
                    xy_offset_bonus=0
                time.sleep(DELAY_SECOND)
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        with open('runtime_error.log','a+',encoding='utf-8') as f:
            f.writelines(datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\t'+errMsg+'\n')
        print(errMsg)
        sys.exit()