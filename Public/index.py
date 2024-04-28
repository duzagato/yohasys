import sys
import os

# Obtendo diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtendo nível acima a partir de diretório atual
parent_dir = os.path.dirname(current_dir)

# Criando caminho até a pasta App (está no diretório acima)
app_dir = os.path.join(parent_dir, 'App')
config_dir = os.path.join(parent_dir, 'Config')

# Adicionando caminho da pasta App ao arquivo atual
sys.path.append(app_dir)
sys.path.append(parent_dir)

# Importando Core, isso só é possível porque adicionamos a pasta App a pasta do sistema.
from Core import Core

# Iniciando aplicação
app = Core()
app.start()