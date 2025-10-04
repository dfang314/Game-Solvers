# In order to bypass OCR, image parsing, etc. and the related headaches,
# we just blindly click based on hard coded values. Therefore, this
# program only crafts one type of pill, and each run requires reconfiging
# some global constants.

import pyautogui
import pydirectinput
import time

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

CLICK_DELAY = 0.2 # delay between clicks

def click_at(x, y):
  time.sleep(CLICK_DELAY)
  pydirectinput.moveTo(x, y)
  pydirectinput.click()

def ordinal(x):
    suffix = 'th'
    if (x % 100) < 11 or (x % 100) > 13:
        suffix = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][x % 10]
    return str(x) + suffix

def craft_pill():
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

time.sleep(STARTUP_TIME - CLICK_DELAY)

for craft_amt in range(CRAFTS):
  print(f"Crafting for the {ordinal(craft_amt)} time")
  craft_pill()

pyautogui.alert(f"toph hella fatty ong") 
