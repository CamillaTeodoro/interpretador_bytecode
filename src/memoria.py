class Memoria:
    """Gerencia variáveis (mapeamento nome -> valor)"""
    
    def __init__(self):
        self.variaveis = {}
    
    def armazenar(self, nome, valor):
        """Armazena um valor em uma variável"""
        self.variaveis[nome] = valor
    
    def carregar(self, nome):
        """Carrega o valor de uma variável"""
        if nome not in self.variaveis:
            raise NameError(f"Variável '{nome}' não definida")
        return self.variaveis[nome]
    
    def existe(self, nome):
        """Verifica se uma variável existe"""
        return nome in self.variaveis
    
    def limpar(self):
        """Limpa todas as variáveis"""
        self.variaveis.clear()
    
    def __str__(self):
        return str(self.variaveis)