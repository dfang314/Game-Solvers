import pyautogui
import pydirectinput
import time
import pytesseract

STARTUP_TIME = 3 # seconds it takes before the script starts
SCREENSHOT_REGION = (147, 127, 162, 15) # location of left, top, width, height of the coordinates on the screen
FLOWER_PATH = [(507.09, 449.30),
               (508.40, 383.33),
               (444.30, 436.33),
               (464.05, 509.11),
               (405.50, 489.32),
               (368.67, 511.33),
               (369.95, 406.54),
               (407.46, 309.68),
               (458.15, 366.63),
               (486.50, 297.94)]

time.sleep(STARTUP_TIME)

for i in range(10):
  pydirectinput.keyDown("w")
  time.sleep(0.3)
  pydirectinput.keyUp("w")

  im = pyautogui.screenshot(region=SCREENSHOT_REGION)

  # coordinates are bright green, set all other pixels to black to help ocr
  width, height = im.size
  for x in range(width):
    for y in range(height):
      r, g, b = im.getpixel((x, y))
      if g < r + b - 10:
        im.putpixel((x, y), (0, 0, 0))
  # through trial and error this config is goated
  # output in format
  # mmm.mmynnnn.nn*ooo.oo
  # where mmm.mm is the negative x, nnnn.nn is the y, * is some character (most of the time z) and ooo.oo is the negative z
  coordstr = pytesseract.image_to_string(im, config="--psm 7 -c tessedit_char_whitelist=0123456789yz.")
  xpos = float(coordstr[:6])
  zpos = float(coordstr[-6:])




pyautogui.alert(f"toph hella fatty ong") 