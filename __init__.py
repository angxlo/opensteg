import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import webbrowser
from ui.py import interfaceStack
from ui.py import popupHideError
from ui.py import popupHideSuccess
from ui.py import popupShowError
from ui.py import popupShowSuccess
from src import steg

# Classe principal da janela
class MainWindow(interfaceStack.Ui_MainWindow):
    def __init__(self):
        # Importa a fonte da logo
        QFontDatabase.addApplicationFont("assets/fonts/good timing bd.ttf")

        # Faz o setup da janela principal
        self.myWindow = QMainWindow()
        self.ui = interfaceStack.Ui_MainWindow()
        self.ui.setupUi(self.myWindow)

        # Define a janela inicial
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)

        # Botões do menu inicial
        self.ui.buttonAccessHide.clicked.connect(self.nextWindow)
        self.ui.buttonAccessShow.clicked.connect(self.accessShowWindow)
        self.ui.buttonGithub.clicked.connect(self.accessGithub)

        # Botões da primeira janela de esteganografia
        self.ui.buttonBrowseFilesInput.clicked.connect(self.browseFilesInput)
        self.ui.buttonGoBackHide1.clicked.connect(self.previousWindow)
        self.ui.buttonGoNextHide1.clicked.connect(self.nextWindow)

        # Botões da segunda janela de esteganografia
        self.ui.buttonGoBackHide2.clicked.connect(self.previousWindow)
        self.ui.buttonSubmitHide2.clicked.connect(self.nextWindow)

        # Botões da terceira janela de esteganografia
        self.ui.buttonBrowseDirectoriesOutput.clicked.connect(self.browseDirectoriesOutput)
        self.ui.buttonGoBackHide3.clicked.connect(self.previousWindow)
        self.ui.buttonDownloadImage.clicked.connect(self.submitHide)

        # Botões da primeira janela de esteganálise
        self.ui.buttonBrowseFilesInput2.clicked.connect(self.browseFilesInput)
        self.ui.buttonSubmitShow1.clicked.connect(self.nextWindow)
        self.ui.buttonGoBackShow1.clicked.connect(self.goBackToMenu)

        # Botões da segunda janela de esteganálise
        self.ui.buttonBrowseDirectoriesOutput2.clicked.connect(self.browseDirectoriesOutput)
        self.ui.buttonGoBackShow2.clicked.connect(self.previousWindow)
        self.ui.buttonDownloadImage2.clicked.connect(self.submitShow)

    # Função que mostra a janela
    def show(self):
        self.myWindow.show()
    
    # Funções que mudam a atual janela da aplicação
    def previousWindow(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()-1)
    def nextWindow(self):
        self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex()+1)
    def goBackToMenu(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.main)
    def accessShowWindow(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.show1)

    # Botão de acesso à página do GitHub do projeto
    def accessGithub(self):
        webbrowser.open('https://github.com/angxlo/tcc-esteganografia')
    
    # Função que abre o explorador de arquivos para selecionar um arquivo
    def browseFilesInput(self):
        fileName = QFileDialog.getOpenFileName()
        # Verifica se o processo sendo realizado é a esteganografia ou a esteganálise (por meio da janela atual) para mudar a variável correspondente
        if (self.ui.stackedWidget.currentIndex() == 1): 
            self.ui.imageDirectoryInput.setText(fileName[0])
        else:
            self.ui.imageDirectoryInput2.setText(fileName[0])
    # Função que abre o explorador de arquivos para selecionar um diretório
    def browseDirectoriesOutput(self):
        directoryName = QFileDialog.getExistingDirectory()
        # Verifica se o processo sendo realizado é a esteganografia ou a esteganálise (por meio da janela atual) para mudar a variável correspondente
        if (self.ui.stackedWidget.currentIndex() == 3):
            self.ui.imageDirectoryOutput.setText(directoryName)
        else:
            self.ui.imageDirectoryOutput2.setText(directoryName)

    # Submete o arquivo para a esteganografia
    def submitHide(self):
        # Obtém os valores dos subpixels a serem editados
        if self.ui.subpixelSelectorComboBox.currentText() == "RGB":
            step = 4
        elif self.ui.subpixelSelectorComboBox.currentText() == "R":
            step = 1
        elif self.ui.subpixelSelectorComboBox.currentText() == "G":
            step = 2
        elif self.ui.subpixelSelectorComboBox.currentText() == "B":
            step = 3

        # Concatena o diretório em que o arquivo será salvo com o nome do mesmo e adiciona o formato ao final do nome do arquivo
        outArch = self.ui.imageDirectoryOutput.text()+"/"+self.ui.imageNameOutput.text()+".png"

        # Caso o algoritmo suceda em ocultar a mensagem, informa o usuário. Caso contrário, imprime uma mensagem de erro
        try:
            steg.hide(self.ui.imageDirectoryInput.text(), self.ui.messageInput.toPlainText(), outArch, step)
            self.showPopupSuccessHide()
        except:
            self.showPopupErrorHide()
    
    # Submete o arquivo para a esteganálise
    def submitShow(self):
        if self.ui.subpixelSelectorComboBox2.currentText() == "RGB":
            step = 4
        elif self.ui.subpixelSelectorComboBox2.currentText() == "R":
            step = 1
        elif self.ui.subpixelSelectorComboBox2.currentText() == "G":
            step = 2
        elif self.ui.subpixelSelectorComboBox2.currentText() == "B":
            step = 3

        # Concatena o diretório em que o texto será salvo com o nome do mesmo
        outArch = self.ui.imageDirectoryOutput2.text()+"/"+self.ui.textNameOutput.text()

        # Caso o algoritmo suceda em encontrar alguma mensagem, informa o usuário. Caso contrário, imprime uma mensagem dizendo que, com as atuais configurações, nada foi encontradfo
        if steg.show(self.ui.imageDirectoryInput2.text(), step, outArch) == "nomessage":
            self.showPopupErrorShow()
        else:
            self.showPopupSuccessShow()

    # Funções encarregadas de mostrar os pop-ups relacionados à esteganografia
    def showPopupErrorHide(self):
        self.windowPopupErrorHide = QMainWindow()
        self.uiPopupErrorHide = popupHideError.Ui_popupHideError()
        self.uiPopupErrorHide.setupUi(self.windowPopupErrorHide)
        self.windowPopupErrorHide.show()
    def showPopupSuccessHide(self):
        self.windowPopupSuccessHide = QDialog()
        self.uiPopupSuccessHide = popupHideSuccess.Ui_popupHideSuccess()
        self.uiPopupSuccessHide.setupUi(self.windowPopupSuccessHide)
        self.windowPopupSuccessHide.show()
    
    # Funções encarregadas de mostrar os pop-ups relacionados à esteganálise
    def showPopupErrorShow(self):
        self.windowPopupErrorShow = QMainWindow()
        self.uiPopupErrorShow = popupShowError.Ui_popupShowError()
        self.uiPopupErrorShow.setupUi(self.windowPopupErrorShow)
        self.windowPopupErrorShow.show()
    def showPopupSuccessShow(self):
        self.windowPopupSuccessShow = QDialog()
        self.uiPopupSuccessShow = popupShowSuccess.Ui_popupShowSuccess()
        self.uiPopupSuccessShow.setupUi(self.windowPopupSuccessShow)
        self.windowPopupSuccessShow.show()

# Classe main, executa a aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    sys.exit(app.exec_())