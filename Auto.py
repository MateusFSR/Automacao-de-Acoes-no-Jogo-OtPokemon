import pyautogui as pa
import keyboard
from HandlerPoke import HandlerPoke
import time
from utils import get_loot, move_and_click 
from pynput.keyboard import Listener
import threading
import time
from multiprocessing import Process
import time


battle_region = (1245, 366, 192, 188)
battle_position = (1263, 443)
poke_list_attack = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8')
handler_poke = HandlerPoke()
BP_loot_position = (1273, 835)
player_position = (705, 441)

def batalha():
        pa.click(battle_position, button='left')
        pa.sleep(0.2)
        pa.press(poke_list_attack, interval=0.1)
        pa.sleep(0.3)
        handler_poke.next()
        pa.sleep(0.7)
        pa.click(battle_position, button='left')
        pa.sleep(0.2)
        pa.press(poke_list_attack, interval=0.1)
        pa.sleep(0.5)

def verificar_mudanca_imagem():
    while True:
        try:
            # Tente localizar a imagem na região especificada
            battle = pa.locateOnScreen('battle.png', confidence=0.8, region=battle_region)
            
            if battle is not None:
                print("Nenhum Pokemon Encontrado")
                
                # Aguarde um intervalo antes de verificar novamente
                time.sleep(0.5)
            else:
                batalha()        
        except pa.ImageNotFoundException:
                    batalha()
        
        # Aguarde um intervalo antes de verificar novamente
        time.sleep(0.5)

# Inicie a verificação
verificar_mudanca_imagem()

def key_code(key):
    #Pegar Loot
    if hasattr(key, 'char') and key.char == 'x':
        get_loot(player_position, BP_loot_position)

with Listener(on_press=key_code) as f:
    f.join()


