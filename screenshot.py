import pyautogui
import time

time.sleep(3)
im = pyautogui.screenshot(region=(0, 0, 100, 100))
im.show()
