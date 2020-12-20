# 需安裝的套件 pypiwin32 pynput==1.6.8
# 版本更新項目 追加ABXY自動連按設定(xinput.ini)及功能實作(xpad.py)

VERSION="0003C"

import time
from Modules.XInput import *
import Modules.mouse_api as Mouse
from pynput.keyboard import Key, Controller
from datetime import datetime
from Modules.WindowMgr import *
import traceback,sys,msvcrt

if __name__ == "__main__":
    try:
        ini_filename="xinput.ini"
        if len(sys.argv)>1 and sys.argv[1]!="" and (sys.argv[1]).split(".")[1]=="ini":
            ini_filename=sys.argv[1]
        #讀取 xinput.ini參數
        with open(ini_filename,"r",encoding="utf-8") as f:
            tmp_content=f.read()
        f.close()
        exec(tmp_content)

        set_deadzone(DEADZONE_TRIGGER,10)
        
        controller1=get_connected()
        if(controller1[0]==True):
            print("-------------------------------")
            print("偵測到控制器 在此視窗中按下 [←Backspace] 可關閉程式")
            print("或同時按住控制器:(LEFT_SHOULDER)+(RIGHT_SHOULDER)+(X)關閉程式")
            print("程式版本:"+VERSION+"\t監控視窗:"+ACTIVE_WIN_TITLE)
            print("-------------------------------")
        else:
            print("未偵測到控制器，程式結束。")
            sys.exit()
        w=WindowMgr()
        #全域變數區.START
        from Modules.IniVariable import *
        global_var=IniVariable()
        global_var.cx,global_var.cy=Mouse.get_pos()
        global_var.xy_offset=XY_OFFSET_UNIT
        global_var.deg_dict=global_var.gent_degree_dict(360,int(XY_OFFSET_UNIT))
        global_var.active_win_title=ACTIVE_WIN_TITLE
        global_var.key_config=KEY_CONFIG
        global_var.set_left_controller_move_and_click=SET_LEFT_CONTROLLER_MOVE_AND_CLICK
        global_var.left_controller_click_val =LEFT_CONTROLLER_CLICK_VAL
        global_var.xy_offset_unit =XY_OFFSET_UNIT
        global_var.delay_second =DELAY_SECOND
        global_var.y_center_offset =Y_CENTER_OFFSET
        global_var.btn_dict =BTN_DICT
        global_var.btn2_dict =BTN2_DICT
        global_var.onoff_list=[]
        global_var.debug_mode =DEBUG_MODE
        global_var.key_onoff_mode=KEY_ONOFF_MODE
        global_var.keys_stat_last=[False,False,False,False,False,False,False,False,False,False,False,False,False,False]
        global_var.current_onoff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        global_var.in_active_win=False
        #全域變數區.END
        from Modules.MyHandler import *
        handler = MyHandler(0,global_var_obj=global_var) # initialize handler object
        thread = GamepadThread(handler)                 # initialize controller thread
        while 1:
            if handler.global_var.keys_stat_last[2]==True and handler.global_var.keys_stat_last[11]==True and handler.global_var.keys_stat_last[11]==True:
                sys.exit()
            if msvcrt.kbhit() and msvcrt.getch() == chr(8).encode():
                sys.exit()
            #判斷當前視窗完整標題文字是否包含 ACTIVE_WIN_TITLE 設定之文字，若是才繼續後續處理...
            if ACTIVE_WIN_TITLE in w.active_window_title():
                handler.global_var.in_active_win=True
                handler.global_var.win_pos_size=w.get_window_pos_size() #[x,y,w,h]
                time.sleep(DELAY_SECOND)
                handler.global_var.x_center=int(handler.global_var.win_pos_size[0]+(handler.global_var.win_pos_size[2]/2))
                handler.global_var.y_center=int(handler.global_var.win_pos_size[1]+(handler.global_var.win_pos_size[3]/2)+(Y_CENTER_OFFSET))
                if handler.global_var.stick_stat[0]==2:
                    if handler.global_var.xy_offset_bonus<20: handler.global_var.xy_offset_bonus+=0.5
                    xx,yy=handler.deg_to_xy(handler.global_var.deg_dict,handler.global_var.stick_degree[0])
                    Mouse.set_pos(handler.global_var.x_center+xx*handler.global_var.xy_offset_unit*2,handler.global_var.y_center+yy*handler.global_var.xy_offset_unit*2)
                    if SET_LEFT_CONTROLLER_MOVE_AND_CLICK==True:
                        handler.kb_press_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                        time.sleep(DELAY_SECOND)
                        handler.kb_release_eval_key(LEFT_CONTROLLER_CLICK_VAL)
                elif handler.global_var.stick_stat[1]==2:
                    if handler.global_var.xy_offset_bonus<20: handler.global_var.xy_offset_bonus+=0.5
                    xx,yy=handler.deg_to_xy(handler.global_var.deg_dict,handler.global_var.stick_degree[1])
                    xx,yy=int(xx*handler.global_var.xy_offset_bonus),int(yy*handler.global_var.xy_offset_bonus)
                    Mouse.move_to(xx,yy)
                else:
                    handler.global_var.xy_offset_bonus=0
                if len(handler.global_var.onoff_list)>0:
                    for i in handler.global_var.onoff_list:
                        handler.kb_press_eval_key(i)
                        time.sleep(DELAY_SECOND)
                        handler.kb_release_eval_key(i)
            else:
                handler.global_var.in_active_win=False
            time.sleep(DELAY_SECOND)
            #print(handler.global_var.onoff_list)
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
