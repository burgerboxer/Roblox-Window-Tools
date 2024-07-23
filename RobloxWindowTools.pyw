import dearpygui.dearpygui as dpg
import psutil
import ctypes
import os
import win32gui
import win32process
import win32con
import threading
import time

def log_message(message):
    dpg.add_text(message, parent="log_window")
    dpg.set_y_scroll("log_window", dpg.get_y_scroll_max("log_window"))

def find_roblox_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'RobloxPlayerBeta.exe':
            return proc.info['pid']
    return None

def get_window_handle_by_pid(pid):
    def enum_windows_callback(hwnd, window_list):
        _, proc_id = win32process.GetWindowThreadProcessId(hwnd)
        if proc_id == pid:
            window_list.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows[0] if windows else None

def rename_window():
    pid = find_roblox_process()
    if pid:
        hwnd = get_window_handle_by_pid(pid)
        if hwnd:
            new_title = dpg.get_value("window_title")
            current_title = win32gui.GetWindowText(hwnd)
            if current_title != new_title:
                ctypes.windll.user32.SetWindowTextW(hwnd, new_title)
            else:
                log_message("Name is already set.")

def set_window_icon(hwnd, icon_path):
    if os.path.exists(icon_path):
        icon_handle = win32gui.LoadImage(
            None, icon_path, win32con.IMAGE_ICON, 0, 0, 
            win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
        if icon_handle:
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, icon_handle)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, icon_handle)
        else:
            log_message(f"Failed to load icon from {icon_path}.")
    else:
        log_message(f"Icon path {icon_path} does not exist.")

def apply_changes():
    pid = find_roblox_process()
    if pid:
        hwnd = get_window_handle_by_pid(pid)
        if hwnd:
            new_title = dpg.get_value("window_title")
            icon_path = dpg.get_value("icon_path")
            current_title = win32gui.GetWindowText(hwnd)
            if new_title and current_title != new_title:
                ctypes.windll.user32.SetWindowTextW(hwnd, new_title)
            if icon_path:
                set_window_icon(hwnd, icon_path)

def update_viewport_title():
    while True:
        pid = find_roblox_process()
        if pid:
            title = f"Roblox Window Tools | {pid}"
        else:
            title = "Roblox Window Tools"
        dpg.set_viewport_title(title)

        if dpg.get_value("auto_apply"):
            apply_changes()

        time.sleep(0.1)

dpg.create_context()

with dpg.window(label="Roblox Window Tools", width=600, height=400):
    dpg.add_text("Rename Roblox Window")
    dpg.add_input_text(hint="Window Title", tag="window_title")
    dpg.add_button(label="Rename Window", callback=rename_window)
    
    dpg.add_text("Replace Window Icon")
    dpg.add_input_text(hint="Icon File Path", tag="icon_path")
    dpg.add_button(label="Set Icon", callback=apply_changes)

    dpg.add_checkbox(label="Auto Apply", tag="auto_apply")
    dpg.add_child_window(label="Log", tag="log_window", width=580, height=200, border=True)

dpg.create_viewport(title="Roblox Window Tools | Initializing", width=615, height=439)
dpg.setup_dearpygui()
dpg.show_viewport()

threading.Thread(target=update_viewport_title, daemon=True).start()

dpg.start_dearpygui()

dpg.destroy_context()
