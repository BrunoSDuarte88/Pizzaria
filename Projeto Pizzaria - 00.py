import pymysql.cursors

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='pizzaria',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

autentico = False

def logar_cadastrar():
    usuario_existente = 0
    autenticado = False
    usuario_master = False

    if decisao == 1:
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuario_master = False
                elif linha ['nivel'] == 2:
                    usuario_master == True
                autenticado = True
            else:
                autenticado = False
        if not autenticado:
            print('e-mail ou senha errado')
    elif decisao == 2:
        print('Faça seu cadastro')
        nome = input('Digite seu nome: ')
        senha = input('Digite sua senha: ')

        for linha in resultado:
            if nome == linha['nome'] and senha == linha['senha']:
                usuario_existente = 1
        if usuario_existente == 1:
            print('Usuário ja cadastrado! Tente um nome ou senha diferente')
        elif usuario_existente == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                    conexao.commit()
                print('Usuario cadastrado com sucesso')
            except:
                print('Erro ao inserir as informações no banco de dados')

    return autenticado, usuario_master



while not autentico:
    decisao = int(input('Digite 1 para logar ou 2 para cadastrar: '))

    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros')
            resultado = cursor.fetchall()

    except:
        print('Erro ao conectar no banco de dados')

    autentico, usuario_supremo = logar_cadastrar()

if autentico == True:
    print('Autenticado')