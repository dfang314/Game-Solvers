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

FLOWER_HARVEST_TIME = 1.9 # time to harvest a flower

W_MOVE_SEC = (None, None) # x, z change for 1 second of holding w
A_MOVE_SEC = (None, None) # x, z change for 1 second of holding a
W_MOVE_SEC_NORM = (None, None) # normalized
A_MOVE_SEC_NORM = (None, None) # normalized

GET_POS_WAIT_TIME = 0.15 # amount of time to wait for coordinates to stabilize

def get_pos():
  time.sleep(GET_POS_WAIT_TIME)
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
  print("Coordinate string is", coordstr)
  time.sleep(GET_POS_WAIT_TIME)
  pos = float(coordstr[:6]), float(coordstr[-6:])
  print("Current position", pos)
  return pos

def calibrate():
  global W_MOVE_SEC, A_MOVE_SEC, W_MOVE_SEC_NORM, A_MOVE_SEC_NORM
  print("Calibrating...")

  startx, startz = get_pos()
  pydirectinput.keyDown("w")
  time.sleep(1)
  pydirectinput.keyUp("w")
  endx, endz = get_pos()
  W_MOVE_SEC = endx - startx, endz - startz
  size = (W_MOVE_SEC[0]**2 + W_MOVE_SEC[1]**2)**0.5
  W_MOVE_SEC_NORM = W_MOVE_SEC[0] / size, W_MOVE_SEC[1] / size
  print("1 second of W affects our coordinates by", W_MOVE_SEC)
  pydirectinput.keyDown("s")
  time.sleep(1)
  pydirectinput.keyUp("s")

  startx, startz = get_pos()
  pydirectinput.keyDown("a")
  time.sleep(1)
  pydirectinput.keyUp("a")
  endx, endz = get_pos()
  A_MOVE_SEC = endx - startx, endz - startz
  size = (A_MOVE_SEC[0]**2 + A_MOVE_SEC[1]**2)**0.5
  A_MOVE_SEC_NORM = A_MOVE_SEC[0] / size, A_MOVE_SEC[1] / size
  print("1 second of A affects our coordinates by", A_MOVE_SEC)
  pydirectinput.keyDown("d")
  time.sleep(1)
  pydirectinput.keyUp("d")

def cycle():
  print("Starting a cycle")
  for flower in FLOWER_PATH:
    x, z = get_pos()
    dx, dz = flower[0] - x, flower[1] - z

    # Use w and a as axes, take scalar projection to find out how much of each to press
    amt_w = dx * W_MOVE_SEC_NORM[0] + dz * W_MOVE_SEC_NORM[1]
    amt_a = dx * A_MOVE_SEC_NORM[0] + dz * A_MOVE_SEC_NORM[1]

    print(f"Walking {amt_w}secs of w and {amt_a}secs of a to get the next flower")
    ws_key = "w" if amt_w > 0 else "s"
    ad_key = "a" if amt_a > 0 else "d"

    pydirectinput.keyDown(ws_key)
    time.sleep(abs(amt_w))
    pydirectinput.keyUp(ws_key)

    pydirectinput.keyDown(ad_key)
    time.sleep(abs(amt_a))
    pydirectinput.keyUp(ad_key)

    pydirectinput.keyDown("e")
    time.sleep(FLOWER_HARVEST_TIME)
    pydirectinput.keyUp("e")

time.sleep(STARTUP_TIME)

calibrate()

cycle()

pyautogui.alert(f"toph hella fatty ong") 