import sys
from pilha import Pilha
from memoria import Memoria
from instrucoes import ParserInstrucoes

class InterpretadorBytecode:
    """Interpretador de bytecode para máquina de pilha"""
    
    def __init__(self):
        self.pilha = Pilha()
        self.memoria = Memoria()
        self.instrucoes = []
        self.labels = {}
        self.pc = 0  # Program Counter (apontador de instrução)
        self.pilha_chamadas = []  # Pilha para CALL/RET
        self.MAX_CALL_DEPTH = 1000
    
    def carregar_programa(self, caminho_arquivo):
        """Carrega programa bytecode de um arquivo"""
        self.instrucoes = ParserInstrucoes.parsear_arquivo(caminho_arquivo)
        self.labels = ParserInstrucoes.encontrar_labels(self.instrucoes)
        self.pc = 0
    
    def executar(self):
        """Executa o programa bytecode"""
        while self.pc < len(self.instrucoes):
            operacao, argumento, num_linha = self.instrucoes[self.pc]
            
            try:
                if not self.executar_instrucao(operacao, argumento):
                    break  # HALT encontrado
                
            except Exception as e:
                print(f"Erro na linha {num_linha + 1}: {e}", file=sys.stderr)
                sys.exit(1)
    
    def executar_instrucao(self, op, arg):
        """Executa uma única instrução. Retorna False para HALT."""
        
        # Operações de pilha
        if op == 'PUSH':
            self.pilha.push(arg)
            self.pc += 1
        
        elif op == 'POP':
            self.pilha.pop()
            self.pc += 1
        
        # Operações aritméticas
        elif op == 'ADD':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(a + b)
            self.pc += 1
        
        elif op == 'SUB':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(a - b)
            self.pc += 1
        
        elif op == 'MUL':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(a * b)
            self.pc += 1
        
        elif op == 'DIV':
            b = self.pilha.pop()
            a = self.pilha.pop()
            if b == 0:
                raise ZeroDivisionError("Divisão por zero")
            self.pilha.push(int(a / b))  
            self.pc += 1
        
        elif op == 'MOD':
            b = self.pilha.pop()
            a = self.pilha.pop()
            if b == 0:
                raise ZeroDivisionError("Módulo por zero")
            self.pilha.push(a % b)
            self.pc += 1
        
        elif op == 'NEG':
            a = self.pilha.pop()
            self.pilha.push(-a)
            self.pc += 1
        
        # Variáveis
        elif op == 'STORE':
            valor = self.pilha.pop()
            self.memoria.armazenar(arg, valor)
            self.pc += 1
        
        elif op == 'LOAD':
            valor = self.memoria.carregar(arg)
            self.pilha.push(valor)
            self.pc += 1
        
        # Fluxo de controle
        elif op == 'JMP':
            self.pc = self.resolver_endereco(arg)
        
        elif op == 'JZ':  # Jump if Zero
            condicao = self.pilha.pop()
            if condicao == 0:
                self.pc = self.resolver_endereco(arg)
            else:
                self.pc += 1
        
        elif op == 'JNZ':  # Jump if Not Zero
            condicao = self.pilha.pop()
            if condicao != 0:
                self.pc = self.resolver_endereco(arg)
            else:
                self.pc += 1
        
        elif op == 'HALT':
            return False
        
        # Comparações
        elif op == 'EQ':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a == b else 0)
            self.pc += 1
        
        elif op == 'NEQ':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a != b else 0)
            self.pc += 1
        
        elif op == 'LT':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a < b else 0)
            self.pc += 1
        
        elif op == 'GT':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a > b else 0)
            self.pc += 1
        
        elif op == 'LE':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a <= b else 0)
            self.pc += 1
        
        elif op == 'GE':
            b = self.pilha.pop()
            a = self.pilha.pop()
            self.pilha.push(1 if a >= b else 0)
            self.pc += 1
        
        # Funções
        elif op == 'CALL':
            if len(self.pilha_chamadas) >= self.MAX_CALL_DEPTH:
                raise RuntimeError(f"Limite de recursão excedido ({self.MAX_CALL_DEPTH})")
            self.pilha_chamadas.append(self.pc + 1)  # Salva endereço de retorno
            self.pc = self.resolver_endereco(arg)
        
        elif op == 'RET':
            if not self.pilha_chamadas:
                raise RuntimeError("RET sem CALL correspondente")
            self.pc = self.pilha_chamadas.pop()
        
        # E/S
        elif op == 'PRINT':
            if self.pilha.vazia():
                raise RuntimeError("PRINT: pilha vazia")
            valor = self.pilha.peek()  # Mantém na pilha
            print(int(valor) if isinstance(valor, float) and valor.is_integer() else valor)
            self.pc += 1
        
        elif op == 'READ':
            try:
                valor = int(input())
                self.pilha.push(valor)
            except ValueError:
                raise ValueError("Entrada inválida: esperado um número")
            self.pc += 1
        
        elif op in ('VAZIO', 'LABEL'):
            self.pc += 1
        
        else:
            raise ValueError(f"Operação desconhecida: {op}")
        
        return True
    
    def resolver_endereco(self, endereco):
        """Resolve endereço (pode ser label ou número)"""
        if isinstance(endereco, str):
            if endereco not in self.labels:
                raise ValueError(f"Label '{endereco}' não encontrado")
            return self.labels[endereco]
        
        if not isinstance(endereco, str):
            raise ValueError(f"Endereço deve ser inteiro ou label, recebido: {type(endereco)}")
        
        if endereco < 0 or endereco >= len(self.instrucoes):
            raise ValueError(f"Endereço {endereco} fora do alcance (0-{len(self.instrucoes)-1})")
    
        return endereco


def main():
    """Função principal - lê da entrada padrão e executa"""
    if len(sys.argv) > 1:
        interpretador = InterpretadorBytecode()
        interpretador.carregar_programa(sys.argv[1])
        interpretador.executar()
    else:
        linhas = sys.stdin.readlines()
        interpretador = InterpretadorBytecode()
        interpretador.instrucoes = ParserInstrucoes.parsear_linhas(linhas)
        interpretador.labels = ParserInstrucoes.encontrar_labels(interpretador.instrucoes)
        interpretador.executar()


if __name__ == '__main__':
    main()