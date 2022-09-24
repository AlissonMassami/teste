import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QAction, QDialog, QStackedWidget, QTableWidgetItem
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.uic import loadUi
from PyQt5.uic.properties import QtCore

colGastos=['Data', 'Registro', 'Valor', 'NomeSetor']
colSetor=['NomeSetor', 'Porcentagem', 'SaldoAtual']
colContas=['NomeConta', 'Valor']
colHist=['Mes', 'RendaMensal', 'CustoFixoTotal', 'Restante']
# INICIALIZAÇÕES
# CRIAR NOVO DF
#df = pd.DataFrame(columns=['Data', 'Registro', 'Valor'. 'NomeSetor'])
# df1 = pd.DataFrame(columns=['NomeSetor', 'Porcentagem', 'SaldoAtual'])
# df2 = pd.DataFrame(columns=['NomeConta', 'Valor'])
# df3 = pd.DataFrame(columns=['Mes', 'RendaMensal', 'CustoFixoTotal', 'Restante'])
# #EXPORTAR DF TO CSV
# df.to_csv('gastos.csv', encoding='utf-8')
#df1.to_csv('setores.csv', encoding='utf-8')
# df2.to_csv('contasFixas.csv', encoding='utf-8')
# df3.to_csv('historico.csv', encoding='utf-8')
#
df_gastos = pd.read_csv('gastos.csv', encoding='utf-8')
df_setores = pd.read_csv('setores.csv', encoding='utf-8')
df_contasFixas = pd.read_csv('contasFixas.csv', encoding='utf-8')
df_historico = pd.read_csv('historico.csv', encoding='utf-8')

app = QApplication(sys.argv)

janelaCadastro = loadUi('novoCadastro.ui')
menuPrincipal = loadUi('menuPrincipal.ui')
janelaLogin = loadUi('novoLogin.ui')
janelaAttContas = loadUi('atualizarContas.ui')
novoPagamento = loadUi("novoPagamento.ui")
telaGastos = loadUi("telaGastos.ui")

#funções
def fecharTelaLogin():
    janelaLogin.close()
    menuPrincipal.show()
def abrirJanelaCadastro():
    janelaCadastro.show()
    menuPrincipal.close()
    attListaCustos(janelaCadastro)
    attListaSetor(janelaCadastro)
def fecharJanelaCadastro():
    janelaCadastro.close()
    menuPrincipal.show()

def abrirJanelaAttCusto():
    menuPrincipal.close()
    janelaAttContas.show()
    attListaSetor(janelaAttContas)
    attListaCustos(janelaAttContas)

def fecharTelaAttContas():
    janelaAttContas.close()
    menuPrincipal.show()

def abrirJanelaNovoPag():
    menuPrincipal.close()
    novoPagamento.show()
    attListaCustos(novoPagamento)
def abrirAcerto():
    menuPrincipal.close()
    telaGastos.show()
    setores = []
    setores = df_setores['NomeSetor'].tolist()
    telaGastos.comboBox.addItems(setores)
    attSaldoGastos()

def attSaldoGastos():

    listaHeader = []
    for index, linha in df_setores.iterrows():
        print(linha['NomeSetor'],linha['SaldoAtual'])
        listaHeader.append(linha['NomeSetor'])
        listaHeader.append(str(linha['SaldoAtual']))
    print(listaHeader)
    telaGastos.tabelaSaldo.clearContents()
    telaGastos.tabelaSaldo.setColumnCount(len(listaHeader))
    telaGastos.tabelaSaldo.setHorizontalHeaderLabels(listaHeader)
    attListaGastos(tabela = telaGastos, listaHeader = listaHeader)

def addNovoCusto():
    global df_contasFixas
    nomeCusto=janelaCadastro.novoCustoText.text()
    valorCusto=janelaCadastro.novoValorText.text()
    custo = [nomeCusto, valorCusto]
    df = pd.DataFrame([custo], columns=colContas)
    df_contasFixas = pd.concat([df_contasFixas, df], ignore_index=True)
    attListaCustos(janelaCadastro)
    janelaCadastro.novoCustoText.clear()
    janelaCadastro.novoValorText.clear()

def addNovoSetor():
    global df_setores
    nomeSetor=janelaCadastro.novoSetor.text()
    valorPorc=janelaCadastro.novaPorcentagem.text()
    novoSet = [nomeSetor, valorPorc, 0]
    df = pd.DataFrame([novoSet], columns=colSetor)
    df_setores = pd.concat([df_setores, df], ignore_index=True)
    attListaSetor(janelaCadastro)
    janelaCadastro.novoSetor.clear()
    janelaCadastro.novaPorcentagem.clear()

def salvarGastosCSV():
    df_gastos.to_csv('gastos.csv', encoding='utf-8', index=False)
def salvarSetorCSV():
    df_setores.to_csv('setores.csv', encoding='utf-8', index=False)
def salvarContasFixas():
    df_contasFixas.to_csv('contasFixas.csv', encoding='utf-8', index=False)
def salvarHistorico():
    df_historico.to_csv('historico.csv', encoding='utf-8', index=False)

def attListaCustos(tabela):
    global df_contasFixas
    row=0
    tabela.listaDeCustos.setRowCount(len(df_contasFixas))
    for index, linha in df_contasFixas.iterrows():
        tabela.listaDeCustos.setItem(row, 0, QTableWidgetItem(linha['NomeConta']))
        tabela.listaDeCustos.setItem(row, 1, QTableWidgetItem(str(linha['Valor'])))
        row+=1

def attListaSetor(tabela):
    global df_setores
    row = 0
    tabela.listaSetor.setRowCount(len(df_setores))
    for index, linha in df_setores.iterrows():
        tabela.listaSetor.setItem(row, 0, QTableWidgetItem(linha['NomeSetor']))
        tabela.listaSetor.setItem(row, 1, QTableWidgetItem(str(linha['Porcentagem'])))
        tabela.listaSetor.setItem(row, 2, QTableWidgetItem(str(linha['SaldoAtual'])))
        row += 1
def attListaGastos(tabela, listaHeader):
    global df_gastos, df_setores
    #row = tabela.listaSaldo.rowCount()
    tabela.tabelaSaldo.setRowCount(len(df_gastos))
    print("oi")
    if len(df_gastos) > 0:
        print("oi1")
        lu = 0
        for index, linha in df_gastos.iterrows():
            print("oi2")
            col = listaHeader.index(linha['NomeSetor'])
            # df = pd.DataFrame(columns=['Data', 'Registro', 'Valor'. 'NomeSetor'])
            #tabela.listaSaldo.insertRow(0)
            print(linha['Registro'])
            tabela.tabelaSaldo.setItem(lu, col, QTableWidgetItem(linha['Registro']))
            tabela.tabelaSaldo.setItem(lu, col+1, QTableWidgetItem(str(linha['Valor'])))
            lu+=1

def salvarGastos():
    global df_gastos
    reg = telaGastos.textoRegistro.text()
    valor =telaGastos.textoValor.text()
    setor =telaGastos.comboBox.currentText()
    date = telaGastos.dataRegistro.date().toString()
    novoGasto = [date, reg, valor, setor]
    df = pd.DataFrame([novoGasto], columns=colGastos)
    df_gastos = pd.concat([df_gastos, df], ignore_index=True)
    for index, linha in df_setores.iterrows():
        df_setores.at[index, 'SaldoAtual'] = float(linha['SaldoAtual'])-float(valor)
        print(df_setores.at[index, 'SaldoAtual'])
    attSaldoGastos()
    telaGastos.textoRegistro.clear()
    telaGastos.textoValor.clear()


# df = pd.DataFrame(columns=['Data', 'Registro', 'Valor'. 'NomeSetor'])
# df1 = pd.DataFrame(columns=['NomeSetor', 'Porcentagem', 'SaldoAtual'])
def attContas(janela):
    global df_contasFixas
    custo = []
    new_df = pd.DataFrame(columns=['NomeConta', 'Valor'])
    numRows = janela.listaDeCustos.rowCount()
    for row in range(numRows):
        custo.append(janela.listaDeCustos.item(row, 0).text())
        custo.append(janela.listaDeCustos.item(row, 1).text())
        df = pd.DataFrame([custo], columns=colContas)
        new_df = pd.concat([new_df, df], ignore_index=True)
        print(new_df)
        custo = []
    df_contasFixas = pd.concat([new_df], ignore_index=True)

def attSetor(janela):
    global df_setores
    custo = []
    new_df = pd.DataFrame(columns=colSetor)
    numRows = janela.listaSetor.rowCount()
    for row in range(numRows):
        custo.append(janela.listaSetor.item(row, 0).text())
        custo.append(janela.listaSetor.item(row, 1).text())
        custo.append(janela.listaSetor.item(row, 2).text())
        df = pd.DataFrame([custo], columns=colSetor)
        new_df = pd.concat([new_df, df], ignore_index=True)
        print(new_df)
        custo = []
    df_setores = pd.concat([new_df], ignore_index=True)
    print(df_setores)

def somaPagamento(tabela):
    soma=0
    for i in range(tabela.rowCount()):
        soma += float(tabela.item(i, 1).text())
    novoPagamento.label_Saldo.setText(str(soma))

def moverDados(tabela1, tabela2):
    rowNova = tabela2.rowCount()
    currentRow = tabela1.currentRow()
    tabela2.setRowCount(rowNova+1)
    tabela2.setItem(rowNova, 0, QTableWidgetItem(tabela1.item(currentRow, 0).text()))
    tabela2.setItem(rowNova, 1, QTableWidgetItem(tabela1.item(currentRow, 1).text()))
    tabela1.removeRow(currentRow)
    somaPagamento(tabela2)

def pagar():
#colHist = ['Mes', 'RendaMensal', 'CustoFixoTotal', 'Restante']
    global df_historico
    date = novoPagamento.dateEdit.date().toString()
    datas=[]
    datas = date.split()
    mes = datas[1]
    ano=datas[3]
    rendaMensal = float(novoPagamento.textRendaMensal.text())
    custoFixo = float(novoPagamento.label_Saldo.text())
    dataAtual = mes+' '+ano
    restante = float(rendaMensal-custoFixo)
    print(restante)
    novoHist = [dataAtual, rendaMensal, custoFixo, restante]
    print(novoHist)
    df = pd.DataFrame([novoHist], columns=colHist)
    df_historico = pd.concat([df_historico, df], ignore_index=True)
    print(df_historico)
    atualizarSaldo(restante)

def atualizarSaldo(resto):
    #colSetor = ['NomeSetor', 'Porcentagem', 'SaldoAtual']
    for index, linha in df_setores.iterrows():
        print(index)
        df_setores.at[index, 'SaldoAtual'] = float(linha['SaldoAtual'])+(resto*float(linha['Porcentagem'])/100)
        print(df_setores)

def mostrarSaldo():
    print(df_setores)



#comandos botões----------------------------------------------------
janelaLogin.botaoLogin.clicked.connect(lambda: fecharTelaLogin())

janelaAttContas.botaoVoltarAtt.clicked.connect(lambda: fecharTelaAttContas())
janelaAttContas.botaoAttCusto.clicked.connect(lambda: attContas(janelaAttContas))
janelaAttContas.botaoAttSetores.clicked.connect(lambda: attSetor(janelaAttContas))

novoPagamento.botaoAddOne.clicked.connect(lambda: moverDados(tabela1=novoPagamento.listaDeCustos, tabela2=novoPagamento.tableCustosAdd))
novoPagamento.botaoRemOne.clicked.connect(lambda: moverDados(tabela2=novoPagamento.listaDeCustos, tabela1=novoPagamento.tableCustosAdd))
novoPagamento.botaoPagar.clicked.connect(lambda: pagar())

menuPrincipal.pushButtonNovoCadastro.clicked.connect(lambda: abrirJanelaCadastro())

telaGastos.pushButtonAdd.clicked.connect(lambda: salvarGastos())

menuPrincipal.pushButtonAtualizarDados.clicked.connect(lambda: abrirJanelaAttCusto())
menuPrincipal.pushButtonMostrarSaldo.clicked.connect(lambda: mostrarSaldo())
menuPrincipal.pushButtonAcerto.clicked.connect(lambda: abrirAcerto())

janelaCadastro.botaoVoltar.clicked.connect(lambda: fecharJanelaCadastro())
janelaCadastro.botaoAddNovoCusto.clicked.connect(lambda: addNovoCusto())
janelaCadastro.botaoAddNovoSetor.clicked.connect(lambda: addNovoSetor())

menuPrincipal.pushButtonNovoPagamento.clicked.connect(lambda: abrirJanelaNovoPag())
#--------------------------------------------------------------------------




janelaLogin.show()















try:
    sys.exit(app.exec_())
except:
    print("salvando")
    salvarHistorico()
    salvarSetorCSV()
    salvarGastosCSV()
    salvarContasFixas()

