from time import sleep

menu = """
-----------Menu Principal -----------
            [d] - Depositar
            [s] - Sacar
            [e] - Extrato
            [c] - Cadastrar Usuario
            [cc] - Cadastrar Conta
            [lc] - Listar Contas
            [q] - Sair
--------------------------------------
             """
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
depositos = 0

def saque(*, valor_saldo, valor, valor_extrato, limite_saque, meu_numero_saques, meu_limite_saques):
    global saldo
    global extrato
    global numero_saques
    maximo_saques = meu_numero_saques == LIMITE_SAQUES
    sem_saldo = valor > saldo
    valor_limite = valor > limite

    if maximo_saques:
        print ("Você chegou ao seu limite de saques.")
        print ("voltando ao menu principal...")
        sleep(2)
    elif sem_saldo:
        print ("Saldo insuficiente para sacar!")
        print ("voltando ao menu principal...")
        sleep(2)
    elif valor_limite:
        print ("Valor passa do limite que pode ser sacado!")
        print ("voltando ao menu principal...")
        sleep(2)
    elif valor > 0:         
        saldo -= valor
        numero_saques += 1
        extrato += f"{numero_saques}º Saque: |R${valor:.2f}|\n"
        print("Valor sacado com sucesso.")
        print ("voltando ao menu principal...")
        sleep(2)
    else:
        print("Valor inválido.")
        print ("voltando ao menu principal...")
        sleep(2)

    return saldo, extrato, numero_saques

def deposito(valor_saldo, valor, valor_extrato):
    global depositos
    global saldo
    global extrato

    if valor > 0:
        saldo += valor
        depositos += 1
        extrato += f"{depositos}º valor depositado: |R${valor:.2f}|\n"
        print("Deposito realizado com sucesso")
        print ("voltando ao menu principal...")
        sleep(2)
    else:
            print("Valor inválido.")
            print ("voltando ao menu principal...")
            sleep(2)
    return saldo, extrato

def imprimir_extrato(saldo, *, extrato):
    print(f"""
========== EXTRATO COMPLETO ==========
{extrato}
          Saldo atual: R${saldo:.2f}
========================================""")
    print ("voltando ao menu principal...")
    sleep(2)

usuarios={}
contas={}
contas_criadas = 1
AGENCIA = "0001"

def filtro_usuario(num_cpf, todos_usuarios):
    if num_cpf in todos_usuarios:
        return True
    else:
        return False
def cadastrar_usuario(cpf):
    global usuarios
    usuario_existente = filtro_usuario(cpf,usuarios)
    if usuario_existente:
        print("O CPF informado já existe no sistema.")
        print ("voltando ao menu principal...")
        sleep(2)
        return None
        
    else:
        nome = str(input("Insira seu nome: "))
        data_de_nascimento = str(input("Insira sua data de nascimento ('dia/mes/ano'): "))
        logradouro = str(input("""
            ENDEREÇO: 
Insira o logradouro que reside: """))
        num = int(input("Numero: "))
        bairro = str(input("Bairro: "))
        cidade = str(input("Cidade: "))
        estado = str(input("Estado('apenas silga'): "))
    endereco = f"""
    Logradouro: {logradouro}, Numero: {num}
    Bairro: {bairro}, Cidade: {cidade}/{estado}
    """
    data_de_nasc = f"{data_de_nascimento[0:2]}/{data_de_nascimento[2:4]}/{data_de_nascimento[4:]}"
    print("\nUsuario cadastrado com sucesso")
    print ("voltando ao menu principal...")
    sleep(2)
    user = {"Nome":nome, "Data de Nascimento": data_de_nasc, "Endereço": endereco, "contas": {"conta1" : 0, "AGENCIA": "0001"}}
    usuarios[cpf] = user
    return usuarios
def cadastrar_conta(cpf,lista_usuarios,lista_contas, agencia): 
    global contas
    global contas_criadas
    usuario_existente = filtro_usuario(cpf,lista_usuarios)
    if usuario_existente:
        if cpf in contas:
            contacliente = {f"Conta{contas_criadas}" : contas_criadas, f"agencia da Conta{contas_criadas}" : agencia}
            contas[cpf].update(contacliente)
            print(f"""
            Conta criada com sucesso
            CPF: {cpf}
            Conta: {contas_criadas}
            Agencia: {agencia}""")
            print ("voltando ao menu principal...")
            sleep(2)
            contas_criadas += 1
            return contas, contas_criadas
        else:
            contacliente = {f"Conta{contas_criadas}" : contas_criadas, f"agencia da Conta{contas_criadas}" : agencia}
            contas[cpf] = contacliente
            print(f"""
            Conta criada com sucesso
            CPF: {cpf}
            Conta: {contas_criadas}
            Agencia: {agencia}""")
            print ("voltando ao menu principal...")
            sleep(2)
            contas_criadas += 1
            return contas, contas_criadas
    else:
        print("CPF não cadastrado no sistema.")
        print ("voltando ao menu principal...")
        sleep(2)
def listar_contas(cpf, lista_usuarios, lista_contas):
    usuario_existente = filtro_usuario(cpf,lista_usuarios)
    newline = "\n"
    if usuario_existente:
        print (f"""
================================================
    Contas cadastradas nesse CPF: 
            CPF: {cpf} 
            Nome: {usuarios[cpf]["Nome"]}
{newline.join(f"{key}: {value}" for key, value in contas[cpf].items())}

    =======================================""")
        print ("voltando ao menu principal...")
        sleep(2)

    else:
        print("CPF não cadastrado no sistema.")
        print ("voltando ao menu principal...")
        sleep(2)

while True:
    opcao = input(menu)

    if opcao.lower() == "d":
        valor = float(input("Insira o valor a ser depositado: "))
        deposito(saldo,valor,extrato)
    elif opcao.lower() == "s":
        valor = float(input("Insira o valor a ser sacado: "))
        saque(valor_saldo=saldo, valor=valor, valor_extrato=extrato, limite_saque = LIMITE_SAQUES, meu_numero_saques=numero_saques,meu_limite_saques=limite)
    elif opcao.lower() == "e":
        imprimir_extrato(saldo, extrato=extrato)
    elif opcao.lower() == "c":
        cpf = int(input("Insira seu CPF: "))
        cadastrar_usuario(cpf)


    elif opcao.lower() == "cc":
        cpf = int(input("Insira o CPF do usuario: "))
        cadastrar_conta(cpf,usuarios,contas,AGENCIA)
    elif opcao.lower() == "lc":
        cpf = int(input("Insira o CPF do usuario: "))
        listar_contas(cpf,usuarios,contas)
    elif opcao.lower() == "q":
        print("Obrigado por usar nosso sistema!")
        break
    else:
        print("opção inválida!")




'''print(f"""
              ___________Extrato___________
              Saldo atual: R${saldo:.2f}
              
              Numero de depósitos: {depositos}
              Valores depositados: {valor_depositado}
              Numero de saques: {numero_saques}
              Valores sacados: {valor_sacado}\n""")
        print ("voltando ao menu principal...")
        sleep(2)'''

