import tkinter as tk
from tkinter import filedialog, messagebox
import json, os, keyboard, time
from screeninfo import get_monitors

# Variáveis globais
indice_palavra = 0
em_execucao = False
palavras = []
intervalo = 1000  # Intervalo inicial em milissegundos (1 segundo)
texto = ""  # Texto a ser exibido

# Caminho do arquivo de configuração
config_file = "config.json"

# Carrega a configuração de PPM do arquivo JSON
def carregar_config():
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
            ppm = config.get("ppm", 60)
            entry_ppm.insert(0, str(ppm))
            ajustar_intervalo(ppm)  # Ajusta o intervalo inicial com o valor carregado
    else:
        entry_ppm.insert(0, "60")  # Valor padrão

# Salva a configuração de PPM em um arquivo JSON
def salvar_config(ppm):
    config = {"ppm": ppm}
    with open(config_file, "w") as f:
        json.dump(config, f)

# Função para criar a segunda janela e exibir o texto iterado
def criar_segunda_janela():
    monitores = get_monitors()  # Obtém a lista de monitores conectados
    if len(monitores) > 1:
        print("Múltiplos monitores detectados. Criando segunda janela.")
        global segunda_janela, label_segunda_janela
        segunda_janela = tk.Toplevel(janela)
        segunda_janela.title("Exibição do Texto")
        segunda_janela.configure(bg="black")  # Fundo preto
        segunda_janela.geometry("1920x1080+1920+0")  # Define tamanho e posição
        segunda_janela.resizable(True, True)  # Permite redimensionamento

        # Label para exibir o texto
        label_segunda_janela = tk.Label(
            segunda_janela,
            text="", 
            font=("Arial", 62), 
            bg="black",  # Fundo preto
            fg="white",  # Texto branco
            anchor="center"
        )
        label_segunda_janela.pack(expand=True, fill="both")  # Centraliza e preenche a janela
    else:
        print("Apenas um monitor detectado. A segunda janela não será criada.")

# Atualiza o texto na segunda janela
def atualizar_label():
    ajustar_intervalo()  # Ajusta o intervalo com base na PPM
    global indice_palavra, em_execucao, texto
    # Verifica se a execução está ativa e se ainda há palavras para exibir
    if em_execucao and indice_palavra < len(palavras):
        texto = palavras[indice_palavra]
        indice_palavra += 1  # Avança para a próxima palavra

        # Atualiza as labels na janela principal e na segunda janela
        label.config(text=texto)
        # Se houver a segunda janela, atualiza o texto dela também
        if 'segunda_janela' in globals() and segunda_janela.winfo_exists():
            # Atualiza o texto na segunda janela
            label_segunda_janela.config(text=texto)

        # Se houver uma vírgula na palavra, atrasa 150%
        if "," in texto:
            janela.after(int(intervalo * 1.5), atualizar_label)
        # Se houver um ponto na palavra, atrasa 200%
        elif "." in texto:
            janela.after(int(intervalo * 2), atualizar_label)
        # Se houver um ponto de interrogação na palavra, atrasa 120%
        elif "?" in texto:
        # Se houver uma queba de linha, atrasa 220%
            janela.after(int(intervalo * 2.2), atualizar_label)
        # Se houver uma quebra de linha, atrasa 350%
        elif "\n" in texto:
            janela.after(int(intervalo * 2.5), atualizar_label)
        # Se for uma palavra regular, executa imediatamente
        else:
            janela.after(intervalo, atualizar_label)

    elif indice_palavra >= len(palavras):
        # Se não houver mais palavras, reinicia a exibição
        reiniciar()

# Função para iniciar a exibição
def iniciar():
    global em_execucao, palavras
    if not em_execucao: # Verifica se a execução não está ativa
        # Obtém o texto do campo de entrada manual, se houver
        conteudo = text_input.get("1.0", tk.END).strip()
        botao_iniciar.config(text="Pausar")  # Atualiza o texto do botão Iniciar para "Pausar"
        botao_iniciar.update()  # Atualiza o botão imediatamente
        
        if conteudo:
            palavras = conteudo.split()  # Divide o texto em palavras
            # reiniciar()  # Reinicia a exibição para o novo conteúdo
            label_arquivo.config(text="Texto inserido manualmente")  # Atualiza o rótulo do arquivo
        elif not palavras:
            pergunta = messagebox.askyesno("Atenção", "Deseja colar o conteúdo da área de transferência?")
            if pergunta:
                colar_texto()
                time.sleep(0.5) 
                iniciar()
            return

        # Inicia a exibição do texto
        if palavras:
            em_execucao = True
            atualizar_label()
    else: # A execução já está ativa
        # O botão se transforma em "Pausar" e a execução é pausada
        em_execucao = False
        botao_iniciar.config(text="Iniciar")
        botao_iniciar.update()
    
# Função para reiniciar a exibição
def reiniciar():
    global texto, indice_palavra, em_execucao
    indice_palavra = 0
    em_execucao = False
    texto = ""  # Limpa o texto
    label.config(text="")  # Limpa a label
    if segunda_janela.winfo_exists():
        # Se a segunda janela existir, limpa o texto dela também
        label_segunda_janela.config(text="")  # Limpa a label da segunda janela
    botao_iniciar.config(text="Iniciar")  # Atualiza o texto do botão para "Iniciar"
    botao_iniciar.update()  # Atualiza o botão imediatamente

# Função para carregar o arquivo .txt
def carregar_arquivo():
    global palavras
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, "r", encoding="utf-8") as file:
            conteudo = file.read()
            palavras = conteudo.split()  # Divide o conteúdo em palavras
            reiniciar()  # Reinicia a exibição para o novo conteúdo
        # Exibe o nome do arquivo selecionado
        nome_arquivo = filepath.split("/")[-1]
        label_arquivo.config(text=f"Arquivo: {nome_arquivo}")
        text_input.delete("1.0", tk.END)  # Limpa o campo de texto manual
        text_input.insert("1.0", conteudo)  # Insere o conteúdo do arquivo no campo de texto manual
        messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")

# Função para definir o texto da área de entrada manual como conteúdo a ser exibido
def definir_texto_manual():
    global palavras
    conteudo = text_input.get("1.0", tk.END).strip()  # Obtém o texto do campo e remove espaços extras
    if conteudo:
        palavras = conteudo.split()
        reiniciar()  # Reinicia a exibição para o novo conteúdo
        label_arquivo.config(text="Texto inserido manualmente")  # Atualiza o rótulo do arquivo
    else:
        messagebox.showwarning("Atenção", "Por favor, insira algum texto no campo.")

# Função para ajustar o intervalo com base na PPM e salvar a configuração
def ajustar_intervalo(ppm=None):
    global intervalo, em_execucao
    try:
        ppm = int(entry_ppm.get()) if ppm is None else ppm
        intervalo = int(60000 / ppm)  # Converte PPM para intervalo em milissegundos
        salvar_config(ppm)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para PPM.")
        # O botão Iniciar se transforma em "Pausar" e a execução é pausada
        em_execucao = False
        botao_iniciar.config(text="Iniciar")
        botao_iniciar.update()

# Acelera a velocidade em 5%
def acelerar():
    ppm = int(entry_ppm.get())
    ppm = int(ppm * 1.05)
    entry_ppm.delete(0, tk.END)
    entry_ppm.insert(0, ppm)
    ajustar_intervalo(ppm)

# Desacelera a velocidade em 5%
def desacelerar():
    ppm = int(entry_ppm.get())
    ppm = int(ppm / 1.05)
    entry_ppm.delete(0, tk.END)
    entry_ppm.insert(0, ppm)
    ajustar_intervalo(ppm)

# Função para limpar o campo de entrada de texto manual
def limpar_texto():
    text_input.delete("1.0", tk.END)
    label_arquivo.config(text="Arquivo: Nenhum arquivo carregado")
    # Limpa o texto na segunda janela, se existir
    if 'segunda_janela' in globals() and segunda_janela.winfo_exists():
        label_segunda_janela.config(text="")  # Limpa o texto na segunda janela
    # Limpa a memória de palavras
    global palavras
    palavras = []  # Limpa a lista de palavras
    reiniciar()  # Reinicia a exibição

# Função para colar texto da área de transferência no campo de entrada
def colar_texto():
    texto_copiado = janela.clipboard_get()  # Obtém o texto da área de transferência
    text_input.delete("1.0", tk.END)  # Limpa o campo de texto
    text_input.insert("1.0", texto_copiado)  # Insere o texto copiado no campo de texto
    if texto_copiado:
        label_arquivo.config(text="Texto colado da área de transferência")  # Atualiza o rótulo do arquivo


# Função para iniciar/pausar a exibição apenas se a janela estiver em foco
def iniciar_com_foco():
    if janela.focus_get():  # Verifica se a janela está em foco
        iniciar()

# Função para colar texto apenas se a janela estiver em foco
def colar_texto_com_foco():
    if janela.focus_get():  # Verifica se a janela está em foco
        colar_texto()

# Atalhos de teclado condicionados ao foco da janela
keyboard.add_hotkey("ctrl+v", colar_texto_com_foco)  # Cola o texto com Ctrl+V
keyboard.add_hotkey("space", iniciar_com_foco)  # Inicia/pausa a exibição com a barra de espaço
keyboard.add_hotkey("+", acelerar) # Acelera a velocidade em 5%
keyboard.add_hotkey("-", desacelerar) # Diminui a velocidade em 5%

# Configuração da janela principal
janela = tk.Tk()
janela.title("Iterador de Palavras")

# try:
#     janela.iconbitmap("Logo-final.ico")
# except Exception as e:
#     print(f"Erro ao carregar o ícone: {e}")

janela.geometry("580x630+150+0")  # Define tamanho e posição (0px da esquerda, 0px do topo)
janela.configure(bg="gray20")  # Define a cor de fundo para cinza escuro


# Frame para a label de exibição do texto
frame_label = tk.Frame(janela, bg="black", width=580, height=120)  # Fundo preto
frame_label.pack(pady=15, fill="both")  # Adiciona espaçamento entre a label e o topo da janela

label = tk.Label(
    frame_label, 
    text="", 
    font=("Arial", 48), 
    pady=20, 
    bg="black",  # Fundo preto
    fg="white"   # Texto branco
)
label.grid(row=0, column=0, sticky="nsew")  # Preenche todo o espaço do frame
label.pack()  # Exemplo de espaçamento vertical

# Frame para configuração de PPM e botões de controle
frame_controle = tk.Frame(janela, bg="gray20")  # Fundo cinza mais claro
frame_controle.pack(pady=5)

# Campo para definir a PPM
tk.Label(frame_controle, text="Velocidade (PPM):", font=("Arial", 14), bg="gray20", fg="white").grid(row=1,column=1, rowspan=2)
entry_ppm = tk.Entry(frame_controle, width=5, font=("Arial", 14), bg="gray20", fg="white", insertbackground="white")  # Fundo cinza escuro, texto branco
entry_ppm.grid(row=1, column=2, rowspan=2)

# Botão para acelerar ppm
botao_acelerar = tk.Button(frame_controle, text="+", command=acelerar, font=("Arial", 12), bg="gray40", fg="white", width=4)
botao_acelerar.grid(row=1, column=3, padx=8)

# Botão para desacelerar ppm
botao_desacelerar = tk.Button(frame_controle, text="-", command=desacelerar, font=("Arial", 12), bg="gray40", fg="white", width=4)
botao_desacelerar.grid(row=2, column=3, padx=8)

# Botões de controle
botao_iniciar = tk.Button(frame_controle, text="Iniciar", command=iniciar, font=("Arial", 12), bg="gray40", fg="white")
botao_iniciar.grid(row=1, column=4, padx=5)

botao_reiniciar = tk.Button(frame_controle, text="Reiniciar", command=reiniciar, font=("Arial", 12), bg="gray40", fg="white")
botao_reiniciar.grid(row=2, column=4,  padx=5, pady=5)

# Carrega o valor de PPM salvo no arquivo de configuração
carregar_config()
criar_segunda_janela()  # Cria a segunda janela ao iniciar

# Label para exibir o nome do arquivo selecionado
label_arquivo = tk.Label(janela, text="Arquivo: Nenhum arquivo carregado", font=("Arial", 12), bg="gray20", fg="white")
label_arquivo.pack(pady=5)

# Área de entrada de texto manual
text_input = tk.Text(janela, height=8, width=60, font=("Arial", 12), bg="gray40", fg="white", insertbackground="white")
text_input.pack(pady=5)

# Botão para carregar o arquivo
botao_carregar = tk.Button(janela, text="Carregar Arquivo", command=carregar_arquivo, font=("Arial", 12), bg="gray40", fg="white")
botao_carregar.pack(pady=5)

# Botões para colar e limpar texto
botao_colar_texto = tk.Button(janela, text="Colar Texto", command=colar_texto, font=("Arial", 12), bg="gray40", fg="white")
botao_colar_texto.pack(pady=5)

botao_limpar_texto = tk.Button(janela, text="Limpar Texto", command=limpar_texto, font=("Arial", 12), bg="gray40", fg="white")
botao_limpar_texto.pack(pady=5)

# Loop principal da janela
janela.mainloop()
