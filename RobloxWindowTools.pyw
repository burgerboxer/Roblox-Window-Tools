import dearpygui.dearpygui as dpg, psutil, ctypes, os, win32gui, win32process, win32con, threading, time

def a(a):
    dpg.add_text(a, parent="b")
    dpg.set_y_scroll("b", dpg.get_y_scroll_max("b"))

def b():
    for c in psutil.process_iter(['pid', 'name']):
        if c.info['name'] == 'RobloxPlayerBeta.exe':
            return c.info['pid']
    return None

def d(e):
    def f(g, h):
        _, i = win32process.GetWindowThreadProcessId(g)
        if i == e:
            h.append(g)
        return True
    j = []
    win32gui.EnumWindows(f, j)
    return j[0] if j else None

def k():
    l = b()
    if l:
        m = d(l)
        if m:
            n = dpg.get_value("o")
            o = win32gui.GetWindowText(m)
            if o != n:
                ctypes.windll.user32.SetWindowTextW(m, n)
            else:
                a("Name is already set you dumbass.")

def p(q, r):
    if os.path.exists(r):
        s = win32gui.LoadImage(
            None, r, win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        if s:
            win32gui.SendMessage(q, win32con.WM_SETICON, win32con.ICON_SMALL, s)
            win32gui.SendMessage(q, win32con.WM_SETICON, win32con.ICON_BIG, s)
        else:
            a(f"Failed to load icon from {r}.")
    else:
        a(f"Icon path {r} does not exist.")

def t():
    u = b()
    if u:
        v = d(u)
        if v:
            w = dpg.get_value("o")
            x = dpg.get_value("y")
            y = win32gui.GetWindowText(v)
            if w and y != w:
                ctypes.windll.user32.SetWindowTextW(v, w)
            if x:
                p(v, x)

def z():
    while True:
        l = b()
        if l:
            aa = f"Roblox Window Tools | {l}"
        else:
            aa = "Roblox Window Tools"
        dpg.set_viewport_title(aa)

        if dpg.get_value("ab"):
            t()

        time.sleep(0.1)

dpg.create_context()

with dpg.window(label="Roblox Window Tools", width=600, height=400):
    dpg.add_text("Rename Roblox Window")
    dpg.add_input_text(hint="Window Title", tag="o")
    dpg.add_button(label="Rename Window", callback=lambda: k())
    
    dpg.add_text("Replace Window Icon")
    dpg.add_input_text(hint="Icon File Path", tag="y")
    dpg.add_button(label="Set Icon", callback=lambda: t())

    dpg.add_checkbox(label="Auto Apply", tag="ab")
    dpg.add_child_window(label="Log", tag="b", width=580, height=200, border=True)

dpg.create_viewport(title="Roblox Window Tools | Initializing", width=615, height=439)
dpg.setup_dearpygui()
dpg.show_viewport()

threading.Thread(target=z, daemon=True).start()

dpg.start_dearpygui()

dpg.destroy_context()
