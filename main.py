import pyautogui as pa
import keyboard
from pynput.keyboard import Listener
from pynput import keyboard
from HandlerPoke import HandlerPoke
from utils import get_loot, move_and_click

player_position = (727, 346)
BP_loot_position = (1273, 835)
poke_list_attack = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8')
battle_position = (1264, 474)
x_battle = 1260
y_battle = 572
RGB_battle = (103, 18, 19)
battle_region = (1247, 404, 182, 101)

handler_poke = HandlerPoke()
def cura():
    pa.moveTo(90, 450)
    pa.click(90, 450, button='left', clicks=2)
    pa.sleep(1.2)
    pa.press('f1')
    pa.sleep(0.5)
    handler_poke.next()


def key_code(key):

    #Parar
    if key == keyboard.Key.esc:
        return False
    
    #Battle List
    if hasattr(key, 'char') and key.char == 'z':
        move_and_click(battle_position, 'left')
        for attack in poke_list_attack:
            pa.press(attack)
          
    #Pegar Loot
    if hasattr(key, 'char') and key.char == 'x':
        get_loot(player_position, BP_loot_position)

    #Next Pokemon
    if hasattr(key, 'char') and key.char == 'e':
        handler_poke.next()

    #Previous Pokemon
    if hasattr(key, 'char') and key.char == 'q':
        handler_poke.previous()

    #Teste auto
    if hasattr(key, 'char') and key.char == 'b':
        move_and_click(battle_position, 'left')
        for attack in poke_list_attack:
            pa.press(attack)       
        handler_poke.next()
        pa.sleep(0.2)
   
    #curar
    if hasattr(key, 'char') and key.char == 'm':
        cura()
    
with Listener(on_press=key_code) as f:
    f.join()




