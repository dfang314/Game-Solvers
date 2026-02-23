# In order to bypass OCR, we don't try to fully understand the game state.
# Instead, we just check basic intersection Therefore, this
# program only crafts one type of pill, and each run requires reconfiging
# some global constants.

import pyautogui
import pydirectinput
import time
from PIL import Image, ImageChops

# ===== CHANGE THESE BEFORE EVERY RUN ===== #
CRAFTS = 5 # amount of times to craft

HERB_1_ROW = 1 # choose from 1, 2, or 3
HERB_1_COL = 1 # choose from 1, 2, 3, ..., 10

HERB_2_ROW = 1 # choose from 1, 2, or 3
HERB_2_COL = 1 # choose from 1, 2, 3, ..., 10

HERB_3_ROW = 1 # choose from 1, 2, or 3
HERB_3_COL = 1 # choose from 1, 2, 3, ..., 10

HERB_4_ROW = 1 # choose from 1, 2, or 3
HERB_4_COL = 1 # choose from 1, 2, 3, ..., 10
# ========================================= #

STARTUP_TIME = 3 # seconds it takes before the script starts

AMT_ROWS = 3
AMT_COLS = 10

TOP_LEFT_X = 550 # centered x coordinate of the top left herb
TOP_LEFT_Y = 750 # centered y coordinate of the top left herb

USE_X_CHANGE = 325 - TOP_LEFT_X # x displacement from the herb icon to the use button
USE_Y_CHANGE = 990 - TOP_LEFT_Y # y displacement from the herb icon to the use button

GRID_D = 200 # displacement from one grid item to the next

CRAFT_X = 1700 # x of craft button
CRAFT_Y = 625 # y of craft button

JIGGLE_X = 5 # amount to move x when jiggling
JIGGLE_Y = 5 # amount to move y when jiggling

HERB_REGION_1 = (1030, 400, 120, 120) # region to screenshot to see if first herb is placed
HERB_REGION_2 = (1260, 400, 120, 120) # region to screenshot to see if second herb is placed
HERB_REGION_3 = (1490, 400, 120, 120) # region to screenshot to see if third herb is placed
HERB_REGION_4 = (1720, 400, 120, 120) # region to screenshot to see if fourth herb is placed

MIN_DIFF_HERB_IMG = 1000 # minimum difference between an image and the image of no herb to classify as "herb"

KEEP_CHECKING = False

def click_at(x, y):
  # pydirectinput doesn't support non-instant moving so we need to jiggle
  pydirectinput.moveTo(x + JIGGLE_X, y + JIGGLE_Y)
  pydirectinput.moveTo(x, y) 
  pydirectinput.click()

def ordinal(x):
  suffix = 'th'
  if (x % 100) < 11 or (x % 100) > 13:
    suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][x % 10]
  return str(x) + suffix

def has_herb(img, no_herb_img):
  diff_img = ImageChops.difference(img, no_herb_img)
  diff = sum([pixel[0] + pixel[1] + pixel[2] for pixel in list(diff_img.getdata())])
  print("Found a difference of", diff)
  return diff > MIN_DIFF_HERB_IMG

def craft_pill(no_herb_img):
  if KEEP_CHECKING:
    while not has_herb(pyautogui.screenshot(region=HERB_REGION_1), no_herb_img):
      click_at(TOP_LEFT_X + (HERB_1_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_1_ROW - 1) * GRID_D)
      click_at(TOP_LEFT_X + (HERB_1_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_1_ROW - 1) * GRID_D + USE_Y_CHANGE)
    while not has_herb(pyautogui.screenshot(region=HERB_REGION_2), no_herb_img):
      click_at(TOP_LEFT_X + (HERB_2_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_2_ROW - 1) * GRID_D)
      click_at(TOP_LEFT_X + (HERB_2_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_2_ROW - 1) * GRID_D + USE_Y_CHANGE)
    while not has_herb(pyautogui.screenshot(region=HERB_REGION_3), no_herb_img):
      click_at(TOP_LEFT_X + (HERB_3_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_3_ROW - 1) * GRID_D)
      click_at(TOP_LEFT_X + (HERB_3_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_3_ROW - 1) * GRID_D + USE_Y_CHANGE)
    while not has_herb(pyautogui.screenshot(region=HERB_REGION_4), no_herb_img):
      click_at(TOP_LEFT_X + (HERB_4_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_4_ROW - 1) * GRID_D)
      click_at(TOP_LEFT_X + (HERB_4_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_4_ROW - 1) * GRID_D + USE_Y_CHANGE)
    while has_herb(pyautogui.screenshot(region=HERB_REGION_1), no_herb_img):
      click_at(CRAFT_X, CRAFT_Y)
  else:
    click_at(TOP_LEFT_X + (HERB_1_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_1_ROW - 1) * GRID_D)
    click_at(TOP_LEFT_X + (HERB_1_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_1_ROW - 1) * GRID_D + USE_Y_CHANGE)
    click_at(TOP_LEFT_X + (HERB_2_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_2_ROW - 1) * GRID_D)
    click_at(TOP_LEFT_X + (HERB_2_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_2_ROW - 1) * GRID_D + USE_Y_CHANGE)
    click_at(TOP_LEFT_X + (HERB_3_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_3_ROW - 1) * GRID_D)
    click_at(TOP_LEFT_X + (HERB_3_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_3_ROW - 1) * GRID_D + USE_Y_CHANGE)
    click_at(TOP_LEFT_X + (HERB_4_COL - 1) * GRID_D, TOP_LEFT_Y + (HERB_4_ROW - 1) * GRID_D)
    click_at(TOP_LEFT_X + (HERB_4_COL - 1) * GRID_D + USE_X_CHANGE, TOP_LEFT_Y + (HERB_4_ROW - 1) * GRID_D + USE_Y_CHANGE)
    click_at(CRAFT_X, CRAFT_Y)
  
pyautogui.FAILSAFE = True
pydirectinput.PAUSE = 0.02 # reduce pause time because there is so much lag in jiggling and clicking so much

no_herb_img = Image.open('no_herb.png')

time.sleep(STARTUP_TIME)

for craft_amt in range(CRAFTS):
  print(f"Crafting for the {ordinal(craft_amt+1)} time")
  craft_pill(no_herb_img)

pyautogui.alert(f"toph hella fatty ong") 
