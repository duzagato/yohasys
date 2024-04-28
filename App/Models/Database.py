from Config.Configuracao import Configuracao
import psycopg2

class Database():
    def __init__(self, schema) -> None:
        self.__schema = schema
        config = Configuracao()
        database = config.config['database']
        try:
            self.__connection = psycopg2.connect(dbname=database['dbname'], user=database['user'], password=database['password'], host=database['host'])
        except:
            print('Erro ao se conectar')

        self.__connection.autocommit = True
        self.__cursor = self.__connection.cursor()

    def EnviarQuery(self, query):
        self.__cursor.execute(query)

        self.__connection.commit()

    def Selecionar(self, query):
        self.__cursor.execute(query)
        resultados = self.__cursor.fetchall()
        colunas = [desc[0] for desc in self.__cursor.description]

        retorno = []

        for linha in resultados:
            retorno.append(dict(zip(colunas, linha)))

        return retorno
    
    def SelecionarRota(self, rota):
        query = f"SELECT * FROM {self.__schema}.ex_rota_diretorio WHERE caminho_rota = '{rota}' ORDER BY id_rota ASC"
        resultado = self.Selecionar(query)
        if len(resultado) > 0:
            rota = resultado[0]
        else:
            query = f"SELECT * FROM {self.__schema}.ex_rota_diretorio WHERE caminho_rota = '/erro' ORDER BY id_rota ASC"
            rota = self.Selecionar(query)[0]
        
        return rota


    def Inserir(self, tabela, dados):
        dados_tabela = ()
        colunas = []
        for chave, valor in dados.items():
            colunas.append(chave)
            dados_tabela += (valor,)

        colunas_query = ', '.join(colunas)
        valores_query = ', '.join(['%s'] * len(colunas))
        query = f'INSERT INTO {self.__schema}.{tabela} ({colunas_query}) VALUES ({valores_query})'
        
        self.__cursor.execute(query, dados_tabela)
        self.__connection.commit()

    def CriarTabela(self, nome, colunas):
        id_coluna = f"Id_{nome} SERIAL PRIMARY KEY"
        colunas.insert(0, id_coluna)
        colunasQuery = ", ".join(colunas)
        query = f'CREATE TABLE {self.__schema}.{nome} ({colunasQuery})'
        
        self.__cursor.execute(query)

        self.__connection.commit()

    def CriarFK(self, coluna, tabela_filha, tabela_pai):
        query = f'ALTER TABLE {self.__schema}.{tabela_filha} ADD CONSTRAINT fk_{coluna} FOREIGN KEY ({coluna}) REFERENCES {self.__schema}.{tabela_pai}({coluna})'

        self.EnviarQuery(query)


