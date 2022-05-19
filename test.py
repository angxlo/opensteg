#bibliotecas necessárias
import sys
import numpy as np
from PIL import Image
# garante que valores contidos em arrays SEMPPRE exibam sua representação completa, sem arredondar
np.set_printoptions(threshold=sys.maxsize)

#função de codificação
def Encode(source, message, destination):
    # abre a imagem como um array de todos os seus pixels
    img = Image.open(source, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    # diferencia entre imagens do tipo rgb ou rgba (com transparência)
    if img.mode == 'RGB':
        imgtype = 3
    elif img.mode == 'RGBA':
        imgtype = 4

    # calcula a quantidade de pixels disponiveis para ediçao
    total_pixels = array.size//imgtype

    # pede a chave delimitadora (onde o código irá parar de decodifcar) ao usuário
    message += input("Input the delimiter key: ")
    # transforma a mensagem em valores binários
    binary_message = ''.join([format(ord(i), "08b") for i in message])
    # calcula a quantidade mínima de pixels para codificar a mensagem digitada
    required_pixels = len(binary_message)

    # calcula se a mensagem é grande de mais para o tamanho da imagem
    if required_pixels > total_pixels:
        print("Failed to encode. Image is too small.")
    else:
        index=0
        for j in range(total_pixels):
            for k in range(0, 3):
                if index < required_pixels:
                    # modifica os bits menos significativos da imagem para exibir a mensagem escondida
                    array[j][k] = int(bin(array[j][k])[2:9] + binary_message[index], 2)
                    index += 1

        # transforma o array de acordo com altura, largura e tipo de pixel da imagem
        array=array.reshape(height, width, imgtype)
        # transforma o array em imagem com a biblioteca Pillow
        encoded_img = Image.fromarray(array.astype('uint8'), img.mode)
        encoded_img.save(destination)
        print("Image Encoded Successfully")

#decoding function
def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")

#main function
def Stego():
    print("--Welcome to $t3g0--")
    print("1: Encode")
    print("2: Decode")

    func = input()

    if func == '1':
        print("Enter Source Image Path")
        src = input()
        print("Enter Message to Hide")
        message = input()
        print("Enter Destination Image Path")
        dest = input()
        print("Encoding...")
        Encode(src, message, dest)

    elif func == '2':
        print("Enter Source Image Path")
        src = input()
        print("Decoding...")
        Decode(src)

    else:
        print("ERROR: Invalid option chosen")

Stego()