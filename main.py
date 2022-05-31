from PyQt5 import  uic,QtWidgets
import sqlite3
from senhar import senhar_segreda
import logging
import os

#configurarções LOGS
logging.basicConfig(
    level=0, 
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s:',
    encoding='UTF-8',
    filename=os.path.join('./log/log.log'), 
    )
    
Logger=logging.getLogger(__name__)


def chama_segunda_tela():
    
    primeira_tela.erro.setText("")
    nome_usuario = primeira_tela.Login.text()
    senha = primeira_tela.senhar.text()
    senhar_s = senhar_segreda(senha)
    try:
        banco = sqlite3.connect(os.path.join('./banco/banco_cadastro.db')) 
        curso= banco.cursor()
        sql = "select senha from cadastro where login = ? and senha = ? "
        valor= (nome_usuario,senhar_s,)
        curso.execute(sql, valor)
        senhar_b = curso.fetchall()
        banco.commit()
        # print(senhar_s, senhar_b[0][0])
        banco.close()
        if senhar_s == senhar_b[0][0]:
            primeira_tela.close()
            segunda_tela.show()

        Logger.info('Normal ok')

        
       
        
    except sqlite3.Error as E:
        primeira_tela.erro.setText(f'ERRO {E}')
        Logger.critical('erro no banco de dado')
        

    except:
        primeira_tela.erro.setText("Dados de login incorretos!")
        Logger.warning('Dados de login incorretos!')
        
            
      
          
        
    

def logout():
    #PARA SAIR DO SISTEMA
    segunda_tela.close()
    primeira_tela.show()
    if primeira_tela.erro.setText("") !="":
        primeira_tela.erro.setText("")
    if primeira_tela.Login.text()!='' and primeira_tela.senhar.text() != '':
        primeira_tela.Login.setText('')
        primeira_tela.senhar.setText('')

def abre_tela_cadastro():
    tela_cadastro.show()
    primeira_tela.close()
    if tela_cadastro.erro.setText("") !="":
        tela_cadastro.erro.setText("")
    if tela_cadastro.login.text() != '' and tela_cadastro.senhar.text() !="":
        tela_cadastro.login.setText('')
        tela_cadastro.senhar.setText('')

def volta_primeira(): 
    #VOLTA PARA PRIMEIRA TELA
    
    tela_cadastro.close()
    primeira_tela.show()
    if primeira_tela.Login.text()!='' and primeira_tela.senhar.text() != '':
        primeira_tela.Login.setText('')
        primeira_tela.senhar.setText('')
  
    if primeira_tela.erro.setText("") !="":
        primeira_tela.erro.setText("")




def cadastrar():
    """para cadastra tem ter login 
    uma senhar maio ou igual A 8
"""
    
    login = tela_cadastro.login.text()
    senha = tela_cadastro.senhar.text()
    c_senha = tela_cadastro.c_senhar.text()
    senha_s = senhar_segreda(senha)

    if login =="" and senha=="":
        tela_cadastro.erro.setText("campos esta vazio")
        Logger.error('usuario tento me encanar')
    

    elif senha == c_senha:
        if len(senha)<8 and login=="":
            tela_cadastro.erro.setText("ops senhar esta menos 8 támbem login esta vazio")
            Logger.error('usuario tento cadastrar sem Login ')
        elif len(senha)<8: 
            tela_cadastro.erro.setText("erro campo senha e menos que 8")
            Logger.error('senhar meno do minino')
        elif login=="":
            tela_cadastro.erro.setText("campo login esta vazio")
            Logger.error('meu!!!, sem longin não dar')

        else:
            try:
                banco = sqlite3.connect(os.path.join('./banco/banco_cadastro.db')) 
                cursor = banco.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS cadastro (id INTEGER PRIMARY KEY autoincrement,login text,senha text)")
                sql=("INSERT INTO cadastro  (login, senha) VALUES(?,?)" )
                dados= (login, senha_s)
                banco.execute(sql,dados)
                banco.commit() 
                banco.close()
                tela_cadastro.close()  
                primeira_tela.show()
                Logger.info('sucesso')

            except sqlite3.Error as E:
                tela_cadastro.erro.setText('tenta mais tarde de novo')
                Logger.critical('erro grave {E}')
    else:
         tela_cadastro.erro.setText("As senhas digitadas estão diferentes")
         Logger.info('As senhas diferentes não sei tem na cabeça')
        
#configurarções
app=QtWidgets.QApplication([])
primeira_tela=uic.loadUi(os.path.join("./tela/login.ui"))
segunda_tela = uic.loadUi(os.path.join("./tela/bem-vindo.ui"))
tela_cadastro = uic.loadUi(os.path.join("./tela/cadastro.ui"))
primeira_tela.entra.clicked.connect(chama_segunda_tela)
segunda_tela.sair.clicked.connect(logout)
primeira_tela.senhar.setEchoMode(QtWidgets.QLineEdit.Password)
primeira_tela.cadastror.clicked.connect(abre_tela_cadastro)
tela_cadastro.cadastror.clicked.connect(cadastrar) 
tela_cadastro.voltar.clicked.connect(volta_primeira)
tela_cadastro.senhar.setEchoMode(QtWidgets.QLineEdit.Password)
tela_cadastro.c_senhar.setEchoMode(QtWidgets.QLineEdit.Password)


primeira_tela.show()
app.exec()

