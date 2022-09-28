from Steg import steg

# Seleção do método e arquivo (placeholder)
print("hide ou show")
esc = input()
print("Digite o nome do arquivo:")
nome = input()
print("RGB(0), R(1), G(2) ou B(3)?")
step = input()

if (esc=="hide"):
    print("Digite a mensagem:")
    msg = input()
    print("Digite o arquivo final:")
    arch = input()
    steg.hide(nome, msg, arch, step)
elif (esc=="show"):
    steg.show(nome, step)
else:
    print("escolha inválida")