import customtkinter
from tkinter import filedialog

def selecionar_pasta():
    root = customtkinter.CTk()
    root.withdraw()  
    pasta = filedialog.askdirectory(title="Selecione o diretório onde o projeto será criado")
    root.destroy()
    return pasta