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

GET_POS_WAIT_TIME = 0.15 # amount of time to wait for coordinates to stabilize

def hold_key(key, duration):
  pydirectinput.keyDown(key)
  time.sleep(duration)
  pydirectinput.keyUp(key)

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
  coordstr = coordstr[:-1] # parser always gives a newline at the end
  time.sleep(GET_POS_WAIT_TIME)
  pos = float(coordstr[:6]), float(coordstr[-6:])
  print("Current position", pos)
  return pos

def calibrate():
  global W_MOVE_SEC, A_MOVE_SEC
  print("Calibrating...")

  startx, startz = get_pos()
  hold_key("w", 0.4)
  endx, endz = get_pos()
  W_MOVE_SEC = (endx - startx) / 0.4, (endz - startz) / 0.4
  hold_key("s", 0.4)

  startx, startz = get_pos()
  hold_key("a", 0.4)
  endx, endz = get_pos()
  A_MOVE_SEC = (endx - startx) / 0.4, (endz - startz) / 0.4
  hold_key("d", 0.4)

def cycle():
  print("Starting a cycle")
  for flower in FLOWER_PATH:
    x, z = get_pos()
    dx, dz = flower[0] - x, flower[1] - z

    # Use w and a are not necessarily axes due to inaccuracies
    # We want
    # W_MOVE_SEC[0]*amt_w + A_MOVE_SEC[0]*amt_a = dx
    # W_MOVE_SEC[1]*amt_w + A_MOVE_SEC[1]*amt_a = dz
    # [W[0] A[0]    [amt_w    [dx
    #  W[1] A[1]] @  amt_a] =  dz]
    # [amt_w    [A[1] -A[0]                              [dx
    #  amt_a] =  -W[1] W[0]] / (W[0]*A[1] - A[0]*W[1]) @  dz]
    # amt_w = (dx*A[1] - dz*A[0]) / (W[0]*A[1] - A[0]*W[1])
    # amt_a = (-dx*W[1] + dz*W[0]) / (W[0]*A[1] - A[0]*W[1])

    det = W_MOVE_SEC[0] * A_MOVE_SEC[1] - A_MOVE_SEC[0] * W_MOVE_SEC[1]
    amt_w = (dx * A_MOVE_SEC[1] - dz * A_MOVE_SEC[0]) / det
    amt_a = (-dx * W_MOVE_SEC[1] + dz * W_MOVE_SEC[0]) / det

    ws_key = "w" if amt_w > 0 else "s"
    ad_key = "a" if amt_a > 0 else "d"

    hold_key(ws_key, abs(amt_w))
    hold_key(ad_key, abs(amt_a))

    hold_key("e", FLOWER_HARVEST_TIME)
  
pyautogui.FAILSAFE = True

time.sleep(STARTUP_TIME)

calibrate()

cycle()

pyautogui.alert(f"toph hella fatty ong") 