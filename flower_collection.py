import pyautogui
import pydirectinput
import time
import pytesseract

time.sleep(3)

for i in range(10):
  pydirectinput.keyDown("w")
  time.sleep(0.3)
  pydirectinput.keyUp("w")
  im = pyautogui.screenshot(region=(147, 127, 162, 15))
  width, height = im.size
  for x in range(width):
    for y in range(height):
      r, g, b = im.getpixel((x, y))
      if g < r + b - 10:
        im.putpixel((x, y), (0, 0, 0))
  coordstr = pytesseract.image_to_string(im, config="--psm 7 -c tessedit_char_whitelist=0123456789xyz:.-")
  print(coordstr)


pyautogui.alert(f"toph hella fatty ong") 