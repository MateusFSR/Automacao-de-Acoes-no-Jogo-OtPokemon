class PokemonBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pokemon Bot")
        largura_janela = 350
        altura_janela = 120
        self.root.geometry(f"{largura_janela}x{altura_janela}")

        # Configuração para manter a janela no topo
        self.root.attributes('-topmost', True)           

        # Frame para os botões AutoBattle
        frame_verificar = tk.Frame(root)
        frame_verificar.grid(row=0, column=0, padx=8, pady=10, sticky='nsew')
        
        self.status_label = tk.Label(frame_verificar, text="Auto Battle", font=('Verdana', 8))
        self.status_label.grid(row=0, column=0, pady=5)

        self.start_verificar_button = tk.Button(frame_verificar, text="Iniciar", command=self.iniciar_verificar, font=('Verdana', 8))
        self.start_verificar_button.grid(row=1, column=0, pady=5)

        self.stop_verificar_button = tk.Button(frame_verificar, text="Parar", command=self.parar_verificar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_verificar_button.grid(row=2, column=0, pady=5)

        # Frame para os botões AutoCatch
        frame_capturar = tk.Frame(root)
        frame_capturar.grid(row=0, column=1, padx=8, pady=10, sticky='nsew')
        
        self.status_label = tk.Label(frame_capturar, text="Auto Captura", font=('Verdana', 8))
        self.status_label.grid(row=0, column=0, pady=5)

        self.start_capturar_button = tk.Button(frame_capturar, text="Iniciar", command=self.iniciar_capturar, font=('Verdana', 8))
        self.start_capturar_button.grid(row=1, column=0, pady=5)

        self.stop_capturar_button = tk.Button(frame_capturar, text="Parar", command=self.parar_capturar, state=tk.DISABLED, font=('Verdana', 8))
        self.stop_capturar_button.grid(row=2, column=0, pady=5)

        # Frame para configuraçoes
        frame_config = tk.Frame(root)
        frame_config.grid(row=0, column=2, padx=10, pady=10, sticky='nsew')

        self.status_label = tk.Label(frame_config, text="Configurações", font=('Verdana', 8))
        self.status_label.grid(row=0, column=0, pady=5)

        self.dummy_button = tk.Button(frame_config, text="Posicao Batalha (H)", font=('Verdana', 8), pady=1, padx=7, command=self.capturar_battle)
        self.dummy_button.grid(row=1, column=0, pady=5)  
        
        self.dummy_button = tk.Button(frame_config, text="Posicao Pokemon (H)", font=('Verdana', 8), pady=1, command=self.capturar_posicao)
        self.dummy_button.grid(row=2, column=0, pady=5)
      

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
                battle = pa.locateOnScreen('battle.png', confidence=0.8, region=self.capturar_tela)
                if battle is not None:
                        print("Sem Pokemons para batalha")
                        time.sleep(0.5)
                else:
                    print("Pokemon Encontrado")
                    pa.click(self.battle_position, button='left')
                    pa.sleep(0.2)
                    pa.press(poke_list_attack, interval=0.1)
                    pa.sleep(0.3)
                    pa.sleep(0.7)
                    pa.click(self.battle_position, button='left')
                    pa.sleep(0.2)
                    pa.press(poke_list_attack, interval=0.1)
                    pa.sleep(0.5)
                    time.sleep(0.5)
            except pa.ImageNotFoundException:
                print("Pokemon Encontrado")
                pa.click(self.battle_position, button='left')
                pa.sleep(0.2)
                pa.press(poke_list_attack, interval=0.1)
                pa.sleep(0.3)
                pa.sleep(0.7)
                pa.click(self.battle_position, button='left')
                pa.sleep(0.2)
                pa.press(poke_list_attack, interval=0.1)
                pa.sleep(0.5)
                time.sleep(0.5)


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

    def capturar_posicao(self):
        keyboard.wait('h')
        self.bposicao = pa.position()
        x = self.bposicao.x
        y = self.bposicao.y
        self.battle_position = (x, y)
        print(self.battle_position)

    def capturar_battle(self):
        keyboard.wait('h')
        self.btela = pa.locateOnScreen('battle.png', confidence=0.7)
        self.left = self.btela.left
        self.top = self.btela.top
        self.width = self.btela.width
        self.height = self.btela.height
        self.capturar_tela = (self.left, self.top, self.width, self.height)
        print(self.capturar_tela)

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonBotApp(root)
    root.mainloop()
