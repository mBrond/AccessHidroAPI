from tkinter import *
from tkinter import PhotoImage, filedialog, scrolledtext, messagebox
from tkcalendar import Calendar, DateEntry
import manipulacaoArquivos
from gerenciador import solicitar_estacoes

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

        self.root.title(titulo)
        self.root.configure(bg=BG_COLOR)

        # Carregar e exibir o logo
        self.carregar_logo()

        # Frame principal
        main_frame = Frame(self.root, bg=BG_COLOR)
        main_frame.pack(pady=20)

        # Botões
        Button(main_frame, text="Atualizar credenciais", command=self.interface_atualizar_credenciais, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)
        Button(main_frame, text="Atualizar estações", command=self.interface_atualizar_estacoes, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)

        # Radiobuttons
        Label(main_frame, text="Selecione o tipo:", bg=BG_COLOR).pack(anchor='w', padx=10)
        Radiobutton(main_frame, text="Telemétricas Adotadas", variable=self.tipo, value="Adotada", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Telemétricas Detalhadas", variable=self.tipo, value="Detalhada", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Chuva", variable=self.tipo, value="Chuva", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Cota", variable=self.tipo, value="Cota", bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(main_frame, text="Convencionais de Sedimentos", variable=self.tipo, value="Sedimentos", bg=BG_COLOR).pack(anchor='w', padx=20)

        Button(main_frame, text="Baixar estacoes", command=self.interface_baixar_estacoes, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=5, padx=10, fill=X)

    def carregar_logo(self):
        try:
            logo = PhotoImage(file="img/Logo.png")  # Substitua pelo caminho correto do seu logo
            logo_label = Label(self.root, image=logo, bg=BG_COLOR)
            logo_label.image = logo  # Manter uma referência da imagem
            logo_label.pack(pady=10)  # Adiciona o logo ao topo da janela
        except Exception as e:
            print("Erro ao carregar logo:", e)

    def visualizar_estacoes(self):
        try:
            # Lê as estações do arquivo, removendo linhas vazias e quebras de linha
            with open(self.pathEstacoes, 'r') as arq:
                linhas = [linha.strip() for linha in arq if linha.strip()]

            janela_conteudo = Toplevel(self.root)
            janela_conteudo.title("Estações para download")
            janela_conteudo.geometry("400x500")

            # Frame para os checkboxes
            frame_checks = Frame(janela_conteudo)
            frame_checks.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Listas para guardar as variáveis e as linhas
            vars_checks = []
            for linha in linhas:
                var = BooleanVar()
                chk = Checkbutton(frame_checks, text=linha, variable=var, anchor='w')
                chk.pack(fill='x', anchor='w')
                vars_checks.append((var, linha))

            def remover_estacoes():
                # Filtra as estações não marcadas
                novas_linhas = [linha for var, linha in vars_checks if not var.get()]
                # Atualiza o arquivo
                with open(self.pathEstacoes, 'w') as arq:
                    for linha in novas_linhas:
                        arq.write(linha + '\n')
                # Fecha a janela e mostra mensagem
                janela_conteudo.destroy()
                messagebox.showinfo("Sucesso", "Estações removidas com sucesso!")

            btn_remover = Button(janela_conteudo, text="Remover selecionadas", command=remover_estacoes, bg="#f44336", fg="white")
            btn_remover.pack(pady=5)

            btn_fechar = Button(janela_conteudo, text="Fechar", command=janela_conteudo.destroy, bg="#888888", fg="white")
            btn_fechar.pack(pady=5)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo de estações:\n{str(e)}")

    def interface_atualizar_credenciais(self):
        def submitCredenciais():
            dados = {'id': entryLogin.get(), 'senha': entrySenha.get()}
            manipulacaoArquivos.atualiza_credenciais_ana(self.pathConfigs, dados)
            messagebox.showinfo("Sucesso", "Credenciais atualizadas!")

        novaJanela = Toplevel(self.root)
        novaJanela.title("Atualizando credenciais")
        novaJanela.geometry("300x200")
        novaJanela.configure(bg=BG_COLOR)

        Label(novaJanela, text="Novo login:", bg=BG_COLOR).pack(pady=5)
        entryLogin = Entry(novaJanela, width=30)
        entryLogin.pack(pady=5)

        Label(novaJanela, text="Nova senha:", bg=BG_COLOR).pack(pady=5)
        entrySenha = Entry(novaJanela, show='*', width=30)
        entrySenha.pack(pady=5)

        Button(novaJanela, text="Confirmar", command=submitCredenciais, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)
        Button(novaJanela, text="Voltar", command=novaJanela.destroy, bg="#f44336", fg="white").pack(pady=5)

    def interface_atualizar_estacoes(self):
        novaJanela = Toplevel(self.root)
        novaJanela.title("Atualizando estações")
        novaJanela.geometry("400x400")
        novaJanela.configure(bg=BG_COLOR)

        Button(novaJanela, text="Visualizar estações", command=self.visualizar_estacoes, bg="#2196F3", fg="white").pack(pady=10)

        Label(novaJanela, text="Escolha uma opção:", bg=BG_COLOR).pack(pady=5)
        sobreeescrever = BooleanVar(value=True)
        Radiobutton(novaJanela, text="Sobreescrever estações", variable=sobreeescrever, value=True, bg=BG_COLOR).pack(anchor='w', padx=20)
        Radiobutton(novaJanela, text="Adicionar estações", variable=sobreeescrever, value=False, bg=BG_COLOR).pack(anchor='w', padx=20)

        Label(novaJanela, text="Insira as novas estações (uma por linha):", bg=BG_COLOR).pack(pady=5)
        text_area = scrolledtext.ScrolledText(novaJanela, width=40, height=10)
        text_area.pack(pady=5)

        def update_file():
            # Lê as estações já existentes
            final = set()
            existentes = set()
            novas = set()

            try:
                with open(self.pathEstacoes, 'r') as f:
                    existentes = set(linha.strip() for linha in f if linha.strip())
            except FileNotFoundError:
                existentes = set()

            for linha in text_area.get("1.0", END).splitlines():
                valor = linha.strip()
                if valor and valor.isdigit():
                    novas.add(valor) # Adiciona ao conjunto apenas se for número

            if not novas:
                messagebox.showwarning("Aviso", "Nenhuma estação inserida!")
                return

            total_linhas = len([linha for linha in text_area.get("1.0", END).splitlines() if linha.strip()])
            if len(novas) < total_linhas:
                messagebox.showinfo("Atenção", "Estações não numéricas foram ignoradas!")

            if sobreeescrever.get():
                final = novas
            else:
                final = existentes | novas  # União, evita duplicidade, 

            manipulacaoArquivos.escreverEstacoes(self.pathEstacoes, 1, list(final))
    

            text_area.delete("1.0", END)
            messagebox.showinfo("Sucesso", "Estações atualizadas!")

        Button(novaJanela, text="Atualizar", command=update_file, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)
        Button(novaJanela, text="Fechar", command=novaJanela.destroy, bg="#888888", fg="white").pack(pady=5)

    def interface_baixar_estacoes(self):
        novaJanela = Toplevel(self.root)
        novaJanela.title("Baixando")
        novaJanela.geometry("300x200")
        novaJanela.configure(bg=BG_COLOR)

        Label(novaJanela, text="Data de início:", bg=BG_COLOR).pack(pady=5)
        calendarioComeco = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioComeco.pack(pady=5)

        Label(novaJanela, text="Data de fim:", bg=BG_COLOR).pack(pady=5)
        calendarioFinal = DateEntry(novaJanela, date_pattern='yyyy-mm-dd')
        calendarioFinal.pack(pady=5)

        def solicitar_estacao():
            dataComeco = calendarioComeco.get()
            dataFinal = calendarioFinal.get()
            solicitar_estacoes(dataComeco, dataFinal, self.pathEstacoes, self.pathConfigs, self.tipo.get(), self.qtdDownloadAsync)

        Button(novaJanela, text="Confirmar", command=solicitar_estacao, bg=BTN_COLOR, fg=BTN_TEXT_COLOR).pack(pady=10)

if __name__ == "__main__":
    pass
