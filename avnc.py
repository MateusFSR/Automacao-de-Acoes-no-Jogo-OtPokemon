import tkinter as tk
from threading import Thread
import pyautogui as pa
import time
from pynput.keyboard import Listener
import threading
import keyboard

battle_region = (1245, 366, 192, 188)
poke_list_attack = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8')

class PosicaoBatalhaMixin:
    def capturar_posicao_batalha(self):
        keyboard.wait('h')
        posicao = pa.position()

        # Extrai os valores de X e Y separadamente
        x = posicao.x
        y = posicao.y

        self.battle_position = (x, y)
        print(self.battle_position)

    def batalha(self):
        if self.battle_position:
            print(self.battle_position)
            #pa.click(self.battle_position, button='left')
            #pa.sleep(0.2)
            #pa.press(poke_list_attack, interval=0.1)
            #pa.sleep(0.3)
            #pa.sleep(0.7)
            #pa.click(self.battle_position, button='left')
            #pa.sleep(0.2)
            #pa.press(poke_list_attack, interval=0.1)
            #pa.sleep(0.5)


class SegundaTela(tk.Frame, PosicaoBatalhaMixin):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=2, column=1, sticky="nsew")
        self.criar_widgets()
        self.battle_position = None

    def criar_widgets(self):
        label = tk.Label(self, text="Configurar Picks 🔧", font=("Arial Black", 16))
        label.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky='nsew')

        # Botao Para Capturar Posicao de Batalha
        frame_posicao = tk.Frame(self)
        frame_posicao.grid(row=1, column=0)
        self.botao_capturar = tk.Button(frame_posicao, text="Capturar valor", command=self.capturar_posicao_batalha)
        self.botao_capturar.grid(row=1, column=0)

class PrimeiraTela(tk.Frame, PosicaoBatalhaMixin):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=2, column=1, sticky="nsew")
        self.criar_widgets()
        self.battle_position = None

    def criar_widgets(self):
        label = tk.Label(self, text="Poke AutoBot 🍚", font=("Arial Black", 16), fg="#FF0000")
        label.grid(row=0, column=0, pady=5, padx=5, columnspan=2, sticky='nsew')

        # Adicione widgets específicos para a primeira tela aqui
        caminho_icone = 'pokeball.ico'
        self.master.iconbitmap(caminho_icone)

        self.master.attributes('-topmost', True)

        frame_verificar = tk.Frame(self)
        frame_verificar.grid(row=1, column=0, padx=10, pady=5)

        self.start_verificar_button = tk.Button(frame_verificar, text="Iniciar AutoBattle", command=self.iniciar_verificar, font=('Verdana', 8))
        self.start_verificar_button.grid(row=0, column=0, pady=5)

        self.stop_verificar_button = tk.Button(frame_verificar, text="Parar AutoBattle", command=self.parar_verificar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_verificar_button.grid(row=1, column=0, pady=5)

        frame_capturar = tk.Frame(self)
        frame_capturar.grid(row=1, column=1, padx=10, pady=5)

        self.start_capturar_button = tk.Button(frame_capturar, text="Iniciar AutoCatch", command=self.iniciar_capturar, font=('Verdana', 8))
        self.start_capturar_button.grid(row=0, column=0, pady=5)

        self.stop_capturar_button = tk.Button(frame_capturar, text="Parar AutoCatch", command=self.parar_capturar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_capturar_button.grid(row=1, column=0, pady=5)

        self.running_capturar = False
        self.running_verificar = False

    def capturar_pokemon(self):
        while self.running_capturar:
            try:
                capturar = pa.locateOnScreen('capturar1.png', confidence=0.8)

                if capturar is not None:
                    print("Pokemon Encontrado")
                    pa.press('j')
                    pa.moveTo(capturar)
                    pa.sleep(0.4)
                    pa.click(capturar, button='left')
                    pa.sleep(2.0)
                    pa.press('right', presses=3)
                    time.sleep(0.5)
                else:
                    print("Nenhum Pokemon Encontrado")
                    time.sleep(0.5)
            except pa.ImageNotFoundException:
                print("Nenhum Pokemon Encontrado")
                time.sleep(0.5)

    def verificar_mudanca_imagem(self):
        while self.running_verificar:
            try:
                battle = pa.locateOnScreen('battle.png', confidence=0.8, region=battle_region)

                if battle is not None:
                    print("Nenhum Pokemon Encontrado")
                    time.sleep(0.5)
                else:
                    self.batalha()
            except pa.ImageNotFoundException:
                self.batalha()

    def iniciar_capturar(self):
        self.start_capturar_button.config(state=tk.DISABLED)
        self.stop_capturar_button.config(state=tk.NORMAL)
        self.running_capturar = True

        self.thread_capturar = Thread(target=self.capturar_pokemon)
        self.thread_capturar.start()

    def parar_capturar(self):
        self.start_capturar_button.config(state=tk.NORMAL)
        self.stop_capturar_button.config(state=tk.DISABLED)
        self.running_capturar = False
        self.thread_capturar.join()

    def iniciar_verificar(self):
        self.start_verificar_button.config(state=tk.DISABLED)
        self.stop_verificar_button.config(state=tk.NORMAL)
        self.running_verificar = True

        self.thread_verificar = Thread(target=self.verificar_mudanca_imagem)
        self.thread_verificar.start()

    def parar_verificar(self):
        self.start_verificar_button.config(state=tk.NORMAL)
        self.stop_verificar_button.config(state=tk.DISABLED)
        self.running_verificar = False
        self.thread_verificar.join()

       

class Aplicativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Bot")
        self.frame_atual = None

        self.botao_ir_para_primeira_tela = tk.Button(root, text="Aplicativo", command=self.ir_para_primeira_tela)
        self.botao_ir_para_primeira_tela.grid(row=1, column=0, padx=1, pady=10, sticky='nsew')

        self.botao_ir_para_segunda_tela = tk.Button(root, text="Configuração", command=self.ir_para_segunda_tela)
        self.botao_ir_para_segunda_tela.grid(row=1, column=2, padx=5, pady=10, sticky='nsew')

        self.criar_primeira_tela()

    def criar_primeira_tela(self):
        if self.frame_atual:
            self.frame_atual.destroy()
        self.frame_atual = PrimeiraTela(self.root)

    def criar_segunda_tela(self):
        if self.frame_atual:
            self.frame_atual.destroy()
        self.frame_atual = SegundaTela(self.root)

    def ir_para_segunda_tela(self):
        self.criar_segunda_tela()

    def ir_para_primeira_tela(self):
        self.criar_primeira_tela()


if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicativo(root)
    root.mainloop()
