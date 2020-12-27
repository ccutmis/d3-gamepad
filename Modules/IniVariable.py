from pynput.keyboard import Key
from math import pi,sin,cos

class IniVariable:
    def __init__ (self):
        self.KEY_MAP={"alt":Key.alt,"alt_l":Key.alt_l,"alt_r":Key.alt_r,"backspace":Key.backspace,"caps_lock":Key.caps_lock,"cmd":Key.cmd,"cmd_r":Key.cmd_r,"ctrl":Key.ctrl,"ctrl_l":Key.ctrl_l,"ctrl_r":Key.ctrl_r,"delete":Key.delete,"down":Key.down,"end":Key.end,"enter":Key.enter,"esc":Key.esc,"f1":Key.f1,"f10":Key.f10,"f11":Key.f11,"f12":Key.f12,"f13":Key.f13,"f14":Key.f14,"f15":Key.f15,"f16":Key.f16,"f17":Key.f17,"f18":Key.f18,"f19":Key.f19,"f2":Key.f2,"f20":Key.f20,"f3":Key.f3,"f4":Key.f4,"f5":Key.f5,"f6":Key.f6,"f7":Key.f7,"f8":Key.f8,"f9":Key.f9,"home":Key.home,"insert":Key.insert,"left":Key.left,"menu":Key.menu,"num_lock":Key.num_lock,"page_down":Key.page_down,"page_up":Key.page_up,"pause":Key.pause,"print_screen":Key.print_screen,"right":Key.right,"scroll_lock":Key.scroll_lock,"shift":Key.shift,"shift_r":Key.shift_r,"space":Key.space,"tab":Key.tab,"up":Key.up}
        self.cx=None
        self.cy=None
        self.triger_stat=[0,0]
        self.stick_stat=[0,0]
        self.stick_degree=[0,0]
        self.xy_offset=None
        self.xy_offset_bonus=0
        self.onoff_list=[]
        self.deg_dict=None
        self.last_thumb_dict={"l_thumb_x":0,"l_thumb_y":0,"r_thumb_x":0,"r_thumb_y":0}
        self.x_center=-1
        self.y_center=-1
        self.win_pos_size=[0,0,0,0]
        self.active_win_title=None
        self.key_config=None
        self.set_left_controller_move_and_click=None
        self.left_controller_click_val =None
        self.xy_offset_unit =None
        self.delay_second =None
        self.y_center_offset =None
        self.btn_dict =None
        self.btn2_dict =None
        self.onoff_list =None
        self.debug_mode =None
        self.key_onoff_mode = None
        self.keys_stat_last = None
        self.current_onoff = None
        self.in_active_win = None
        self.elapsed_time = None
        self.stick_info=[None,None]

    def gent_degree_dict(self,divisions=360,radius=10):
        #divisions,radius=360,10
        out_dict={}
        # the difference between angles in radians -- don't bother with degrees
        angle = 2 * pi / divisions
        # a list of all angles using a list comprehension
        angles = [i*angle for i in range(divisions)]
        oi=0
        for a in angles:
            out_dict[oi]=[int(radius*sin(a)),(int(radius*cos(a)))]
            oi+=1
        return out_dict