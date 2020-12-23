# see http://msdn.microsoft.com/en-us/library/ms646260(VS.85).aspx for details
import ctypes

MOUSE_LEFT_DOWN=0x0002
MOUSE_LEFT_UP=0x0004
MOUSE_RIGHT_DOWN=0x0008
MOUSE_RIGHT_UP=0x0010

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

def get_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x,pt.y

def move_to(offx=0,offy=0):
    cx,cy=get_pos()
    set_pos(cx+offx,cy+offy)
    return cx+offx,cy+offy

def set_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def click(flag,x,y,updown=1):
    if flag=='left':
        if updown==1:
            ctypes.windll.user32.mouse_event(MOUSE_LEFT_DOWN, x, y, 0,0) # left down
        else:
            ctypes.windll.user32.mouse_event(MOUSE_LEFT_UP, x, y, 0,0) # left up
    elif flag=='right':
        if updown==1:
            ctypes.windll.user32.mouse_event(MOUSE_RIGHT_DOWN, x, y, 0,0) # left down
        else:
            ctypes.windll.user32.mouse_event(MOUSE_RIGHT_UP, x, y, 0,0) # left up
#def rodar():
#    for i in range(0,500,10):
#        set_pos(i,i)
#        time.sleep(0.01)

#if __name__ == "__main__":
#    input('press enter to start testing...')
#    rodar()
#    print(get_pos())
#    move_to(100,-100)
#    cx,cy=get_pos()
#    click('right',cx,cy)