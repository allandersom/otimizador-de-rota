class CaminhaoPoliguindaste:
    """
    Representa um caminhão poliguindaste na frota.
    Capacidade máxima: 4 'slots' de espaço.
    - Caixa Vazia = Ocupa 1 slot (Máx 4 vazias).
    - Caixa Cheia = Ocupa 2 slots (Máx 2 cheias).
    """
    
    def __init__(self, placa: str, motorista: str, vazias_iniciais: int = 0):
        self.placa = placa
        self.motorista = motorista
        self.caixas_vazias = vazias_iniciais
        self.caixas_cheias = 0
        self.viagens_usina = 0
        self.tarefas = {'colocacoes': 0, 'retiradas': 0, 'trocas': 0}

    def espaco_livre(self) -> int:
        """Calcula o espaço livre no caminhão (Máximo de 4 slots)."""
        espaco_ocupado = (self.caixas_vazias * 1) + (self.caixas_cheias * 2)
        return 4 - espaco_ocupado

    def descarregar_na_usina(self):
        """Simula a ida do caminhão até a usina para descarte das caixas cheias."""
        if self.caixas_cheias > 0:
            self.caixas_cheias = 0
            self.viagens_usina += 1
            # Nota: O caminhão mantém as caixas vazias que já carregava.

    def verificar_limite_usina(self):
        """Verifica se o caminhão atingiu o limite de 2 caixas cheias e força o descarte."""
        if self.caixas_cheias == 2:
            self.descarregar_na_usina()

    def tentar_colocacao(self) -> bool:
        """Tenta realizar uma colocação (deixar 1 caixa vazia na obra)."""
        if self.caixas_vazias >= 1:
            self.caixas_vazias -= 1
            self.tarefas['colocacoes'] += 1
            return True
        return False

    def tentar_retirada(self) -> bool:
        """
        Tenta realizar uma retirada (pegar 1 caixa cheia).
        Funciona inclusive se o caminhão estiver totalmente sem caixas (0 vazias, 0 cheias),
        pois haverá 4 slots livres (espaço suficiente para a caixa cheia que exige 2).
        """
        if self.espaco_livre() >= 2:
            self.caixas_cheias += 1
            self.tarefas['retiradas'] += 1
            self.verificar_limite_usina()  # Vai para a usina se lotou
            return True
        return False

    def tentar_troca(self) -> bool:
        """
        Tenta realizar uma troca (deixa 1 vazia, pega 1 cheia).
        Exige pelo menos 1 vazia na caçamba e que, após deixar a vazia, haja espaço para a cheia.
        """
        # Se tem 1 vazia e pelo menos 1 slot livre (pois a cheia toma 2, e a vazia libera 1)
        if self.caixas_vazias >= 1 and self.espaco_livre() >= 1:
            self.caixas_vazias -= 1
            self.caixas_cheias += 1
            self.tarefas['trocas'] += 1
            self.verificar_limite_usina()  # Vai para a usina se lotou
            return True
        return False


def distribuir_tarefas(frota: list, total_colocacoes: int, total_retiradas: int, total_trocas: int):
    """
    Distribui as tarefas demandadas entre a frota ativa disponível.
    Prioriza trocas, depois colocações, depois retiradas.
    """
    print("--- INICIANDO ROTEIRIZAÇÃO ---\n")
    
    # 1. Distribuição de Trocas
    while total_trocas > 0:
        alocado = False
        for caminhao in frota:
            if total_trocas > 0 and caminhao.tentar_troca():
                total_trocas -= 1
                alocado = True
        if not alocado:
            print(f"⚠️ Alerta: Faltou capacidade/caixa vazia para realizar {total_trocas} trocas.")
            break

    # 2. Distribuição de Colocações
    while total_colocacoes > 0:
        alocado = False
        for caminhao in frota:
            if total_colocacoes > 0 and caminhao.tentar_colocacao():
                total_colocacoes -= 1
                alocado = True
        if not alocado:
            print(f"⚠️ Alerta: Faltou caixa vazia na frota para realizar {total_colocacoes} colocações.")
            break

    # 3. Distribuição de Retiradas
    while total_retiradas > 0:
        alocado = False
        for caminhao in frota:
            if total_retiradas > 0 and caminhao.tentar_retirada():
                total_retiradas -= 1
                alocado = True
        if not alocado:
            print(f"⚠️ Alerta: Faltou espaço na frota para realizar {total_retiradas} retiradas.")
            break

    # Relatório Final
    print("\n--- RESUMO DA ROTA POR MOTORISTA ---")
    for c in frota:
        print(f"🚛 Motorista: {c.motorista} | Placa: {c.placa}")
        print(f"   Tarefas: {c.tarefas['colocacoes']} Colocações | {c.tarefas['retiradas']} Retiradas | {c.tarefas['trocas']} Trocas")
        print(f"   Idas à Usina (Descarte): {c.viagens_usina}")
        print(f"   Carga Final no Caminhão: {c.caixas_vazias} Vazias | {c.caixas_cheias} Cheias")
        print("-" * 50)


if __name__ == "__main__":
    # Dados da frota fornecida
    placas = ['BWU5G46', 'BYJ1E53', 'CSE0H31', 'CSQ8E46', 'PFB1495', 'DKI6I07', 
              'GFA9B22', 'GHA0I73', 'GIR7B54', 'PEY9J45', 'OFQ8A53', 'KLQ4482', 
              'KJC1401', 'OHE9D01', 'OYV5235']
    motoristas = ['ELCIDES', 'MARCONI', 'MAYKEL', 'LUIZ RODRIGO', 'BRUNO', 'PLATINIS']

    # Criando a frota ativa e equipando os caminhões iniciais
    # Exemplo: Caminhões saem da base com 3 caixas vazias (deixa 1 slot livre para facilitar manobras/retiradas)
    frota_ativa = []
    for i in range(len(motoristas)):
        caminhao = CaminhaoPoliguindaste(placa=placas[i], motorista=motoristas[i], vazias_iniciais=3)
        frota_ativa.append(caminhao)

    # Inserindo a demanda do dia
    demanda_colocacoes = 6
    demanda_retiradas = 8
    demanda_trocas = 4

    # Executando o sistema
    distribuir_tarefas(frota_ativa, demanda_colocacoes, demanda_retiradas, demanda_trocas)
