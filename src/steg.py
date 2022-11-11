import numpy as np
from PIL import Image

def setStepo(step):
    match step:
        case "1": 
            return 3 # Altera apenas um sub-pixel
        case "2": 
            return 3 # Altera apenas um sub-pixel
        case "3":
            return 3 # Altera apenas um sub-pixel
        case _: 
            return 1 # Altera todos os sub-pixels

def setCtrl(step):
    match step:
        case "1": 
            return 0 # Começa no sub-pixel "R"
        case "2": 
            return 1 # Começa no sub-pixel "G"
        case "3":
            return 2 # Começa no sub-pixel "B"
        case _:
            return 0 # Começa no sub-pixel "R"

def setOpn(inArch):
    img = Image.open(inArch, 'r') # Abre a imagem para leitura
    if img.mode != "RGB" and img.mode != "RGBA":
        img = img.convert("RGBA")
    return img

def setXY(opn):
    return opn.size # Pega o tamanho ("x" para largura, "y" para altura)

def setImg(opn):
    return np.array(list(opn.getdata()))# Pega os valores dos pixels da imagem, em sequência, 
                                        # transforma em uma lista e depois em um array

def setN(opn):
    if opn.mode == 'RGB':  return 3 # Checa se a imagem é RGB, e atribui o valor 3 a "n" 
    elif opn.mode == 'RGBA': return 4 # Checa se a imagem é RGB, e atribui o valor 4 a "n"

def setQnt(img, n, stepo):
    # qnt = (img.size//n) # Pega quantidade de colunas da imagem
    return int((img.size//n)/stepo) # Pega quantidade de colunas da imagem

def setMsg(msg):
    msg += "!@#$" # Adiciona o delimitador da mensagem
    b_msg = ''.join([format(ord(i),"08b") for i in msg]) # Pega mensagem, transforma cada digito em binário de 8 digitos ("08b")
    return b_msg

def esteganografia(req_qnt, qnt, ctrl, stepo, img, b_msg, n):
    if req_qnt > qnt: # Se a quantidade mínima de bits for maior que a mensagem...
        return
    else: # Se não for maior...
        i = 0 # ...índice é 0...
        for j in np.arange(qnt): # ...roda um for pelas linhas...
            for k in np.arange(0+ctrl, n, int(stepo)): # ...roda um for pelas colunas.
                if i < req_qnt: # Se índice for menor que a quantidade mínima de pixels para a mensagem...
                    img[j][k] = int(bin(img[j][k]) [2:-1] + b_msg[i], 2) # ...esconde a mensagem (altera o pixel da imagem, mudando o bit menos significativo ([2:9] recorta da posição 2 até a 9 do elemento do array))
                    i += 1 # incrementa o índice
                else: return img

def salvar(y, x, n, opn, outArch, img):
    img = img.reshape(y, x, n) # Altera o formato do array de pixels da imagem
    outImg = Image.fromarray(img.astype('uint8'), opn.mode) # Transforma o array "img" em uma imagem
    outImg.save(f"{outArch}", format='png') # Salva a imagem no diretorio desejado

def esteganalise(qnt, ctrl, stepo, img, n):
    sec = "" # Cria variável para bits escondidos
    for j in range(qnt): # percorre o array
        for k in range(0+ctrl, n, int(stepo)):
            sec += (bin(img[j][k])[2:][-1]) # pega o ultimo bit do byte e coloca em uma string
    sec = [sec[i:i+8] for i in range(0, len(sec), 8)] # pega os bits de 8 em 8
    return sec

def estegMsg(sec, inArch):
    msg = ""
    for i in range(len(sec)):
        if msg[-4:] == "!@#$":
            break
        else:
            msg += chr(int(sec[i],2))
    if "!@#$" in msg:
        with open(inArch+".txt", "w") as file:
            file.write(msg[:-4])
    else:
        return "nomessage"

def hide(inArch, msg, outArch, step):
    # Valores padrão
    stepo = setStepo(step)
    ctrl  = setCtrl(step)

    # Informações da imagem
    opn = setOpn(inArch)
    x, y = setXY(opn)
    img = setImg(opn)

    # Quantidade de sub-pixels
    n = setN(opn)

    # Quantidade 
    qnt = setQnt(img, n, stepo)

    # Mensagem
    b_msg = setMsg(msg)
    req_qnt = len(b_msg) # Pega a quantidade mínima de bits 

    # Esteganografia
    img = esteganografia(req_qnt, qnt, ctrl, stepo, img, b_msg, n)
    
    # Salvar a imagem
    salvar(y, x, n, opn, outArch, img)

def show(inArch, step, inDir):
    # Valores padrão
    stepo = setStepo(step)
    ctrl  = setCtrl(step)
    
    # Informações da imagem 
    opn = setOpn(inArch)
    img = setImg(opn)

    # Quantidade de sub-pixels
    n = setN(opn)
    
    # Quantidade 
    qnt = setQnt(img, n, stepo)

    # Esteganálise
    sec = esteganalise(qnt, ctrl, stepo, img, n)

    # Remonta a mensagem e retorna o sucesso da operação
    return estegMsg(sec, inDir)