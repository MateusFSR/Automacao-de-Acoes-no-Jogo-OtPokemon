import tkinter as tk
from threading import Thread
import pyautogui as pa
import time
from pynput.keyboard import Listener
from HandlerPoke import HandlerPoke
import threading

battle_region = (1245, 366, 192, 188)
battle_position = (1262, 482)
poke_list_attack = ('f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8')
handler_poke = HandlerPoke()

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

class PrimeiraTela(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack()
        self.criar_widgets()

    def criar_widgets(self):
        label = tk.Label(self, text="Você está na Primeira Tela", font=("Helvetica", 16))
        label.pack()

        # Adicione widgets específicos para a primeira tela aqui
        caminho_icone = 'C:/Users/Mateus/Desktop/Programação/Battle_BOT/pokeball.ico'
        self.master.iconbitmap(caminho_icone)

        # Configuração para manter a janela no topo
        self.master.attributes('-topmost', True)

        frame_verificar = tk.Frame(self)
        frame_verificar.pack(side=tk.LEFT, padx=10)

        self.start_verificar_button = tk.Button(frame_verificar, text="Iniciar AutoBattle", command=self.iniciar_verificar, font=('Verdana', 8))
        self.start_verificar_button.pack(pady=5)

        self.stop_verificar_button = tk.Button(frame_verificar, text="Parar AutoBattle", command=self.parar_verificar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_verificar_button.pack(pady=5)

        frame_capturar = tk.Frame(self)
        frame_capturar.pack(side=tk.LEFT, padx=10)

        self.start_capturar_button = tk.Button(frame_capturar, text="Iniciar AutoCatch", command=self.iniciar_capturar, font=('Verdana', 8))
        self.start_capturar_button.pack(pady=5)

        self.stop_capturar_button = tk.Button(frame_capturar, text="Parar AutoCatch", command=self.parar_capturar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_capturar_button.pack(pady=5)

        self.running_capturar = False
        self.running_verificar = False

    def capturar_pokemon(self):
        while self.running_capturar:
            try:
                # Tente localizar a imagem na região especificada
                capturar = pa.locateOnScreen('capturar1.png', confidence=0.8)
                
                if capturar is not None:
                    print("Pokemon Encontrado")
                    pa.press('j')
                    pa.moveTo(capturar)
                    pa.sleep(0.4)
                    pa.click(capturar, button='left')
                    
                    # Aguarde um intervalo antes de verificar novamente
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

    def iniciar_capturar(self):
        self.start_capturar_button.config(state=tk.DISABLED)
        self.stop_capturar_button.config(state=tk.NORMAL)
        self.running_capturar = True

        # Inicia uma thread para capturar pokemon
        self.thread_capturar = Thread(target=self.capturar_pokemon)
        self.thread_capturar.start()

    def parar_capturar(self):
        self.start_capturar_button.config(state=tk.NORMAL)
        self.stop_capturar_button.config(state=tk.DISABLED)
        self.running_capturar = False

        # Para a thread de capturar pokemon
        self.thread_capturar.join()

    def iniciar_verificar(self):
        self.start_verificar_button.config(state=tk.DISABLED)
        self.stop_verificar_button.config(state=tk.NORMAL)
        self.running_verificar = True

        # Inicia uma thread para verificar mudança de imagem
        self.thread_verificar = Thread(target=self.verificar_mudanca_imagem)
        self.thread_verificar.start()

    def parar_verificar(self):
        self.start_verificar_button.config(state=tk.NORMAL)
        self.stop_verificar_button.config(state=tk.DISABLED)
        self.running_verificar = False

        # Para a thread de verificar mudança de imagem
        self.thread_verificar.join()


class SegundaTela(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack()
        self.criar_widgets()

    def criar_widgets(self):
        label = tk.Label(self, text="Você está na Segunda Tela", font=("Helvetica", 16))
        label.pack()

        # Adicione widgets específicos para a segunda tela aqui


class Aplicativo:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Bot")
        self.frame_atual = None

        # Botão para ir para a primeira tela
        self.botao_ir_para_primeira_tela = tk.Button(root, text="Ir para Primeira Tela", command=self.ir_para_primeira_tela)
        self.botao_ir_para_primeira_tela.pack(side=tk.LEFT, padx=10, pady=20)

        # Botão para ir para a segunda tela
        self.botao_ir_para_segunda_tela = tk.Button(root, text="Ir para Segunda Tela", command=self.ir_para_segunda_tela)
        self.botao_ir_para_segunda_tela.pack(side=tk.LEFT, padx=10, pady=20)

        # Inicializa a primeira tela
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
