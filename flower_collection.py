import pyautogui
import pydirectinput
import time
import pytesseract
from PIL import Image

STARTUP_TIME = 3 # seconds it takes before the script starts

IMAGE_RESIZE = 3 # ratio of resizing to help image parsing
SCREENSHOT_REGION = (166, 128, 143, 14) # location of left, top, width, height of the coordinates on the screen

FLOWER_PATH = [(507.09, 449.30),
               (507.40, 398.33),
               (444.30, 436.33),
               (464.05, 509.11),
               (405.50, 489.32),
               (380.17, 490.33),
               (369.95, 406.54),
               (407.46, 309.68),
               (458.15, 366.63),
               (486.50, 297.94)]

FLOWER_HARVEST_TIME = 1.4 # time to harvest a flower

# These globals are related to calibration. Some are not usable until calibration is complete
CALIBRATION_SEC = 0.4 # how long to move for w and a during calibration
W_MOVE_SEC = (None, None) # x, z change for 1 second of holding w
A_MOVE_SEC = (None, None) # x, z change for 1 second of holding a

GET_POS_TRIES = 3 # amount of times to try get_pos until you crash
JIGGLE_TIME = 0.01 # time to move to change position when retrying get_pos
GET_POS_WAIT_TIME = 0.1 # amount of time to wait for coordinates to stabilize

def hold_keys(keys, duration):
  for key in keys:
    pydirectinput.keyDown(key)
  time.sleep(duration)
  for key in keys:
    pydirectinput.keyUp(key)

def ordinal(x):
  suffix = 'th'
  if (x % 100) < 11 or (x % 100) > 13:
    suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][x % 10]
  return str(x) + suffix

def get_pos():
  time.sleep(GET_POS_WAIT_TIME)

  for try_number in range(1, GET_POS_TRIES + 1):
    im = pyautogui.screenshot(region=SCREENSHOT_REGION)

    # coordinates are bright green, filter into black onto white text
    width, height = im.size
    im = im.resize((width*IMAGE_RESIZE, height*IMAGE_RESIZE), resample=Image.BILINEAR)
    width, height = im.size
    for x in range(width):
      for y in range(height):
        r, g, b = im.getpixel((x, y))
        if g > 180 and r < 100 and b < 100:
          im.putpixel((x, y), (0, 0, 0))
        else:
          im.putpixel((x, y), (255, 255, 255))
    
    # through trial and error this config is goated
    # output in format mmmmmynnnnnn*ooooo

    # mmm[.]mm is the negative x,
    # nnnn[.]nn is the y,
    # * is some character (most of the time z),
    # ooo[.]oo is the negative z
    coordstr = pytesseract.image_to_string(im, config="--psm 7 -c tessedit_char_whitelist=0123456789yz")
    coordstr = coordstr[:-1] # parser always gives a newline at the end
    try:
      pos = float(coordstr[:5]) / 100, float(coordstr[-5:]) / 100
      print("Current position", pos)
      return pos
    except ValueError:
      print(f"Failed to parse coordinates {coordstr}. This is the {ordinal(try_number)} fail in a row.")
      hold_keys(["w", "a"], JIGGLE_TIME)
      continue
  print("Max amount of retries reached and still couldn't parse coordinates.")
  raise ValueError(f"Couldn't parse coordinates")

def calibrate():
  global W_MOVE_SEC, A_MOVE_SEC
  print("Calibrating...")

  startx, startz = get_pos()
  hold_keys(["w"], CALIBRATION_SEC)
  endx, endz = get_pos()
  W_MOVE_SEC = (endx - startx) / CALIBRATION_SEC, (endz - startz) / CALIBRATION_SEC
  hold_keys(["s"], CALIBRATION_SEC)

  startx, startz = get_pos()
  hold_keys(["a"], CALIBRATION_SEC)
  endx, endz = get_pos()
  A_MOVE_SEC = (endx - startx) / CALIBRATION_SEC, (endz - startz) / CALIBRATION_SEC
  hold_keys(["d"], CALIBRATION_SEC)

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

    amt_w = abs(amt_w)
    amt_a = abs(amt_a)

    hold_keys([ws_key], amt_w)
    hold_keys([ad_key], amt_a)

    # new flower needs to get pos so we can start that while still harvesting this flower
    hold_keys(["e"], FLOWER_HARVEST_TIME - GET_POS_WAIT_TIME) 
  
pyautogui.FAILSAFE = True

time.sleep(STARTUP_TIME)

calibrate()

for cycle_num in range(10):
  print("Starting cycle number", cycle_num)
  cycle()

pyautogui.alert(f"toph hella fatty ong") 