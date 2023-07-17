import sys
import time
import threading
from playsound import playsound
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key, KeyCode


def m_playsound(file):
    def ps():
        playsound(file)
    t = threading.Thread(target=ps)
    t.start()


print("开/关连点：x\n"
      "- 开启后按住shift启用\n"
      "切换左右键：PgUp\n"
      "退出：end")
m_playsound("data/on.wav")

delay = 0.0009  # 每次点击的间隔时间
button = Button.right  # 使用右键点击

# 鼠标对象
mouse = Controller()

# 键盘监听器相关变量
current_key = None
stop_event = threading.Event()

on_or_off = False
left_or_right = False


def presss(key):
    global current_key
    global on_or_off
    global button
    global left_or_right
    key_list = [key]
    if KeyCode(char='x') in key_list or KeyCode(char='X') in key_list:  # 设置按下的触发按键
        if on_or_off:
            on_or_off = False
            m_playsound("data/off.wav")
            print('禁用了连点')
        else:
            on_or_off = True
            m_playsound("data/on.wav")
            print('启用了连点')

    if on_or_off:
        if Key.shift in key_list:  # 设置按下的触发按键
            current_key = key
            print(f'触发了 {button} 连点')
            t = threading.Thread(target=click)
            t.start()

    if Key.page_up in key_list:
        if left_or_right:
            button = Button.right
            left_or_right = False
            print('切换到右键连点')
            m_playsound("data/on.wav")
            time.sleep(0.1)
            m_playsound("data/on.wav")

        else:
            button = Button.left
            left_or_right = True
            print('切换到左键连点')
            m_playsound("data/off.wav")
            time.sleep(0.1)
            m_playsound("data/off.wav")

    if Key.end in key_list:
        m_playsound("data/off.wav")
        listener.stop()
        print("程序已关闭")
        sys.exit(0)


def on_press(key):
    t = threading.Thread(target=presss(key))
    t.start()


def on_release(key):
    global current_key
    if key == current_key:
        current_key = None


def click():
    global on_or_off
    while current_key is not None and not stop_event.is_set() and on_or_off:
        mouse.click(button)
        time.sleep(delay)


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    stop_event.set()
