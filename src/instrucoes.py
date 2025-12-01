class ParserInstrucoes:
    """Parser para ler e processar instruções bytecode"""
    
    @staticmethod
    def parsear_arquivo(caminho_arquivo):
        """Lê arquivo e retorna lista de instruções"""
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
        return ParserInstrucoes.parsear_linhas(linhas)
    
    @staticmethod
    def parsear_linhas(linhas):
        """Processa linhas de texto em instruções"""
        instrucoes = []
        
        for i, linha in enumerate(linhas):
            linha = linha.strip()
            
            if not linha or linha.startswith('#'):
                instrucoes.append(('VAZIO', None, i))
                continue
            
            if '#' in linha:
                linha = linha[:linha.index('#')].strip()
            
            if linha.endswith(':'):
                label = linha[:-1].strip()
                instrucoes.append(('LABEL', label, i))
                continue
            
            partes = linha.split(maxsplit=1)
            operacao = partes[0].upper()
            argumento = partes[1] if len(partes) > 1 else None
            
            if argumento and argumento.replace('-', '').replace('.', '').isdigit():
                argumento = float(argumento) if '.' in argumento else int(argumento)
            
            instrucoes.append((operacao, argumento, i))
        
        return instrucoes
    
    @staticmethod
    def encontrar_labels(instrucoes):
        """Cria mapa de labels para índices de instrução"""
        labels = {}
        for idx, (op, arg, _) in enumerate(instrucoes):
            if op == 'LABEL':
                if arg in labels:
                    raise ValueError(f"Label duplicado: {arg}")
                labels[arg] = idx
        return labels