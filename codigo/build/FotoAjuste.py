from pathlib import Path
from tkinter import *
from tkinter import Tk, Canvas, Button, PhotoImage, filedialog, Scale
from PIL import Image, ImageTk
import os
import tkinter as tk
import threading
import json




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame1"
CONFIG_FILE = OUTPUT_PATH / "config.json"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.overrideredirect(True)
window_width = 706
window_height = 765

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
window.configure(bg="#F4F4F4")

canvas = Canvas(
    window,
    bg="#F4F4F4",
    height=765,
    width=706,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

is_dragging = False
start_x = 0
start_y = 0

def on_button_press(event):
    global is_dragging, start_x, start_y
    is_dragging = True
    start_x = event.x
    start_y = event.y

def on_mouse_drag(event):
    if is_dragging:
        x = window.winfo_x() - start_x + event.x
        y = window.winfo_y() - start_y + event.y
        window.geometry(f"+{x}+{y}")

def on_button_release(event):
    global is_dragging
    is_dragging = False


var_condicao = 0
marca_dagua = None


def salvar_caminho_marca_dagua(caminho_arquivo):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump({'marca_dagua': caminho_arquivo}, config_file)


def carregar_marca_dagua_salva():
    global marca_dagua
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
            caminho_arquivo = config.get('marca_dagua')
            if caminho_arquivo and os.path.exists(caminho_arquivo):
                imagem = Image.open(caminho_arquivo)
                
                largura_maxima = 300
                altura_maxima = 166
                
                largura_original, altura_original = imagem.size
                
                proporcao = min(largura_maxima / largura_original, altura_maxima / altura_original)
                
                nova_largura = int(largura_original * proporcao)
                nova_altura = int(altura_original * proporcao)
                
                imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
                imagem_tk = ImageTk.PhotoImage(imagem)

                posicao_x = (largura_maxima - nova_largura) // 2 + 53
                posicao_y = (altura_maxima - nova_altura) // 2 + 185

                canvas.create_image(posicao_x, posicao_y, anchor="nw", image=imagem_tk)

                canvas.image = imagem_tk
            
                marca_dagua = imagem



def carregar_marca_dagua():
    global marca_dagua
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos PNG", "*.png")])
    if caminho_arquivo:
        salvar_caminho_marca_dagua(caminho_arquivo)
        imagem = Image.open(caminho_arquivo)
        
        largura_maxima = 300
        altura_maxima = 166
        
        largura_original, altura_original = imagem.size
        
        proporcao = min(largura_maxima / largura_original, altura_maxima / altura_original)

        nova_largura = int(largura_original * proporcao)
        nova_altura = int(altura_original * proporcao)
        
        imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)

        posicao_x = (largura_maxima - nova_largura) // 2 + 53 
        posicao_y = (altura_maxima - nova_altura) // 2 + 185 

        canvas.create_image(posicao_x, posicao_y, anchor="nw", image=imagem_tk)

        canvas.image = imagem_tk
        
        marca_dagua = imagem




#função para abrir o explorador de arquivos e carregar múltiplas imagens
def carregar_fotos():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("All files", ".jpg"), ("All files", ".png")])
    entry_2.config(state=NORMAL)
    entry_2.delete("1.0", "end")
    if file_paths:
        canvas.delete("photo_names")
        y = 440
        for file_path in file_paths:
            photo_name = Path(file_path).name
            entry_2.insert("end", f"{photo_name}\n")
            y += 20
        entry_2.config(state=DISABLED)



def abrir_aviso(mensagem_de_erro):
    msg_erro = mensagem_de_erro

    aviso = tk.Toplevel()
    aviso.title("Aviso")
    aviso.geometry("300x150")
    
    largura = 300
    altura = 150
    x = (aviso.winfo_screenwidth() // 2) - (largura // 2)
    y = (aviso.winfo_screenheight() // 2) - (altura // 2)
    aviso.geometry(f"{largura}x{altura}+{x}+{y}")

    mensagem = tk.Label(aviso, text=msg_erro, font=("Poppins Medium", 10))
    mensagem.pack(pady=20)
    aviso.grab_set()
    '''
    # Adiciona um botão para fechar a janela de aviso
    botao_fechar = tk.Button(aviso, text="Fechar", command=aviso.destroy)
    botao_fechar.pack(pady=10)
    '''

def mostrar_na_pasta():
    janela_processamento.destroy()
    if os.name == 'nt':  # para Windows
        os.startfile(pasta_destino)
    elif os.name == 'posix':  # para macOS ou Linux
        os.system(f'open "{pasta_destino}"')
    else:
        tk.messagebox.showerror("Erro", "Sistema operacional não suportado.")


def mostrar_janela_processamento(status):
    global janela_processamento
    janela_processamento = tk.Toplevel(window)
    janela_processamento.title("Processamento")
    janela_processamento.geometry("300x150")

    largura = 300
    altura = 150
    x = (janela_processamento.winfo_screenwidth() // 2) - (largura // 2)
    y = (janela_processamento.winfo_screenheight() // 2) - (altura // 2)
    janela_processamento.geometry(f"{largura}x{altura}+{x}+{y}")

    janela_processamento.label = tk.Label(
        janela_processamento,
        text=status,
        font=("Poppins Medium", 12)
    )
    
    janela_processamento.label.pack(expand=True)
    janela_processamento.grab_set()


def atualizar_janela_processamento(status):
    janela_processamento.label.config(text=status)
    janela_processamento.update()
    janela_processamento.grab_set()

def processar_imagens():
    global var_condicao
    global pasta_destino
    var_condicao = 0
    if not file_paths:
        print("Nenhuma imagem selecionada.")
        mensagem_erro = "Nenhuma imagem selecionada."
        abrir_aviso(mensagem_erro)
        return

    porcentagem = valor_slider()
    
    if porcentagem == 0:
        print("Porcentagem selecionada é 0%. Nenhuma imagem será reduzida.")
        mensagem_erro = "Porcentagem selecionada é 0%.\nNenhuma imagem será reduzida."
        abrir_aviso(mensagem_erro)
        return
    
    if marca_dagua is None:
        print("Nenhuma marca d'água carregada.")
        mensagem_erro = "Nenhuma marca d'água carregada."
        abrir_aviso(mensagem_erro)
        return
    
    pasta_destino = escolher_pasta_destino()

    def funcionar():
        global var_condicao
        if pasta_destino:
            window.after(0, lambda: mostrar_janela_processamento("Processando, aguarde..."))
            for caminho_imagem in file_paths:
                aplicar_marca_dagua(caminho_imagem, marca_dagua, porcentagem, pasta_destino)
            var_condicao = 1
            print(f"Imagens salvas em: {pasta_destino}")

    def monitorar_processamento():

        if 'janela_processamento' in globals():
            if var_condicao == 1:
                atualizar_janela_processamento("Processamento concluído.")
                
                mostrar_fechar = tk.Button(janela_processamento, text="Fechar", command=janela_processamento.destroy)
                mostrar_fechar.pack(pady=7)
                mostrar_na_pasta_botao = tk.Button(janela_processamento, text="Mostrar na pasta", command=mostrar_na_pasta)
                mostrar_na_pasta_botao.pack(pady=10)
            else:
                janela_processamento.after(100, monitorar_processamento)
        else:
            window.after(100, monitorar_processamento)


    def iniciar_processamento():
        thread = threading.Thread(target=funcionar)
        thread.start()
        monitorar_processamento()

    iniciar_processamento()










def aplicar_marca_dagua(caminho_imagem, marca_dagua, porcentagem, pasta_destino):
    # Carregar a imagem original
    imagem = Image.open(caminho_imagem)
    
    # Reduzir a imagem
    largura_original, altura_original = imagem.size
    nova_largura = int(largura_original * (porcentagem / 100))
    nova_altura = int(altura_original * (porcentagem / 100))
    imagem = imagem.resize((nova_largura, nova_altura), Image.LANCZOS)

    # Redimensionar a marca d'água proporcionalmente
    largura_marca, altura_marca = marca_dagua.size
    if largura_original > altura_original:  # Imagem horizontal
        proporcao = min(nova_largura * 0.12 / largura_marca, nova_altura * 0.12 / altura_marca)  # 12% do tamanho da imagem
    else:  # Imagem vertical
        proporcao = min(nova_largura * 0.18 / largura_marca, nova_altura * 0.18 / altura_marca)  # 18% do tamanho da imagem
    nova_largura_marca = int(largura_marca * proporcao)
    nova_altura_marca = int(altura_marca * proporcao)
    marca_dagua_redimensionada = marca_dagua.resize((nova_largura_marca, nova_altura_marca), Image.LANCZOS)

    # Calcular a margem proporcional
    margem_proporcional = 0.02  # 2% da largura da imagem
    margem_x = int(nova_largura * margem_proporcional)
    margem_y = int(nova_altura * margem_proporcional)

    # Calcular a posição da marca d'água (canto inferior direito com margem proporcional)
    posicao_x = nova_largura - nova_largura_marca - margem_x
    posicao_y = nova_altura - nova_altura_marca - margem_y

    # Aplicar a marca d'água na imagem
    imagem.paste(marca_dagua_redimensionada, (posicao_x, posicao_y), marca_dagua_redimensionada)

    # Salvar a imagem com a marca d'água
    nome_imagem = os.path.basename(caminho_imagem)
    nome_base, extensao = os.path.splitext(nome_imagem)  # Separar nome e extensão
    caminho_salvo = os.path.join(pasta_destino, nome_imagem)

    # Verificar se o arquivo já existe e renomear se necessário
    contador = 1
    while os.path.exists(caminho_salvo):
        caminho_salvo = os.path.join(pasta_destino, f"{nome_base} ({contador}){extensao}")
        contador += 1

    # Salvar a imagem com o nome único
    imagem.save(caminho_salvo)


# retangulo superior que movimenta a pagina
canvas.place(x=0, y=0)
movable_rectangle = canvas.create_rectangle(
    0.0,
    0.0,
    706.0,
    110.0,
    fill="#588FAE",
    outline=""
)

# Conectar os eventos de mouse ao retângulo específico
canvas.tag_bind(movable_rectangle, "<ButtonPress-1>", on_button_press)
canvas.tag_bind(movable_rectangle, "<B1-Motion>", on_mouse_drag)
canvas.tag_bind(movable_rectangle, "<ButtonRelease-1>", on_button_release)

canvas.create_text(
    30.0,
    26.0,
    anchor="nw",
    text="FotoAjuste",
    fill="#FFFFFF",
    font=("Poppins Bold", 40 * -1)
)

canvas.create_rectangle(
    53.0,
    185.0,
    353.0,
    351.0,
    fill="#D9D9D9",
    outline=""
)

canvas.create_rectangle(
    29.0,
    163.0,
    30.0,
    388.0,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    670.0,
    164.0,
    671.0,
    389.0,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    28.99993896484375,
    387.0,
    671.0,
    388.0000000000001,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    28.99993896484375,
    163.0,
    672.0,
    164.00366083189755,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    29.0,
    418.0,
    30.0,
    642.0,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    670.0,
    419.0,
    671.0,
    643.0,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    28.99993896484375,
    641.0,
    671.0,
    642.0036608321468,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    28.99993896484375,
    418.0,
    672.0,
    419.0036608318975,
    fill="#598FAE",
    outline=""
)

canvas.create_text(
    375.0,
    237.0,
    anchor="nw",
    text="selecione sua marca d'água",
    fill="#1B597D",
    font=("Poppins Bold", 18 * -1)
)

canvas.create_text(
    375.0,
    492.0,
    anchor="nw",
    text="selecione suas fotos",
    fill="#1B597D",
    font=("Poppins Bold", 18 * -1)
)

canvas.create_text(
    375.0,
    257.0,
    anchor="nw",
    text="formato: png",
    fill="#1C5A7D",
    font=("Poppins Light", 12 * -1)
)

canvas.create_text(
    282.0,
    715.0,
    anchor="nw",
    text="powered by ",
    fill="#000000",
    font=("Poppins Light", 9 * -1)
)

canvas.create_text(
    30.0,
    674.0,
    anchor="nw",
    text="Ajuste a proporção para reduzir a imagem",
    fill="#598FAE",
    font=("Poppins Bold", 11 * -1)
)

canvas.create_text(
    30.0,
    687.0,
    anchor="nw",
    text="recomendado: 70",
    fill="#598FAE",
    font=("Poppins", 11 * -1)
)

canvas.create_rectangle(
    53.0,
    351.0,
    353.0,
    367.2209949493408,
    fill="#598FAE",
    outline=""
)

canvas.create_text(
    147.5,
    352.0,
    anchor="nw",
    text="↑   marca selecionada   ↑",
    fill="#FFFFFF",
    font=("Poppins Bold", 9 * -1)
)

canvas.create_rectangle(
    53.0,
    606.0,
    353.0,
    622.2209949493408,
    fill="#598FAE",
    outline=""
)

canvas.create_text(
    149.0,
    607.0,
    anchor="nw",
    text="↑   fotos selecionadas   ↑",
    fill="#FFFFFF",
    font=("Poppins Bold", 9 * -1)
)

canvas.create_rectangle(
    29.0,
    146.0,
    148.0,
    164.0,
    fill="#598FAE",
    outline=""
)

canvas.create_rectangle(
    29.0,
    401.0,
    148.0,
    419.0,
    fill="#598FAE",
    outline=""
)

canvas.create_text(
    73.0,
    400.0,
    anchor="nw",
    text="fotos",
    fill="#FFFFFF",
    font=("Poppins Bold", 12 * -1)
)

canvas.create_text(
    44.0,
    145.0,
    anchor="nw",
    text="marca d’água",
    fill="#FFFFFF",
    font=("Poppins Bold", 12 * -1)
)

canvas.create_text(
    338.0,
    715.0,
    anchor="nw",
    text="Studio Sérgio Silva",
    fill="#000000",
    font=("Poppins Bold", 9 * -1)
)


#SCROLLBAR
entry_2 = Text(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    font=("Poppins Light", 16 * -1),
    wrap='word',
    state=DISABLED
)

scrollbar = Scrollbar(window, orient="vertical", command=entry_2.yview)
entry_2.configure(yscrollcommand=scrollbar.set)

# posicionando scroll
scrollbar.place(
    x=335.5,  # 105 (posição x do entry_2) + 304 (largura do entry_2)
    y=440.0,
    height=183.0
)

entry_2.place(
    x=53.0,
    y=440.0,
    width=300.0,  # ajustar a largura para acomodar a barra de scroll
    height=166.0
)



# botao de selecionar marca d'água
botao_imagem_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
botao_1 = Button(
    image=botao_imagem_1,
    borderwidth=0,
    highlightthickness=0,
    command=carregar_marca_dagua,  # Comando para abrir o explorador de arquivos para uma única imagem
    relief="flat"
)
botao_1.place(
    x=375.0,
    y=281.0,
    width=78.0,
    height=18.248619079589844
)


# botao de selecionar fotos
botao_imagem_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
botao_2 = Button(
    image=botao_imagem_2,
    borderwidth=0,
    highlightthickness=0,
    command=carregar_fotos,  # Comando para abrir o explorador de arquivos para múltiplas imagens
    relief="flat"
)
botao_2.place(
    x=375.0,
    y=523.0,
    width=78.0,
    height=18.248619079589844
)

















# botão ajusar e finalizar
botao_imagem_3 = PhotoImage(file=relative_to_assets("button_3.png"))
botao_3 = Button(
    image=botao_imagem_3,
    borderwidth=0,
    highlightthickness=0,
    command=processar_imagens,  # Usar a nova função que inicia o processamento com a janela de status
    relief="flat"
)
botao_3.place(
    x=539.3480834960938,
    y=669.1160278320312,
    width=131.7955780029297,
    height=24.331491470336914
)

# fechar programa
botao_imagem_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
botao_4 = Button(
    image=botao_imagem_4,
    borderwidth=0,
    highlightthickness=0,
    command=window.destroy,  # Comando para fechar a janela
    relief="flat"
)
botao_4.place(
    x=642.0,
    y=39.0,
    width=30.0,
    height=30.0
)

file_paths = []

# adicionar um (x) em fotos repetidas
def gerar_nome_arquivo(caminho_destino):
    base, extensao = Path(caminho_destino).stem, Path(caminho_destino).suffix
    contador = 1
    novo_caminho = Path(caminho_destino)
    
    while novo_caminho.exists():
        novo_nome = f"{base} ({contador}){extensao}"
        novo_caminho = Path(Path(caminho_destino).parent) / novo_nome
        contador += 1
    
    return novo_caminho


# Função para reduzir as imagens
def reduzir_imagens(fotos, porcentagem, pasta_destino):
    for foto in fotos:
        with Image.open(foto) as img:
            largura, altura = img.size
            nova_largura = int(largura * (porcentagem / 100))
            nova_altura = int(altura * (porcentagem / 100))
            img_reduzida = img.resize((nova_largura, nova_altura), Image.Resampling.LANCZOS)
            
            nome_arquivo = Path(foto).name
            caminho_destino = Path(pasta_destino) / nome_arquivo
            
            # Verificar e gerar um novo nome se necessário
            caminho_destino = gerar_nome_arquivo(caminho_destino)
            
            img_reduzida.save(caminho_destino)


def escolher_pasta_destino():
    return filedialog.askdirectory(title="Escolha a pasta para salvar as imagens reduzidas")


# SLIDER
slider = Scale(
    window,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    length=200,
    width=12,
    sliderlength=15,
    bg="#F4F4F4",
    fg="black",
    activebackground="#588FAE",
    troughcolor="#588FAE",
    borderwidth=0,
    highlightthickness=0

)

# Posicionando o slider no canvas
slider_window = canvas.create_window(280, 657, window=slider, anchor="nw")
slider.set(70)

def valor_slider(): #obtem o valor dado ao slider
    return int(slider.get())



# Carregar a marca d'água salva ao iniciar o programa
carregar_marca_dagua_salva()

window.resizable(False, False)
window.mainloop()
