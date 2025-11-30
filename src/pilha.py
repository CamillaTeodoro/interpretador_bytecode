class Pilha:
    """Implementação da pilha para a máquina virtual"""
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        """Empilha um valor"""
        self.items.append(item)
    
    def pop(self):
        """Desempilha e retorna o topo"""
        if self.vazia():
            raise IndexError("Pop em pilha vazia")
        return self.items.pop()
    
    def peek(self):
        """Retorna o topo sem desempilhar"""
        if self.vazia():
            raise IndexError("Peek em pilha vazia")
        return self.items[-1]
    
    def vazia(self):
        """Verifica se a pilha está vazia"""
        return len(self.items) == 0
    
    def tamanho(self):
        """Retorna o tamanho da pilha"""
        return len(self.items)
    
    def __str__(self):
        return str(self.items)