import pyautogui as pa


def move_and_click(position, side_button='right', click=1):
    pa.moveTo(position)
    pa.click(button=side_button, clicks=click)

def get_loot(player_position, BP_loot_position):
    move_and_click(player_position)
    move_and_click(BP_loot_position, 'left', 5)
