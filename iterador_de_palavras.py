import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os

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
    global segunda_janela, label_segunda_janela
    segunda_janela = tk.Toplevel(janela)
    segunda_janela.title("Exibição do Texto")
    segunda_janela.configure(bg="black")  # Fundo preto
    segunda_janela.geometry("1910x1080+1920+0")  # Define tamanho e posição (900px da esquerda, alinhado ao topo da janela principal)
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

# Atualiza o texto na segunda janela
def atualizar_label():
    global indice_palavra, em_execucao, texto
    # Verifica se a execução está ativa e se ainda há palavras para exibir
    if em_execucao and indice_palavra < len(palavras):
        texto = palavras[indice_palavra]
        indice_palavra += 1  # Avança para a próxima palavra

        # Atualiza as labels na janela principal e na segunda janela
        label.config(text=texto)
        label_segunda_janela.config(text=texto)

        # Chama a função novamente após o intervalo
        janela.after(intervalo, atualizar_label)

# Função para iniciar a exibição (agora inclui a funcionalidade de "Usar Texto Inserido")
def iniciar():
    global em_execucao, palavras
    # Obtém o texto do campo de entrada manual, se houver
    conteudo = text_input.get("1.0", tk.END).strip()
    if conteudo:
        palavras = conteudo.split()  # Divide o texto em palavras
        reiniciar()  # Reinicia a exibição para o novo conteúdo
        label_arquivo.config(text="Texto inserido manualmente")  # Atualiza o rótulo do arquivo
    elif not palavras:
        messagebox.showwarning("Atenção", "Carregue um arquivo de texto ou insira o texto manualmente.")
        return

    # Inicia a exibição do texto
    if palavras and not em_execucao:
        em_execucao = True
        atualizar_label()

# Função para pausar a exibição
def pausar():
    global em_execucao
    em_execucao = False

# Função para reiniciar a exibição
def reiniciar():
    global texto, indice_palavra, em_execucao
    indice_palavra = 0
    em_execucao = False
    label.config(text="")  # Limpa a label
    texto = ""  # Limpa o texto
    label_segunda_janela.config(text="")  # Limpa a label da segunda janela

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

# Função para colar texto da área de transferência no campo de entrada
def colar_texto():
    texto_copiado = janela.clipboard_get()  # Obtém o texto da área de transferência
    text_input.delete("1.0", tk.END)  # Limpa o campo de texto
    text_input.insert("1.0", texto_copiado)  # Insere o texto copiado no campo de texto

# Configuração da janela principal
janela = tk.Tk()
janela.title("Iterador de Palavras")
try:
    janela.iconbitmap("Logo-final.ico")
except Exception as e:
    print(f"Erro ao carregar o ícone: {e}")
janela.geometry("580x650+-1286+250")  # Define tamanho e posição (0px da esquerda, 0px do topo)
janela.configure(bg="gray20")  # Define a cor de fundo para cinza escuro

# Inicialização dos elementos
label = tk.Label(
    janela, 
    text="", 
    font=("Arial", 48), 
    pady=20, 
    bg="black",  # Fundo preto
    fg="white"   # Texto branco
)
label.pack(pady=30)

# Frame para configuração de PPM e botões de controle
frame_controle = tk.Frame(janela, bg="gray30")  # Fundo cinza mais claro
frame_controle.pack(pady=10)

# Campo para definir a PPM
frame_ppm = tk.Frame(frame_controle, bg="gray30")  # Fundo cinza mais claro
frame_ppm.pack(side="left", padx=(0, 20))  # Adiciona espaçamento à direita
tk.Label(frame_ppm, text="Velocidade (PPM):", font=("Arial", 14), bg="gray30", fg="white").pack(side="left")
entry_ppm = tk.Entry(frame_ppm, width=5, font=("Arial", 14), bg="gray40", fg="white", insertbackground="white")  # Fundo cinza escuro, texto branco
entry_ppm.pack(side="left", padx=5)
botao_definir_ppm = tk.Button(frame_ppm, text="Definir", command=ajustar_intervalo, font=("Arial", 12), bg="gray40", fg="white")
botao_definir_ppm.pack(side="left")

# Carrega o valor de PPM salvo no arquivo de configuração
carregar_config()
criar_segunda_janela()  # Cria a segunda janela ao iniciar

# Botão para carregar o arquivo
botao_carregar = tk.Button(frame_controle, text="Carregar Arquivo", command=carregar_arquivo, font=("Arial", 12), bg="gray40", fg="white")
botao_carregar.pack(side="left", padx=(0, 20))  # Adiciona espaçamento à direita

# Label para exibir o nome do arquivo selecionado
label_arquivo = tk.Label(janela, text="Arquivo: Nenhum arquivo carregado", font=("Arial", 12), bg="gray30", fg="white")
label_arquivo.pack()

# Área de entrada de texto manual
tk.Label(janela, text="Ou insira o texto abaixo:", font=("Arial", 12), bg="gray30", fg="white").pack(pady=10)
text_input = tk.Text(janela, height=8, width=60, font=("Arial", 12), bg="gray40", fg="white", insertbackground="white")
text_input.pack(pady=5)

# Botões para colar e limpar texto
botao_colar_texto = tk.Button(janela, text="Colar Texto", command=colar_texto, font=("Arial", 12), bg="gray40", fg="white")
botao_colar_texto.pack(pady=5)

botao_limpar_texto = tk.Button(janela, text="Limpar Texto", command=limpar_texto, font=("Arial", 12), bg="gray40", fg="white")
botao_limpar_texto.pack(pady=5)

# Frame para os botões de controle
frame_botoes = tk.Frame(frame_controle, bg="gray30")  # Fundo cinza mais claro
frame_botoes.pack(side="right")

# Botões de controle
botao_iniciar = tk.Button(frame_botoes, text="Iniciar", command=iniciar, font=("Arial", 12), bg="gray40", fg="white")
botao_iniciar.pack(pady=5)

botao_pausar = tk.Button(frame_botoes, text="Pausar", command=pausar, font=("Arial", 12), bg="gray40", fg="white")
botao_pausar.pack(pady=5)

botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", command=reiniciar, font=("Arial", 12), bg="gray40", fg="white")
botao_reiniciar.pack(pady=5)

# Loop principal da janela
janela.mainloop()
