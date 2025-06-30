from tkinter import *
from tkinter import PhotoImage, filedialog, scrolledtext, messagebox
from tkcalendar import DateEntry
import manipulacaoArquivos
from gerenciador import solicitar_estacoes

class Application:
    def __init__(self, root, versaoSoftware, pathConfigs, pathResults, pathEstacoes, titulo, qtdDownloadAsync):
        self.root = root
        self.versaoSoftware = versaoSoftware
        self.pathConfigs = pathConfigs
        self.pathResults = pathResults
        self.pathEstacoes = pathEstacoes
        self.qtdDownloadAsync = qtdDownloadAsync

        self.tipo = StringVar()
        self.tipo.set("Adotada")

        self.root.title(titulo)
        self.root.configure(bg="#DFF9CA")

        # Carregar e exibir o logo
        self.load_logo()

        # Frame principal
        main_frame = Frame(self.root, bg="#DFF9CA")
        main_frame.pack(pady=20)

        # Botões
        Button(main_frame, text="Atualizar credenciais", command=self.interface_atualizar_credenciais, bg="#4CAF50", fg="white").pack(pady=5, padx=10, fill=X)
        Button(main_frame, text="Atualizar estações", command=self.interface_atulizar_estacoes, bg="#4CAF50", fg="white").pack(pady=5, padx=10, fill=X)

        # Radiobuttons
        Label(main_frame, text="Selecione o tipo:", bg="#DFF9CA").pack(anchor='w', padx=10)
        Radiobutton(main_frame, text="Telemétricas Adotadas", variable=self.tipo, value="Adotada", bg="#DFF9CA").pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Telemétricas Detalhadas", variable=self.tipo, value="Detalhada", bg="#DFF9CA").pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Chuva", variable=self.tipo, value="Chuva", bg="#DFF9CA").pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Cota", variable=self.tipo, value="Cota", bg="#DFF9CA").pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Sedimentos", variable=self.tipo, value="Sedimentos", bg="#DFF9CA").pack(anchor='w', padx=20)

        Button(main_frame, text="Baixar estacoes", command=self.interface_baixar_estacoes, bg="#4CAF50", fg="white").pack(pady=5, padx=10, fill=X)

    def load_logo(self):
        try:
            logo = PhotoImage(file="img/Logo.png")  # Substitua pelo caminho correto do seu logo
            logo_label = Label(self.root, image=logo, bg="#DFF9CA")
            logo_label.image = logo  # Manter uma referência da imagem
            logo_label.pack(pady=10)  # Adiciona o logo ao topo da janela
        except Exception as e:
            print("Erro ao carregar logo:", e)

    def visualizar_estacoes(self):
        try:
            with open(self.pathEstacoes, 'r') as arq:
                linhas = arq.readlines()

            janela_conteudo = Toplevel(self.root)
            janela_conteudo.title("Estações para download")
            janela_conteudo.geometry("400x400")

            text_area = scrolledtext.ScrolledText(janela_conteudo, wrap=WORD, width=80, height=30)
            text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)

            for linha in linhas:
                text_area.insert(END, linha)

            text_area.config(state=DISABLED)

            btn_fechar = Button(janela_conteudo, text="Fechar", command=janela_conteudo.destroy, bg="#f44336", fg="white")
            btn_fechar.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo de estações:\n{str(e)}")

    def interface_atualizar_credenciais(self):
        def submitCredenciais():
            dados = {'id': entryLogin.get(), 'senha': entrySenha.get()}
            manipulacaoArquivos.atualiza_credenciais_ana(self.pathConfigs, dados)

        novaJanela = Toplevel(self.root)
        novaJanela.title("Atualizando credenciais")
        novaJanela.geometry("300x200")
        novaJanela.configure(bg="#DFF9CA")

        Label(novaJanela, text="Novo login:", bg="#DFF9CA").pack(pady=5)
        entryLogin = Entry(novaJanela, width=30)
        entryLogin.pack(pady=5)

        Label(novaJanela, text="Nova senha:", bg="#DFF9CA").pack(pady=5)
        entrySenha = Entry(novaJanela, show='*', width=30)
        entrySenha.pack(pady=5)

        Button(novaJanela, text="Confirmar", command=submitCredenciais, bg="#4CAF50", fg="white").pack(pady=10)
        Button(novaJanela, text="Voltar", command=novaJanela.destroy, bg="#f44336", fg="white").pack(pady=5)

    def interface_atulizar_estacoes(self):
        novaJanela = Toplevel(self.root)
        novaJanela.title("Atualizando estacoes")
        novaJanela.geometry("300x300")
        novaJanela.configure(bg="#DFF9CA")

        # Botão para visualizar estações
        Button(novaJanela, text="Visualizar estações", command=self.visualizar_estacoes, bg="#2196F3", fg="white").pack(pady=10)

        Label(novaJanela, text="Escolha uma opção:", bg="#DFF9CA").pack(pady=5)
        sobreeescrever = BooleanVar(value=True)
        Radiobutton(novaJanela, text="Sobreescrever estações", variable=sobreeescrever, value=True, bg="#DFF9CA").pack(anchor='w', padx=20)
        Radiobutton(novaJanela, text="Adicionar estações", variable=sobreeescrever, value=False, bg="#DFF9CA").pack(anchor='w', padx=20)

        entries = []

        def add_input():
            entry = Entry(novaJanela, width=30)
            entry.pack(pady=5)
            entries.append(entry)

        def update_file():
            modo = 'w' if sobreeescrever.get() else 'a'  
            with open(self.pathEstacoes, modo) as f:
                for entry in entries:
                    f.write(entry.get()+'\n')
            entries.clear()

        Button(novaJanela, text="Nova entrada", command=add_input, bg="#4CAF50", fg="white").pack(pady=10)
        Button(novaJanela, text="Atualizar", command=update_file, bg="#4CAF50", fg="white").pack(pady=5)

    def interface_baixar_estacoes(self):
        novaJanela = Toplevel(self.root)
        novaJanela.title("Baixando")
        novaJanela.geometry("300x200")
        novaJanela.configure(bg="#DFF9CA")

        Label(novaJanela, text="Data de início:", bg="#DFF9CA").pack(pady=5)
        calendarioComeco = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioComeco.pack(pady=5)

        Label(novaJanela, text="Data de fim:", bg="#DFF9CA").pack(pady=5)
        calendarioFinal = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioFinal.pack(pady=5)

        def solicitar_estacao():
            dataComeco = calendarioComeco.get()
            dataFinal = calendarioFinal.get()
            solicitar_estacoes(dataComeco, dataFinal, self.pathEstacoes, self.pathConfigs, self.tipo.get(), self.qtdDownloadAsync)

        Button(novaJanela, text="Confirmar", command=solicitar_estacao, bg="#4CAF50", fg="white").pack(pady=10)

if __name__ == "__main__":
    pass
