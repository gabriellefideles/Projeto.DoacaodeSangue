
from pymongo import MongoClient

class Doador:
    def _init_(self, doador_id, nome, idade, tipo_sanguineo, data_ultima_doacao):
        self.doador_id = doador_id
        self.nome = nome
        self.idade = idade
        self.tipo_sanguineo = tipo_sanguineo
        self.data_ultima_doacao = data_ultima_doacao

    def to_string(self):
        return f"Doador ID: {self.doador_id}, Nome: {self.nome}, Idade: {self.idade}, Tipo Sanguíneo: {self.tipo_sanguineo}, Última Doação: {self.data_ultima_doacao}"

class Doacao:
    def _init_(self, doacao_id, doador_id, data_doacao, quantidade_ml):
        self.doacao_id = doacao_id
        self.doador_id = doador_id
        self.data_doacao = data_doacao
        self.quantidade_ml = quantidade_ml

    def to_string(self):
        return f"Doação ID: {self.doacao_id}, Doador ID: {self.doador_id}, Data: {self.data_doacao}, Quantidade (ml): {self.quantidade_ml}"

class ControladorBancoDeDados:
    def _init_(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['seu_banco']  # Substitua 'seu_banco' pelo nome desejado

    def inserir_doador(self, doador):
        try:
            doadores_collection = self.db['Doadores']
            doadores_collection.insert_one({
                'doador_id': doador.doador_id,
                'nome': doador.nome,
                'idade': doador.idade,
                'tipo_sanguineo': doador.tipo_sanguineo,
                'data_ultima_doacao': doador.data_ultima_doacao
            })
            print("Doador cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir doador: {e}")

    def inserir_doacao(self, doacao):
        try:
            doacoes_collection = self.db['Doacoes']
            doacoes_collection.insert_one({
                'doacao_id': doacao.doacao_id,
                'doador_id': doacao.doador_id,
                'data_doacao': doacao.data_doacao,
                'quantidade_ml': doacao.quantidade_ml
            })
            print("Doação registrada com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir doação: {e}")

class Relatorios:
    @staticmethod
    def relatorio_total_doacoes_por_tipo_sanguineo():
        try:
            doadores_collection = controlador_banco_dados.db['Doadores']
            resultado = doadores_collection.aggregate([
                {'$group': {'_id': '$tipo_sanguineo', 'total_doacoes': {'$sum': 1}}}
            ])
            return resultado
        except Exception as e:
            print(f"Erro ao gerar relatório_total_doacoes_por_tipo_sanguineo: {e}")

    @staticmethod
    def relatorio_detalhes_doacao_com_doador():
        try:
            doacoes_collection = controlador_banco_dados.db['Doacoes']
            resultado = doacoes_collection.aggregate([
                {'$lookup': {
                    'from': 'Doadores',
                    'localField': 'doador_id',
                    'foreignField': 'doador_id',
                    'as': 'doador_info'
                }},
                {'$unwind': '$doador_info'},
                {'$project': {'nome_doador': '$doador_info.nome', 'data_doacao': '$data_doacao', 'quantidade_ml': '$quantidade_ml'}}
            ])
            return resultado
        except Exception as e:
            print(f"Erro ao gerar relatório_detalhes_doacao_com_doador: {e}")

def menu_relatorios():
    while True:
        print("Menu Relatórios:")
        print("1. Total de Doações por Tipo Sanguíneo")
        print("2. Detalhes da Doação com Doador")
        print("3. Voltar")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            relatorio_total_doacoes_por_tipo_sanguineo()
        elif opcao == 2:
            relatorio_detalhes_doacao_com_doador()
        elif opcao == 3:
            break
        else:
            print("Opção inválida. Tente novamente.")

def relatorio_total_doacoes_por_tipo_sanguineo():
    relatorio = Relatorios.relatorio_total_doacoes_por_tipo_sanguineo()
    print("Relatório: Total de Doações por Tipo Sanguíneo")
    for resultado in relatorio:
        print(f"Tipo Sanguíneo: {resultado['_id']}, Total de Doações: {resultado['total_doacoes']}")

def relatorio_detalhes_doacao_com_doador():
    relatorio = Relatorios.relatorio_detalhes_doacao_com_doador()
    print("Relatório: Detalhes da Doação com Doador")
    for resultado in relatorio:
        print(f"Nome do Doador: {resultado['nome_doador']}, Data da Doação: {resultado['data_doacao']}, Quantidade (ml): {resultado['quantidade_ml']}")

def main():
    splash = SplashScreen()
    splash.show()

    while True:
        print("Menu Principal:")
        print("1. Menu Doador")
        print("2. Menu Doação")
        print("3. Menu Relatórios")
        print("4. Sair")

        opcao = int(input("Escolha uma opção: "))