from tkinter import *
from tkinter import PhotoImage, scrolledtext, messagebox
from tkcalendar import DateEntry
import manipulacaoArquivos
from gerenciador import solicitar_estacoes
import os

BG_COLOR = "#DFF9CA"
BTN_COLOR = "#4CAF50"
BTN_TEXT_COLOR = "white"

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
        
        # Para rastrear a janela atual
        self.janela_atual = None

        self.root.title(titulo)
        self.root.configure(bg=BG_COLOR)

        self.carregar_logo()

        mainFrame = Frame(self.root, bg=BG_COLOR)
        mainFrame.pack(pady=20)

        Button(mainFrame, text="Atualizar credenciais", command=self.interface_atualizar_credenciais, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)
        Button(mainFrame, text="Atualizar estações", command=self.interface_atualizar_estacoes, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)

        Label(mainFrame, text="Selecione o tipo:", bg=BG_COLOR).pack(anchor='w', padx=10)
        Radiobutton(mainFrame, text="Telemétricas Adotadas", variable=self.tipo, value="Adotada", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(mainFrame, text="Telemétricas Detalhadas", variable=self.tipo, value="Detalhada", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(mainFrame, text="Convencionais de Chuva", variable=self.tipo, value="Chuva", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(mainFrame, text="Convencionais de Cota", variable=self.tipo, value="Cota", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(mainFrame, text="Convencionais de Sedimentos", variable=self.tipo, value="Sedimentos", bg=BG_COLOR).pack(anchor='w', padx=20)

        Button(mainFrame, text="Baixar estacoes", command=self.interface_baixar_estacoes, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)

    def carregar_logo(self):
        caminhoLogo = os.path.join(os.path.dirname(__file__), "img", "Logo.png")
        try:
            logoImg = PhotoImage(file=caminhoLogo)
            logoLabel = Label(self.root, image=logoImg, bg=BG_COLOR)
            logoLabel.image = logoImg
            logoLabel.pack(pady=10)
        except Exception as erro:
            print("Erro ao carregar logo:", erro)

    def visualizar_estacoes(self):
        try:
            with open(self.pathEstacoes, 'r') as arquivo:
                linhasEstacoes = [linha.strip() for linha in arquivo if linha.strip()]

            janelaEstacoes = Toplevel(self.root)
            janelaEstacoes.title("Estações para download")
            janelaEstacoes.geometry("400x500")
            janelaEstacoes.transient(self.root)
            janelaEstacoes.grab_set()

            frameChecks = Frame(janelaEstacoes)
            frameChecks.pack(fill=BOTH, expand=True, padx=10, pady=10)

            checkVars = []
            for linha in linhasEstacoes:
                var = BooleanVar()
                check = Checkbutton(frameChecks, text=linha, variable=var, anchor='w')
                check.pack(fill='x', anchor='w')
                checkVars.append((var, linha))

            def remover_estacoes():
                novasLinhas = [linha for var, linha in checkVars if not var.get()]
                with open(self.pathEstacoes, 'w') as arquivo:
                    for linha in novasLinhas:
                        arquivo.write(linha + '\n')
                janelaEstacoes.destroy()
                self.janela_atual = None  # Limpa a referência
                messagebox.showinfo("Sucesso", "Estações removidas com sucesso!")

            def fechar_janela_estacoes():
                janelaEstacoes.destroy()
                self.janela_atual = None

            Button(janelaEstacoes, text="Remover selecionadas", command=remover_estacoes, bg="#f44336", fg="white").pack(pady=5)
            Button(janelaEstacoes, text="Fechar", command=fechar_janela_estacoes, bg="#888888", fg="white").pack(pady=5)

        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo de estações:\n{str(erro)}")

    def interface_atualizar_credenciais(self):
        
        def confirmar_credenciais():
            dados = {'id': loginEntry.get(), 'senha': senhaEntry.get()}
            manipulacaoArquivos.atualiza_credenciais_ana(self.pathConfigs, dados)
            messagebox.showinfo("Sucesso", "Credenciais atualizadas!")

        def fechar_janela_credenciais():
            janelaCredenciais.destroy()
            self.janela_atual = None

        janelaCredenciais = Toplevel(self.root)
        self.janela_atual = janelaCredenciais  # Atualiza referência
        janelaCredenciais.title("Atualizando credenciais")
        janelaCredenciais.geometry("300x200")
        janelaCredenciais.configure(bg=BG_COLOR)
        janelaCredenciais.transient(self.root)
        janelaCredenciais.grab_set()

        Label(janelaCredenciais, text="Novo login:", bg=BG_COLOR).pack(pady=5)
        loginEntry = Entry(janelaCredenciais, width=30)
        loginEntry.pack(pady=5)

        Label(janelaCredenciais, text="Nova senha:", bg=BG_COLOR).pack(pady=5)
        senhaEntry = Entry(janelaCredenciais, show='*', width=30)
        senhaEntry.pack(pady=5)

        Button(janelaCredenciais, text="Confirmar", command=confirmar_credenciais, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)
        Button(janelaCredenciais, text="Voltar", command=fechar_janela_credenciais, bg="#f44336", fg="white").pack(pady=5)

    def interface_atualizar_estacoes(self):
        
        janelaAtualizar = Toplevel(self.root)
        self.janela_atual = janelaAtualizar  # Atualiza referência
        janelaAtualizar.title("Atualizando estações")
        janelaAtualizar.geometry("400x400")
        janelaAtualizar.configure(bg=BG_COLOR)
        janelaAtualizar.transient(self.root)
        janelaAtualizar.grab_set()

        Button(janelaAtualizar, text="Visualizar estações", command=self.visualizar_estacoes, bg="#2196F3", fg="white").pack(pady=10)

        Label(janelaAtualizar, text="Escolha uma opção:", bg=BG_COLOR).pack(pady=5)
        sobrescreverVar = BooleanVar(value=True)
        Radiobutton(janelaAtualizar, text="Sobreescrever estações", variable=sobrescreverVar, value=True, bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(janelaAtualizar, text="Adicionar estações", variable=sobrescreverVar, value=False, bg=BG_COLOR).pack(anchor='w', padx=20)

        Label(janelaAtualizar, text="Insira as novas estações (uma por linha):", bg=BG_COLOR).pack(pady=5)
        textArea = scrolledtext.ScrolledText(janelaAtualizar, width=40, height=10)
        textArea.pack(pady=5)

        def atualizar_arquivo_estacoes():
            estacoesFinais = set()
            estacoesExistentes = set()
            estacoesNovas = set()

            try:
                with open(self.pathEstacoes, 'r') as arquivo:
                    estacoesExistentes = set(linha.strip() for linha in arquivo if linha.strip())
            except FileNotFoundError:
                estacoesExistentes = set()

            for linha in textArea.get("1.0", END).splitlines():
                valor = linha.strip()
                if valor and valor.isdigit():
                    estacoesNovas.add(valor)

            if not estacoesNovas:
                messagebox.showwarning("Aviso", "Nenhuma estação inserida!")
                return

            totalInseridas = len([linha for linha in textArea.get("1.0", END).splitlines() if linha.strip()])
            if len(estacoesNovas) < totalInseridas:
                messagebox.showinfo("Atenção", "Estações não numéricas foram ignoradas!")

            if sobrescreverVar.get():
                estacoesFinais = estacoesNovas
            else:
                estacoesFinais = estacoesExistentes | estacoesNovas

            manipulacaoArquivos.escrever_estacoes(self.pathEstacoes, 1, list(estacoesFinais))

            textArea.delete("1.0", END)
            messagebox.showinfo("Sucesso", "Estações atualizadas!")

        def fechar_janela_atualizar():
            janelaAtualizar.destroy()
            self.janela_atual = None

        Button(janelaAtualizar, text="Atualizar", command=atualizar_arquivo_estacoes, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)
        Button(janelaAtualizar, text="Fechar", command=fechar_janela_atualizar, bg="#888888", fg="white").pack(pady=5)

    def interface_baixar_estacoes(self):
        
        janelaBaixar = Toplevel(self.root)
        self.janela_atual = janelaBaixar  # Atualiza referência
        janelaBaixar.title("Baixando")
        janelaBaixar.geometry("300x200")
        janelaBaixar.configure(bg=BG_COLOR)
        janelaBaixar.transient(self.root)
        janelaBaixar.grab_set()

        Label(janelaBaixar, text="Data de início:", bg=BG_COLOR).pack(pady=5)
        calendarioInicio = DateEntry(janelaBaixar, date_pattern='yyyy-mm-dd')
        calendarioInicio.pack(pady=5)

        Label(janelaBaixar, text="Data de fim:", bg=BG_COLOR).pack(pady=5)
        calendarioFim = DateEntry(janelaBaixar, date_pattern='yyyy-mm-dd')
        calendarioFim.pack(pady=5)

        def solicitar_estacao():
            dataInicio = calendarioInicio.get()
            dataFim = calendarioFim.get()
            solicitar_estacoes(dataInicio, dataFim, self.pathEstacoes, self.pathConfigs, self.tipo.get(), self.qtdDownloadAsync)

        def fechar_janela_baixar():
            janelaBaixar.destroy()
            self.janela_atual = None

        Button(janelaBaixar, text="Confirmar", command=solicitar_estacao, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)
        Button(janelaBaixar, text="Fechar", command=fechar_janela_baixar, bg="#888888", fg="white").pack(pady=5)