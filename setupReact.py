import subprocess
import os
import customtkinter
from tkinter import filedialog, messagebox

def executar_comando(comando, cwd=None, callback=None):
    try:
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        if callback:
            callback(f"Comando executado com sucesso: {comando}\nSaída:\n{resultado.stdout}")
    except subprocess.CalledProcessError as e:
        if callback:
            callback(f"Erro ao executar o comando: {comando}\nSaída de erro:\n{e.stderr}")
        raise  

def selecionar_pasta():
    root = customtkinter.CTk()
    root.withdraw()  
    pasta = filedialog.askdirectory(title="Selecione o diretório onde o projeto será criado")
    root.destroy()
    return pasta

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela principal
        self.title("Criador de Projeto React com Tailwind")
        self.geometry("600x400")

        # Configuração do estilo
        customtkinter.set_appearance_mode("Dark")  
        customtkinter.set_default_color_theme("dark-blue")  

        # Configuração do layout
        self.frame = customtkinter.CTkFrame(self)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.label_nome_projeto = customtkinter.CTkLabel(self.frame, text="Nome do Projeto:")
        self.label_nome_projeto.pack(pady=(0, 5))

        self.nome_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Digite o nome do projeto (sem espaços e com letras minusculas)")
        self.nome_entry.pack(pady=(0, 10), fill="x")

        self.botao_selecionar_diretorio = customtkinter.CTkButton(self.frame, text="Selecionar Diretório", command=self.on_pasta_selecionada)
        self.botao_selecionar_diretorio.pack(pady=(0, 10), fill="x")

        self.botao_criar_projeto = customtkinter.CTkButton(self.frame, text="Iniciar Criação do Projeto", command=self.on_criacao_projeto)
        self.botao_criar_projeto.pack(pady=(0, 10), fill="x")

        self.log_text = customtkinter.CTkTextbox(self.frame, wrap="word", height=15, width=80)
        self.log_text.pack(pady=10, fill="both", expand=True)

        # Variável global para armazenar o caminho selecionado
        self.pasta_selecionada = None

    def on_pasta_selecionada(self):
        self.pasta_selecionada = selecionar_pasta()

    def on_criacao_projeto(self):
        projeto_dir = self.pasta_selecionada
        nome_projeto = self.nome_entry.get()

        if not projeto_dir or not nome_projeto:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos e selecione um diretório.")
            return

        if not os.path.exists(projeto_dir):
            try:
                os.makedirs(projeto_dir)
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar o diretório: {e}\n")
                return

        try:
            comando = f"yarn create vite {nome_projeto} --template react"
            self.log_text.insert("end", "Criando o projeto com Vite...\n")
            self.update_idletasks()
            executar_comando(comando, cwd=projeto_dir, callback=lambda msg: self.log_text.insert("end", msg + '\n'))

            projeto_path = os.path.join(projeto_dir, nome_projeto)
            if not os.path.exists(projeto_path):
                self.log_text.insert("end", f"Diretório do projeto {projeto_path} não encontrado.\n")
                return

            os.chdir(projeto_path)

            comando = "yarn add -D tailwindcss postcss autoprefixer"
            self.log_text.insert("end", "Instalando dependências do Tailwind CSS...\n")
            self.update_idletasks()
            executar_comando(comando, callback=lambda msg: self.log_text.insert("end", msg + '\n'))

            comando = "npx tailwindcss init -p"
            self.log_text.insert("end", "Inicializando Tailwind CSS...\n")
            self.update_idletasks()
            executar_comando(comando, callback=lambda msg: self.log_text.insert("end", msg + '\n'))

            self.log_text.insert("end", "Configurando o Tailwind CSS...\n")
            self.update_idletasks()

            tailwind_config = """/** @type {import('tailwindcss').Config} */
            export default {
                content: [
                    "./index.html",
                    "./src/**/*.{js,ts,jsx,tsx}",
                ],
                theme: {
                    extend: {},
                },
                plugins: [],
            };"""

            postcss_config = """/** @type {import('postcss').ProcessOptions} */
            export default {
                plugins: {
                    tailwindcss: {},
                    autoprefixer: {},
                },
            };"""

            try:
                with open("tailwind.config.js", "w") as f:
                    f.write(tailwind_config)
                with open("postcss.config.js", "w") as f:
                    f.write(postcss_config)
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar arquivos de configuração: {e}\n")
                return

            app_css_file = "src/app.css"
            css_content = """@tailwind base;
            @tailwind components;
            @tailwind utilities;"""

            try:
                with open(app_css_file, "w") as f:
                    f.write(css_content)
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar {app_css_file}: {e}\n")

            self.log_text.insert("end", f"Conteúdo do {app_css_file} atualizado.\n")

            index_css_file = "src/index.css"
            if os.path.exists(index_css_file):
                try:
                    os.remove(index_css_file)
                    self.log_text.insert("end", f"{index_css_file} removido.\n")
                except Exception as e:
                    self.log_text.insert("end", f"Erro ao remover {index_css_file}: {e}\n")
            else:
                self.log_text.insert("end", f"{index_css_file} não encontrado.\n")

            for file_name in ["README.md", "eslint.config.js"]:
                file_path = file_name
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        self.log_text.insert("end", f"{file_path} removido.\n")
                    except Exception as e:
                        self.log_text.insert("end", f"Erro ao remover {file_path}: {e}\n")
                else:
                    self.log_text.insert("end", f"{file_path} não encontrado.\n")

            public_svg_file = os.path.join("public", "vite.svg")
            if os.path.exists(public_svg_file):
                try:
                    os.remove(public_svg_file)
                    self.log_text.insert("end", f"{public_svg_file} removido.\n")
                except Exception as e:
                    self.log_text.insert("end", f"Erro ao remover {public_svg_file}: {e}\n")
            else:
                self.log_text.insert("end", f"{public_svg_file} não encontrado.\n")

            assets_svg_file = os.path.join("src", "assets", "react.svg")
            if os.path.exists(assets_svg_file):
                try:
                    os.remove(assets_svg_file)
                    self.log_text.insert("end", f"{assets_svg_file} removido.\n")
                except Exception as e:
                    self.log_text.insert("end", f"Erro ao remover {assets_svg_file}: {e}\n")
            else:
                self.log_text.insert("end", f"{assets_svg_file} não encontrado.\n")

            app_jsx_file = "src/app.jsx"
            app_jsx_content = """function App() {

            return (
                <>
                    <h1 className="text-xl font-bold bg-blue-500 text-white">Testando o Tailwind</h1>
                </>
            )
            }

            export default App
            """

            try:
                with open(app_jsx_file, "w") as f:
                    f.write(app_jsx_content)
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar {app_jsx_file}: {e}\n")

            self.log_text.insert("end", f"Conteúdo do {app_jsx_file} atualizado.\n")

            main_jsx_file = "src/main.jsx"
            main_jsx_content = """import { StrictMode } from 'react'
        import { createRoot } from 'react-dom/client'
        import App from './App.jsx'
        import './app.css'

        const root = createRoot(document.getElementById('root'))
        root.render(
            <StrictMode>
                <App />
            </StrictMode>
        )
        """

            try:
                with open(main_jsx_file, "w") as f:
                    f.write(main_jsx_content)
            except Exception as e:
                self.log_text.insert("end", f"Erro ao criar {main_jsx_file}: {e}\n")

            self.log_text.insert("end", f"Conteúdo do {main_jsx_file} atualizado.\n")

            self.log_text.insert("end", "Projeto configurado com sucesso!\n")

        except Exception as e:
            self.log_text.insert("end", f"Erro na criação do projeto: {e}\n")

if __name__ == "__main__":
    app = App()
    app.mainloop()
