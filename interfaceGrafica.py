from tkinter import *
from tkinter import PhotoImage
from tkinter import filedialog
from tkcalendar import DateEntry

import manipulacaoArquivos
import main



class Application:
    def __init__(self, root, versaoSoftware, pathConfigs, pathResults, pathEstacoes, titulo):
        self.root = root
        self.versaoSoftware = versaoSoftware
        self.pathConfigs = pathConfigs
        self.pathResults = pathResults
        self.pathEstacoes = pathEstacoes

        self.tipo = StringVar()  # Changed to StringVar()

        self.root.title(titulo)
        self.root.configure(bg="#DFF9CA")

        try:
            icone = PhotoImage(file="img/Logo.png")  # Substitua pelo seu caminho
            self.root.iconphoto(True, icone)
        except Exception as e:
            print("Erro ao carregar ícone:", e)

        Button(self.root, text="Atualizar credenciais", command=self.interface_atualizar_credenciais).pack(anchor='w')
        Button(self.root, text="Atualizar estacoes", command=self.interface_atulizar_estacoes).pack(anchor='w')

        Radiobutton(self.root, text="Telemétricas Adotadas", variable=self.tipo, value="Adotada").pack(anchor='w')
        Radiobutton(self.root, text="Telemétricas Detalhadas", variable=self.tipo, value="Detalhada").pack(anchor='w')
        Radiobutton(self.root, text="Convencionais de Chuva", variable=self.tipo, value="Chuva").pack(anchor='w')
        Radiobutton(self.root, text="Convencionas de Cota", variable=self.tipo, value="Cota").pack(anchor='w')
        Radiobutton(self.root, text="Convencionais de Sendimentos", variable=self.tipo, value="Sedimentos").pack(anchor='w')

        Button(self.root, text="Baixar estacoes", command=self.interface_baixar_estacoes).pack(anchor='w')

    def interface_atualizar_credenciais(self):

        def submitCredenciais():
            dados = {'id': entryLogin.get(), 'senha': entrySenha.get()}

            manipulacaoArquivos.atualiza_credenciais_ana(self.pathConfigs, dados)

        novaJanela = Toplevel(self.root)
        novaJanela.title("Atulizando credenciais")
        novaJanela.geometry("250x150")
        novaJanela.configure(bg="#DFF9CA")

        Label(novaJanela, text="Enter something:").pack(pady=5)
        entryLogin = Entry(novaJanela, text="Novo login: ", width=30)
        entryLogin.pack()
        entrySenha = Entry(novaJanela, text="Nova senha ", width=30)
        entrySenha.pack()


        Button(novaJanela, text="Confirmar", command=submitCredenciais).pack()
        Button(novaJanela, text="Voltar", command=novaJanela.destroy).pack()
        
    
    def interface_atulizar_estacoes(self):
        novaJanela = Toplevel(self.root)
        novaJanela.title("Atualizando estacoes")
        novaJanela.geometry("250x150")
        novaJanela.configure(bg="#DFF9CA")
        sobreescrever = True

        Button(novaJanela, text="Visualizar estações").pack()#ler arquivo de estações, e mostrar em nova janela os códigos
        
        Radiobutton(novaJanela, text="Sobreescrever estações", variable=sobreescrever, value=True).pack()
        Radiobutton(novaJanela, text="Adicionar estações", variable=sobreescrever, value=False).pack()

        entries = list()

        def add_input():
            entry = Entry(novaJanela, width=30).pack()
            entries.append(entry)

        Button(novaJanela, text="Nova entrada", command=add_input).pack()
        Button(novaJanela, text="Atualizar").pack()

        def select_file():
            filePath = filedialog.askopenfile(
                title="Selecione um arquivo", 
                filetypes=[("Text files", "*.txt")]
            )

        Button(novaJanela, text="Selecionar arquivo", command=select_file).pack()


    def interface_baixar_estacoes(self):
        novaJanela = Toplevel(root)
        novaJanela.title("Baixando")
        novaJanela.geometry("250x150")
        novaJanela.configure(bg="#DFF9CA")

        calendarioComeco = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioComeco.pack()

        calendarioFinal = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioFinal.pack()

        def solicitar_estacao():
            dataComeco = calendarioComeco.get()
            dataFinal = calendarioFinal.get()

            main.solicitar_estacoes(dataComeco, dataFinal, self.pathEstacoes, self.pathConfigs, self.tipo.get())

        Button(novaJanela, text="Confirmar", command=solicitar_estacao).pack()


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")  # Tamanho da janela
    app = Application(root, "1.0", "configs.json", "resultados/", "estacoes.txt","AHAPI")
    root.mainloop()
