from tkinter import *

import pymysql

from tkinter import messagebox
from tkinter import ttk

class admin_janela():

    def cadastrar_produto(self):
        self.cadastrar = Tk()
        self.cadastrar.title('Cadastro de Produtos')
        self.cadastrar['bg'] = '#524f4f'

        Label(self.cadastrar, text='Cadastre os produtos', bg='#524f4f', fg='white').grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        Label(self.cadastrar, text='Nome', bg='#524f4f', fg='white').grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        self.nome = Entry(self.cadastrar)
        self.nome.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Ingredientes', bg='#524f4f', fg='white').grid(row=2, column=0, columnspan=1, padx=5, pady=5)
        self.ingredientes = Entry(self.cadastrar)
        self.ingredientes.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Grupo', bg='#524f4f', fg='white').grid(row=3, column=0, columnspan=1, padx=5, pady=5)
        self.grupo = Entry(self.cadastrar)
        self.grupo.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

        Label(self.cadastrar, text='Preço', bg='#524f4f', fg='white').grid(row=4, column=0, columnspan=1, padx=5, pady=5)
        self.preco = Entry(self.cadastrar)
        self.preco.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

        Button(self.cadastrar, text="Cadastrar", width=15, bg="gray", relief='flat', highlightbackground='#524f4f', command=self.cadastrar_produtos_backend).grid(row=5, column=0, padx=5, pady=5)
        Button(self.cadastrar, text="Excluir", width=15, bg="gray", relief='flat', highlightbackground='#524f4f', command=self.remover_cadastros_backend).grid(row=5, column=1, padx=5, pady=5)
        Button(self.cadastrar, text="Atualizar", width=15, bg="gray", relief='flat',highlightbackground='#524f4f', command=self.cadastrar_produtos_backend).grid(row=6, column=0, padx=5, pady=5)
        Button(self.cadastrar, text="Limpar produtos", width=15, bg="gray", relief='flat',highlightbackground='#524f4f', command=self.limpar_cadastros_backend).grid(row=6, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(self.cadastrar, selectmode="browse", column=("column1", "column2", "column3", "column4"),
                                 show='headings')

        self.tree.column("column1", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Nome')

        self.tree.column("column2", width=400, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Ingredientes')

        self.tree.column("column3", width=200, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Grupo')

        self.tree.column("column4", width=60, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Preço')

        self.tree.grid(row=0, column=4, padx=10, pady=10, columnspan=3, rowspan=6)

        self.mostrar_produtos_backend()

        self.cadastrar.mainloop()

    def mostrar_produtos_backend(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='projetopizzaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
             print('Erro ao conectar no banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from produtos')
                resultados = cursor.fetchall()
        except:
            print('Erro ao conectar no banco de dados')

        self.tree.delete(*self.tree.get_children())

        linhaV = []

        for linha in resultados:
            linhaV.append(linha['nome'])
            linhaV.append(linha['ingredientes'])
            linhaV.append(linha['grupo'])
            linhaV.append(linha['preco'])

            self.tree.insert("", END, values=linhaV, iid=linha['id'], tag='1')

            linhaV.clear()

    def cadastrar_produtos_backend(self):
        nome = self.nome.get()
        ingredientes = self.ingredientes.get()
        grupo = self.grupo.get()
        preco = self.preco.get()

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='projetopizzaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
             print('Erro ao conectar no banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('insert into produtos(nome, ingredientes, grupo, preco) values (%s, %s, %s, %s)', (nome, ingredientes, grupo, preco))
                conexao.commit()
        except:
            print('Erro ao conectar no banco de dados')

        self.mostrar_produtos_backend()

    def remover_cadastros_backend(self):
        idDeletar = int(self.tree.selection()[0])

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='projetopizzaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
             print('Erro ao conectar no banco de dados')

        try:
            with conexao.cursor() as cursor:
                cursor.execute('delete from produtos where id = {}'.format(idDeletar))
                conexao.commit()
        except:
            print('Erro ao conectar no banco de dados')

        self.mostrar_produtos_backend()

    def limpar_cadastros_backend(self):
        if messagebox.askokcancel('ATENÇÃO!!!', 'Deseja excluir todos os dados da tabela?'):

            try:
                conexao = pymysql.connect(
                    host='localhost',
                    user='root',
                    password='',
                    db='projetopizzaria',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor
                )
            except:
                print('Erro ao conectar no banco de dados')

            try:
                with conexao.cursor() as cursor:
                    cursor.execute('truncate table produtos')
                    conexao.commit()
            except:
                print('Erro ao conectar no banco de dados')

            self.mostrar_produtos_backend()

    def __init__(self):
        self.root = Tk()
        self.root.title('Administrador')
        self.root.geometry('500x500')

        Button(self.root, text='Pedidos', width=20).grid(row=0, column=0, padx=10, pady=10)
        Button(self.root, text='Cadastros', width=20, bg='blue3', command=self.cadastrar_produto).grid(row=1, column=0, padx=10, pady=10)


        self.root.mainloop()
class janela_login():

    def vericica_login(self):
        autenticado = False
        usuario_master = False

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='projetopizzaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
             print('Erro ao conectar no banco de dados')

        usuario = self.login.get()
        senha = self.senha.get()

        try:
            with conexao.cursor()  as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao conectar no banco de dados')

        for linha in resultados:
            if usuario == linha['nome'] and senha == linha['senha']:
                if linha['nivel'] == 1:
                    usuario_master = False
                elif linha['nivel'] == 2:
                    usuario_master = True
                autenticado = True
                break
            else:
                autenticado = False

        if not autenticado:
            messagebox.showinfo('Login', 'Usuário ou senha invalida')

        if autenticado:
            self.root.destroy()
            if usuario_master:
                admin_janela()

    def cadastro_backend(self):
        codigo_padrao = '123456'

        if self.codigo_seguranca.get() == codigo_padrao:
            if len(self.login.get()) <= 20:
                if len(self.senha.get()) <= 50:
                    nome = self.login.get()

                    senha = self.senha.get()

                    try:
                        conexao = pymysql.connect(
                            host='localhost',
                            user='root',
                            password='',
                            db='projetopizzaria',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
                    except:
                        print('Erro ao conectar no banco de dados')

                    try:
                        with conexao.cursor() as cursor:
                            cursor.execute('insert into cadastros (nome, senha, nivel) values (%s, %s, %s)', (nome, senha, 1))
                            conexao.commit()
                        messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso!')
                        self.root.destroy()
                    except:
                        print('Erro ao inserir dados no banco de dados')
                else:
                    messagebox.showinfo('ERRO', 'Por favor insira uma senha com 50 ou menos caracteres')
            else:
                messagebox.showinfo('ERRO', 'Por favor insira um nome com 20 ou menos caracteres')
        else:
            messagebox.showinfo('ERRO', 'Erro no código de segurança')

    def cadastro(self):
        Label(self.root, text='Chave de Segurança').grid(row=3, column=0, padx=5, pady=5)
        self.codigo_seguranca=Entry(self.root, show='*')
        self.codigo_seguranca.grid(row=3, column=1, padx=10, pady=5)

        Button(self.root, text='Confirmar cadastro', width=15, bg='blue1', command=self.cadastro_backend).grid(row=4, column=0, columnspan=3, padx=10, pady=5)

    def update_backend(self):

        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='projetopizzaria',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
             print('Erro ao conectar no banco de dados')


        try:
            with conexao.cursor()  as cursor:
                cursor.execute('select * from cadastros')
                resultados = cursor.fetchall()
        except:
            print('Erro ao conectar no banco de dados')

        self.tree.delete(*self.tree.get_children())

        linhav = []

        for linha in resultados:
            linhav.append(linha['id'])
            linhav.append(linha['nome'])
            linhav.append(linha['senha'])
            linhav.append(linha['nivel'])

            self.tree.insert("", END, values=linhav, iid=linha['id'], tag='1')

            linhav.clear()

    def visualizar_cadastro(self):
        self.vc = Toplevel()
        self.vc.resizable(False, False)
        self.vc.title('Visualizar Cadastro')

        self.tree = ttk.Treeview(self.vc, selectmode="browse", column=("column1", "column2", "column3", "column4"), show='headings')

        self.tree.column("column1", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#1', text='Id')

        self.tree.column("column2", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#2', text='Usuário')

        self.tree.column("column3", width=100, minwidth=500, stretch=NO)
        self.tree.heading('#3', text='Senha')

        self.tree.column("column4", width=40, minwidth=500, stretch=NO)
        self.tree.heading('#4', text='Nível')

        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.update_backend()

        self.vc.mainloop()


    def __init__(self):
        self.root = Tk()
        self.root.title('Login')

        Label(self.root, text='Faça o login').grid(row=0, column=0, columnspan=2)

        Label(self.root, text='Usuário').grid(row=1, column=0)
        self.login = Entry(self.root)
        self.login.grid(row=1, column=1, padx=5, pady=5)

        Label(self.root, text='Senha').grid(row=2, column=0)
        self.senha = Entry(self.root, show='*')
        self.senha.grid(row=2, column=1, padx=5, pady=5)

        Button(self.root, text='Login', bg='green3', width=10, command=self.vericica_login).grid(row=5, column=0, padx=5, pady=5)

        Button(self.root, text='Cadastrar', bg='orange3', width=10, command=self.cadastro).grid(row=5, column=1, padx=5, pady=5)

        Button(self.root, text='Visualizar Cadastro', bg='white', command=self.visualizar_cadastro).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.root.mainloop()


janela_login()