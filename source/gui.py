import os
import customtkinter
from tkinter import messagebox
import subprocess
import threading  
from utils import selecionar_pasta
from commands import executar_comando
from config_templates import TAILWIND_CONFIG, POSTCSS_CONFIG, APP_CSS_CONTENT, APP_JSX_CONTENT, MAIN_JSX_CONTENT

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.title("Setup - ReactJS + Tailwind CSS")
        self.iconbitmap(os.path.join(BASE_DIR, "assets", "img", "icon.ico"))
        self.geometry("600x400")
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme(os.path.join(BASE_DIR, "assets", "themes", "lavender.json"))
        
        self.resizable(False, False)
        self._initialize_ui()
        self.pasta_selecionada = None

    def _initialize_ui(self):
        """Inicializa a interface do usuário."""
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label_nome_projeto = customtkinter.CTkLabel(self.frame, text="Nome do Projeto:")
        self.label_nome_projeto.pack(pady=(0, 5))

        self.nome_entry = customtkinter.CTkEntry(
            self.frame, 
            placeholder_text="Digite o nome do projeto (sem espaços e com letras minusculas)"
        )
        self.nome_entry.pack(pady=(0, 10), fill="x")

        self.botao_selecionar_diretorio = customtkinter.CTkButton(
            self.frame, 
            text_color="white",
            text="Selecionar Diretório", 
            command=self.on_pasta_selecionada
        )
        self.botao_selecionar_diretorio.pack(pady=(0, 10), fill="x")

        self.botao_criar_projeto = customtkinter.CTkButton(
            self.frame, 
            text_color="white",
            text="Iniciar Criação do Projeto", 
            command=self.iniciar_criacao_projeto  
        )
        self.botao_criar_projeto.pack(pady=(0, 10), fill="x")

        self.log_text = customtkinter.CTkTextbox(self.frame, wrap="word", height=15, width=80)
        self.log_text.pack(pady=10, fill="both", expand=True)

        self.botao_abrir_vscode = customtkinter.CTkButton(
            self.frame, 
            text_color="white",
            text="Abrir projeto no VsCode", 
            command=self.abrir_vscode,
            state='disabled'  
        )
        self.botao_abrir_vscode.pack(pady=(10, 0), fill="x")

        self.label_aviso = customtkinter.CTkLabel(self.frame, text="O projeto será construído com o gerenciador de pacotes 'yarn'")
        self.label_aviso.pack(pady=(10, 0))

    def on_pasta_selecionada(self):
        """Seleciona a pasta onde o projeto será criado.""" 
        self.pasta_selecionada = selecionar_pasta()

    def iniciar_criacao_projeto(self):
        """Inicia a criação do projeto em uma nova thread.""" 
        self.botao_abrir_vscode.configure(state='disabled')  
        thread = threading.Thread(target=self.criar_projeto)
        thread.start()  

    def criar_projeto(self):
        """Cria o projeto e atualiza o Yarn.""" 
        self.log_text.insert("end", "Atualizando o Yarn...\n")
        self._instalar_yarn()
        self.on_criacao_projeto()

    def _instalar_yarn(self):
        """Instala o Yarn globalmente usando npm.""" 
        try:
            comando = "npm install --global yarn"
            self._executar_comando_no_diretorio(comando, None, "Instalando Yarn...")
            self.log_text.insert("end", "Yarn instalado ou atualizado com sucesso!\n")
        except Exception as e:
            self.log_text.insert("end", f"Erro ao instalar o Yarn: {e}\n")

    def on_criacao_projeto(self):
        """Inicia a criação do projeto.""" 
        projeto_dir = self.pasta_selecionada
        nome_projeto = self.nome_entry.get()

        if not projeto_dir or not nome_projeto:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos e selecione um diretório.")
            return

        if not self._criar_diretorio(projeto_dir):
            return

        try:
            self._criar_projeto_vite(projeto_dir, nome_projeto)
            self.log_text.insert("end", "Projeto configurado com sucesso!\n")
            self.botao_abrir_vscode.configure(state='normal')  
        except Exception as e:
            self.log_text.insert("end", f"Erro na criação do projeto: {e}\n")

    def _criar_diretorio(self, projeto_dir):
        """Cria o diretório do projeto, se não existir.""" 
        if not os.path.exists(projeto_dir):
            try:
                os.makedirs(projeto_dir)
                return True
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar o diretório: {e}\n")
                return False
        return True

    def _criar_projeto_vite(self, projeto_dir, nome_projeto):
        """Cria um projeto Vite com o nome e diretório especificados.""" 
        comando = f"yarn create vite {nome_projeto} --template react"
        self._executar_comando_no_diretorio(comando, projeto_dir, "Criando o projeto com Vite...")

        projeto_path = os.path.join(projeto_dir, nome_projeto)
        if not os.path.exists(projeto_path):
            self.log_text.insert("end", f"Diretório do projeto {projeto_path} não encontrado.\n")
            return

        os.chdir(projeto_path)

        self._instalar_dependencias()
        self._inicializar_tailwind_css()
        self._configurar_tailwind_css()
        self._remover_arquivos_desnecessarios()
        self._criar_arquivos_jsx()

    def _executar_comando_no_diretorio(self, comando, cwd, mensagem):
        """Executa um comando em um diretório especificado e atualiza o log.""" 
        self.log_text.insert("end", mensagem + "\n")
        self.update_idletasks()
        executar_comando(comando, cwd=cwd, callback=lambda msg: self.log_text.insert("end", msg + '\n'))

    def _instalar_dependencias(self):
        """Instala as dependências do Tailwind CSS.""" 
        comando = "yarn add -D tailwindcss postcss autoprefixer"
        self._executar_comando_no_diretorio(comando, None, "Instalando dependências do Tailwind CSS...")

    def _inicializar_tailwind_css(self):
        """Inicializa o Tailwind CSS.""" 
        comando = "npx tailwindcss init -p"
        self._executar_comando_no_diretorio(comando, None, "Inicializando Tailwind CSS...")

    def _configurar_tailwind_css(self):
        """Cria os arquivos de configuração do Tailwind CSS.""" 
        try:
            with open("tailwind.config.js", "w") as f:
                f.write(TAILWIND_CONFIG)
            with open("postcss.config.js", "w") as f:
                f.write(POSTCSS_CONFIG)
            with open("src/app.css", "w") as f:
                f.write(APP_CSS_CONTENT)
            self.log_text.insert("end", "Configurações do Tailwind CSS criadas com sucesso.\n")
        except Exception as e:
            self.log_text.insert("end", f"Erro ao criar arquivos de configuração: {e}\n")

    def _remover_arquivos_desnecessarios(self):
        """Remove arquivos desnecessários do projeto.""" 
        arquivos_para_remover = ["README.md", "eslint.config.js"]
        for file_name in arquivos_para_remover:
            self.remover_arquivo(file_name)

        self.remover_arquivo(os.path.join("public", "vite.svg"))
        self.remover_arquivo(os.path.join("src", "assets", "react.svg"))
        self.remover_arquivo(os.path.join("src", "index.css"))

    def _criar_arquivos_jsx(self):
        """Cria os arquivos JSX necessários para o projeto.""" 
        self.criar_arquivo("src/app.jsx", APP_JSX_CONTENT)
        self.criar_arquivo("src/main.jsx", MAIN_JSX_CONTENT)

    def abrir_vscode(self):
        """Abre o projeto no Visual Studio Code.""" 
        if self.pasta_selecionada and self.nome_entry.get():
            try:
                projeto_path = os.path.join(self.pasta_selecionada, self.nome_entry.get())
                subprocess.run(["code", projeto_path], shell=True)
                print(f"Abrindo projeto no VSCode: {projeto_path}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir o projeto no VSCode: {e}")

    def remover_arquivo(self, file_name):
        """Remove o arquivo se existir.""" 
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                self.log_text.insert("end", f"Arquivo {file_name} removido com sucesso.\n")
            except Exception as e:
                self.log_text.insert("end", f"Erro ao remover arquivo {file_name}: {e}\n")

    def criar_arquivo(self, file_name, content):
        """Cria um arquivo com o conteúdo especificado.""" 
        try:
            with open(file_name, "w") as f:
                f.write(content)
            self.log_text.insert("end", f"Arquivo {file_name} criado com sucesso.\n")
        except Exception as e:
            self.log_text.insert("end", f"Erro ao criar arquivo {file_name}: {e}\n")