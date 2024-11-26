import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

# Variáveis globais
indice_palavra = 0
em_execucao = False
palavras = []
intervalo = 500  # Intervalo inicial em milissegundos (1 segundo)

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

# Função para atualizar a label com a próxima palavra
def atualizar_label():
    global indice_palavra, em_execucao
    if em_execucao and indice_palavra < len(palavras):
        label.config(text=palavras[indice_palavra])
        indice_palavra += 1
        janela.after(intervalo, atualizar_label)  # Chama a função novamente após o intervalo

# Função para iniciar a exibição
def iniciar():
    global em_execucao
    if palavras:  # Verifica se há palavras para exibir
        if not em_execucao:
            em_execucao = True
            atualizar_label()
    else:
        messagebox.showwarning("Atenção", "Carregue um arquivo de texto ou insira o texto manualmente.")

# Função para pausar a exibição
def pausar():
    global em_execucao
    em_execucao = False

# Função para reiniciar a exibição
def reiniciar():
    global indice_palavra, em_execucao
    indice_palavra = 0
    em_execucao = False
    label.config(text="")  # Limpa a label

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
        messagebox.showinfo("Sucesso", "Arquivo carregado com sucesso!")

# Função para definir o texto da área de entrada manual como conteúdo a ser exibido
def definir_texto_manual():
    global palavras
    conteudo = text_input.get("1.0", tk.END).strip()  # Obtém o texto do campo e remove espaços extras
    if conteudo:
        palavras = conteudo.split()
        reiniciar()  # Reinicia a exibição para o novo conteúdo
        label_arquivo.config(text="Texto inserido manualmente")  # Atualiza o rótulo do arquivo
        #messagebox.showinfo("Sucesso", "Texto inserido com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Por favor, insira algum texto no campo.")

# Função para ajustar o intervalo com base na PPM e salvar a configuração
def ajustar_intervalo(ppm=None):
    global intervalo
    try:
        ppm = int(entry_ppm.get()) if ppm is None else ppm
        intervalo = int(60000 / ppm)  # Converte PPM para intervalo em milissegundos
        salvar_config(ppm)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para PPM.")

# Função para limpar o campo de entrada de texto manual
def limpar_texto():
    text_input.delete("1.0", tk.END)
    label_arquivo.config(text="Arquivo: Nenhum arquivo carregado")

# Configuração da janela
janela = tk.Tk()
janela.title("Iterador de Palavras")
janela.geometry("1000x800")  # Aumenta o tamanho da janela
#janela.resizable(False, False)  # Impede redimensionamento

# Inicialização dos elementos
label = tk.Label(janela, text="", font=("Arial", 48), pady=20)  # Aumenta a fonte e espaçamento
label.pack(pady=30)

# Frame para configuração de PPM e botões de controle
frame_controle = tk.Frame(janela)
frame_controle.pack(pady=10)

# Campo para definir a PPM
frame_ppm = tk.Frame(frame_controle)
frame_ppm.pack(side="left", padx=(0, 20))  # Adiciona espaçamento à direita
tk.Label(frame_ppm, text="Velocidade (PPM):", font=("Arial", 14)).pack(side="left")
entry_ppm = tk.Entry(frame_ppm, width=5, font=("Arial", 14))
entry_ppm.pack(side="left", padx=5)
botao_definir_ppm = tk.Button(frame_ppm, text="Definir", command=ajustar_intervalo)
botao_definir_ppm.pack(side="left")

# Carrega o valor de PPM salvo no arquivo de configuração
carregar_config()

# Botão para carregar o arquivo
botao_carregar = tk.Button(frame_controle, text="Carregar Arquivo", command=carregar_arquivo, font=("Arial", 12))
botao_carregar.pack(side="left", padx=(0, 20))  # Adiciona espaçamento à direita

# Label para exibir o nome do arquivo selecionado
label_arquivo = tk.Label(janela, text="Arquivo: Nenhum arquivo carregado", font=("Arial", 12))
label_arquivo.pack()

# Área de entrada de texto manual
tk.Label(janela, text="Ou insira o texto abaixo:", font=("Arial", 12)).pack(pady=10)
text_input = tk.Text(janela, height=8, width=60, font=("Arial", 12))
text_input.pack(pady=5)

# Botões para definir e limpar o texto
botao_definir_texto = tk.Button(janela, text="Usar Texto Inserido", command=definir_texto_manual, font=("Arial", 12))
botao_definir_texto.pack(pady=5)
botao_limpar_texto = tk.Button(janela, text="Limpar Texto", command=limpar_texto, font=("Arial", 12))
botao_limpar_texto.pack(pady=5)

# Frame para os botões de controle
frame_botoes = tk.Frame(frame_controle)
frame_botoes.pack(side="right")

# Botões de controle
botao_iniciar = tk.Button(frame_botoes, text="Iniciar", command=iniciar, font=("Arial", 12))
botao_iniciar.pack(pady=5)

botao_pausar = tk.Button(frame_botoes, text="Pausar", command=pausar, font=("Arial", 12))
botao_pausar.pack(pady=5)

botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", command=reiniciar, font=("Arial", 12))
botao_reiniciar.pack(pady=5)

# Loop principal da janela
janela.mainloop()
