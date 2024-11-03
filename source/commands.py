import subprocess

def executar_comando(comando, cwd=None, callback=None):
    try:
        resultado = subprocess.run(comando, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        if callback:
            callback(f"Comando executado com sucesso: {comando}\nSaída:\n{resultado.stdout}")
    except subprocess.CalledProcessError as e:
        if callback:
            callback(f"Erro ao executar o comando: {comando}\nSaída de erro:\n{e.stderr}")
        raise  
