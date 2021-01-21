WINDOWMGR_VERSION="00003A"
import win32gui, win32com.client, win32con, winxpgui, win32api, ctypes
from os import system
from time import sleep
from re import match
from subprocess import Popen,PIPE

"""Encapsulates some calls to the winapi for window management"""
class WindowMgr:
    """ 建構式 """
    def __init__ (self):
        self._handle = None
        self.is_exist = False

    """ find a window by its class_name """
    def find_window(self, class_name, window_name=None):
        self._handle = win32gui.FindWindow(class_name, window_name)

    """Pass to win32gui.EnumWindows() to check all the opened windows"""
    def _window_enum_callback(self, hwnd, wildcard):
        if match(".*?"+wildcard+"*", str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd
            self.is_exist = True

    """ 找視窗(wildcard) """
    ### 找到標題內含wildcard字串的視窗 ###
    def find_window_wildcard(self, wildcard):
        self._handle = None
        self.is_exist = False
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    """ 設cmd標題(cmd_title) """
    ### 設置cmd視窗的標題 ###
    def set_cmd_title(self,cmd_title):
        ctypes.windll.kernel32.SetConsoleTitleW(cmd_title)
        sleep(2)

    """ 當前視窗標題() """
    ### 獲取當前視窗完整標題，傳回值為字串 ###
    def active_window_title(self):
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())

    """ 視窗座標寬高() """
    ### 獲取視窗座標寬高，傳回值為陣列[x,y,w,h] ###
    def get_window_pos_size(self):
        try:
            rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
        except:
            rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        #print("Window %s:" % win32gui.GetWindowText(win32gui.GetForegroundWindow()))
        #print("\tx, y: (%d, %d)" % (x, y))
        #print("\tw, h: (%d, %d)" % (w, h))
        return [x,y,w,h]

    """ 設為前景() """
    ### 將目標視窗設為前景 ###
    def set_foreground(self):
        win32gui.SetForegroundWindow(self._handle)
        #win32gui.ShowWindow(self._handle, win32con.SW_SHOWMAXIMIZED)

    """ 調視窗(tmp_window_state='') """
    ### 設定window狀態:激活並最大化'MAX'、激活並最小化'MIN'、激活並視窗化'' ###
    def set_window_state(self,tmp_window_state=''):
        if tmp_window_state=='MAX':
            win32gui.ShowWindow(self._handle, win32con.SW_SHOWMAXIMIZED)
        elif tmp_window_state=='MIN':
            win32gui.ShowWindow(self._handle, win32con.SW_SHOWMINIMIZED)
        else:
            win32gui.ShowWindow(self._handle, win32con.SW_SHOWNORMAL)

    """ 設定寬高(window_width,window_height) """
    ### 設定目標視窗的寬度及高度 ###
    def set_window_width_height(self,window_width,window_height):
        self.set_window_state('')
        win32gui.MoveWindow(self._handle,0,0,window_width,window_height,True)

    """ 休眠(tmp_sec) """
    ### 程式暫停tmp_sec秒後執行，tmp_sec最小單位為0.1 ###
    def sleep_a_while(self,tmp_sec):
        sleep(tmp_sec)

    """ 關閉當前視窗() """
    ### 把目前是前景的視窗關閉 ###
    def close_current_window(self):
        win32gui.PostMessage(self._handle,win32con.WM_CLOSE,0,0)

    """ 結束程序(process_name) """
    ### 用taskkill /f /im 的dos cmd強制目標程式結束運作 ###
    def end_process(self,process_name):
        try:
            system("taskkill /f /im "+process_name)
        except:
            pass

    """ 重置() """
    ### 執行找視窗()後要找另一個目標視窗前，需先執行 重置() ###
    def reset(self):
        """ 暫時想不到怎麼形容，就是在兩個程式間切換用 """
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

    """ 執行程式(program_loc, wildcard, program_param='') """
    ### 執行外部程式，先偵測程式是否已執行，若無才執行外部程式，程式執行後會把標題含wildcard字串的視窗設為目標視窗 ###
    def run_program(self, program_loc, wildcard, program_param=''):
        self.find_window_wildcard(wildcard)
        if not self.is_exist:
            #subprocess.Popen(program_loc)
            cmd = program_loc if program_param=='' else program_loc+" "+program_param
            Popen(cmd, stdout=PIPE, creationflags=0x08000000)
            while not self.is_exist:
                #print(self.is_exist)
                msg_str = 'finding window please wait...'
                print(msg_str, end='')
                print('\b' * len(msg_str), end='', flush=True)
                self.find_window_wildcard(wildcard)
                #self.sleep_a_while(0.5)

    """ 設為最上層視窗(wildcard,win_w=320,win_h=240,set_top=True) """
    ### 可利用本函式將目標視窗設為永遠置頂(set_top=True)或不要永遠置頂(set_top=False) ###
    def set_window_on_top(self, wildcard,win_w=320,win_h=240,set_top=True):
        self.reset()
        self.find_window_wildcard(wildcard)
        self.set_foreground()
        if set_top==True:
            win32gui.SetWindowPos(self._handle,win32con.HWND_TOPMOST,0,0,win_w,win_h,0)
            #print("將視窗"+wildcard+"設為最上層視窗\n視窗width: "+str(win_w)+" 視窗height: "+str(win_h))
        else:
            win32gui.SetWindowPos(self._handle,win32con.HWND_NOTOPMOST,0,0,win_w,win_h,0)
            #print("將視窗"+wildcard+"設為非上層視窗\n視窗width: "+str(win_w)+" 視窗height: "+str(win_h))
        sleep(0.5)

    """ 半透明視窗(wildcard,alpha_val=180) """
    ### 將目標視窗設為半透明狀態(alpha_val值範圍0-255) ###
    def set_window_alpha(self, wildcard, alpha_val=180):
        self.reset()
        self.find_window_wildcard(wildcard)
        self.set_foreground()
        win32gui.SetWindowLong (self._handle, win32con.GWL_EXSTYLE, win32gui.GetWindowLong (self._handle, win32con.GWL_EXSTYLE ) | win32con.WS_EX_LAYERED )
        winxpgui.SetLayeredWindowAttributes(self._handle, win32api.RGB(0,0,0), alpha_val, win32con.LWA_ALPHA)
