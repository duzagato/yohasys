import importlib
from Models.Database import Database
from Config.Configuracao import Configuracao

import os

class Core():
    def __init__(self) -> None:
        self._db = Database('yoha')
        route = '/api/v1/clientes/get_all_clients'
        rota = self._db.SelecionarRota(route)
        self._controller = rota['controller_rota']
        self._action = rota['action_rota']
        modulo = rota['valor_diretorio'].replace('/', '.')
        self._modulo = modulo.replace('App.', '')
        self._modulo = f'{self._modulo}.{self._controller}'

    def start(self):
        modulo = importlib.import_module(self._modulo)

        nome_classe = self._controller[0].upper() + self._controller[1:]
        classe = getattr(modulo, nome_classe)
        instancia = classe()
        metodo = getattr(instancia, self._action)
        metodo()