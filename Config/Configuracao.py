import json
import os

class Ambiente():
    ambiente = None

    def __init__(self):
        if "AMBIENTE_DEV" in os.environ:
            self.ambiente = 'dev'
        else:
            self.ambiente = 'localhost'

    def receberAmbiente(self):
        return self.ambiente

class Configuracao(Ambiente):
    config = dict()

    def __init__(self):
        super().__init__()

        arquivoNome = f'config.{self.ambiente}.json'
        configCaminho = os.path.dirname(os.path.abspath(__file__))
        arquivoCaminho = os.path.join(configCaminho, arquivoNome)

        with open(arquivoCaminho, 'r') as dadosConfig:
            self.config = json.load(dadosConfig)

        
    def receberConfiguracao(self, nomeConfig):
        return self.config[nomeConfig]