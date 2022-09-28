import numpy as np
from PIL import Image
import csv

txt = []
with open("lang/pt-BR.csv", newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in reader:
        txt.append(row)

def hide(inArch, msg, outArch, step):
    # Valores padrão
    match step:
        case "1": 
            stepo = 3
            ctrl = 0
        case "2": 
            stepo = 3
            ctrl = 1
        case "3":
            stepo = 3
            ctrl = 2
        case _: 
            stepo = 1
            ctrl = 0

    opn = Image.open(inArch, 'r') # Abre a imagem para leitura
    x, y = opn.size # Pega o tamanho ("x" para largura, "y" para altura)
    img = np.array(list(opn.getdata())) # Pega os valores dos pixels da imagem, em sequência, transforma em uma lista, depois em um array

    if opn.mode == 'RGB':  n = 3 # Checa se a imagem é RGB, e atribui o valor 3 a "n" 
    elif opn.mode == 'RGBA': n = 4 # Checa se a imagem é RGB, e atribui o valor 4 a "n"

    # print("img:\n",img)

    qnt = int((img.size//n)/stepo) # Pega quantidade de colunas da imagem
    # print("qnt:\n",qnt)

    msg += "!@#$" # Adiciona o delimitador da mensagem
    b_msg = ''.join([format(ord(i),"08b") for i in msg]) # Pega mensagem, transforma cada digito em binário de 8 digitos ("08b")

    req_qnt = len(b_msg) # Pega a quantidade mínima de bits 

    if req_qnt > qnt: # Se a quantidade mínima de bits for maior que a mensagem...
        print("ERRO: Imagem menor que mensagem. Insira uma imagem maior.") # ...mensagem de erro aparece.
    else: # Se não for maior...
        i = 0 # ...índice é 0...
        for j in range(qnt): # ...roda um for pelas linhas...
            for k in range(0+ctrl,3, int(stepo)): # ...roda um for pelas colunas.
                if i < req_qnt: # Se índice for menor que a quantidade mínima de pixels para a mensagem...
                    img[j][k] = int(bin(img[j][k]) [2:9] + b_msg[i], 2) # ...esconde a mensagem (altera o pixel da imagem, mudando o bit menos significativo ([2:9] recorta da posição 2 até a 9 do elemento do array))
                    # print(f"Binário: {bin(img[j][k])}\nRGB: {img[j][k]}")
                    i += 1 # incrementa o índice
    
    img = img.reshape(y, x, n) # Altera o formato do array de pixels da imagem
    outImg = Image.fromarray(img.astype('uint8'), opn.mode) # Transforma o array "img" em uma imagem
    outImg.save(f"{outArch}", format='png') # Salva a imagem no diretorio desejado
    print(f"Pronto.\nMensagem esteganografada: {msg[:-4]}\nArquivo original: {inArch}\nArquivo final: {outArch}")

def show(inArch, step):
    # Valores padrão
    match step:
        case "1": 
            stepo = 3
            ctrl = 0
        case "2": 
            stepo = 3
            ctrl = 1
        case "3":
            stepo = 3
            ctrl = 2
        case _: 
            stepo = 1
            ctrl = 0
    
    opn = Image.open(inArch, 'r') # Abre a imagem para leitura
    img = np.array(list(opn.getdata())) # Pega os valores dos pixels da imagem, em sequência, transforma em uma lista, depois em um array

    # Mesma coisa de cima
    if opn.mode == 'RGB': n = 3
    elif opn.mode == 'RGBA': n = 4
    
    qnt = int((img.size//n)/stepo) # Pega quantidade de colunas da imagem

    sec = "" # Cria variável para bits escondidos
    for j in range(qnt): # percorre o array
        for k in range(0+ctrl, 3, int(stepo)):
            sec += (bin(img[j][k])[2:][-1]) # pega o ultimo bit do byte e coloca em uma string

    sec = [sec[i:i+8] for i in range(0, len(sec), 8)] # pega os bits de 8 em 8

    msg = ""
    for i in range(len(sec)):
        if msg[-4:] == "!@#$":
            break
        else:
            msg += chr(int(sec[i],2))
    if "!@#$" in msg:
        print(msg[:-4])
        with open(inArch[:-4]+".txt", "w") as file:
            file.write(msg[:-4])
    else:
        print("Sem Mensagem Escondida.")
