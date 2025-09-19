import random
import copy

class AG:
    @classmethod
    def executa_ag(cls, itens, capacidade_maxima=50, pop_size=50, geracoes=120,
                   k_torneio=3, p_cross=0.9, p_mut=0.02, elitismo=2, mostrar_processo=False):
        """
        Executa algoritmo Genético para o problema da mochila
        
        Args:
            itens: Lista de ItemDataclass com nome, valor e peso
            capacidade_maxima: Capacidade máxima da mochila (padrão: 50)
            pop_size: Tamanho da população (padrão: 50)
            geracoes: Número de gerações (padrão: 120)
            k_torneio: Tamanho do torneio para seleção (padrão: 3)
            p_cross: Probabilidade de crossover (padrão: 0.9)
            p_mut: Probabilidade de mutação (padrão: 0.02)
            elitismo: Número de melhores indivíduos preservados (padrão: 2)
            mostrar_processo: Se deve mostrar o processo detalhado
        
        Returns:
            tuple: (melhor_solucao, melhor_valor, melhor_peso, historico)
        """
        
        def calcular_fitness(individuo):
            """Calcula o fitness (valor total) de um indivíduo"""
            peso_total = sum(itens[i].peso for i in range(len(individuo)) if individuo[i] == 1)
            
            if peso_total > capacidade_maxima:
                # PENALIZAÇÃO: Fitness proporcional ao excesso de peso
                excesso = peso_total - capacidade_maxima
                penalizacao = excesso * 10  # Penaliza 10 pontos por kg de excesso
                valor_bruto = sum(itens[i].valor for i in range(len(individuo)) if individuo[i] == 1)
                return max(0, valor_bruto - penalizacao)
            
            valor_total = sum(itens[i].valor for i in range(len(individuo)) if individuo[i] == 1)
            return valor_total
        
        def calcular_peso(individuo):
            """Calcula o peso total de um indivíduo"""
            return sum(itens[i].peso for i in range(len(individuo)) if individuo[i] == 1)
        
        def gerar_individuo_aleatorio():
            """Gera um indivíduo (solução) aleatório"""
            return [random.randint(0, 1) for _ in range(len(itens))]
        
        def gerar_populacao_inicial():
            """Gera população inicial de indivíduos aleatórios"""
            populacao = []
            
            # 50% da população: indivíduos completamente aleatórios
            for _ in range(pop_size // 2):
                individuo = gerar_individuo_aleatorio()
                populacao.append(individuo)
            
            # 50% da população: indivíduos com reparo (heurística gulosa)
            for _ in range(pop_size // 2):
                individuo = gerar_individuo_aleatorio()
                individuo_reparado = reparar_individuo(individuo)
                populacao.append(individuo_reparado)
            
            return populacao
        
        def reparar_individuo(individuo):
            """Repara indivíduo inválido removendo itens com menor ratio"""
            individuo_reparado = individuo.copy()
            peso_atual = calcular_peso(individuo_reparado)
            
            while peso_atual > capacidade_maxima:
                itens_selecionados = [i for i in range(len(individuo_reparado)) if individuo_reparado[i] == 1]
                if not itens_selecionados:
                    break
                
                item_a_remover = min(itens_selecionados, key=lambda i: itens[i].ratio_valor_peso())
                individuo_reparado[item_a_remover] = 0
                peso_atual -= itens[item_a_remover].peso
            
            return individuo_reparado
        
        def selecao_torneio(populacao, fitness_populacao, k=k_torneio):
            """Seleção por torneio: escolhe k indivíduos aleatórios e retorna o melhor"""
            indices_torneio = random.sample(range(len(populacao)), k)
            melhor_indice = max(indices_torneio, key=lambda i: fitness_populacao[i])
            return populacao[melhor_indice].copy()
        
        def crossover_um_ponto(pai1, pai2):
            """Crossover de um ponto: troca genes após ponto aleatório"""
            if random.random() > p_cross:
                # Não faz crossover, retorna os pais
                return pai1.copy(), pai2.copy()
            
            # Escolhe ponto de corte aleatório
            ponto_corte = random.randint(1, len(pai1) - 1)
            
            # Cria filhos
            filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
            filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
            
            return filho1, filho2
        
        def mutacao_bit(individuo):
            """Mutação por inversão de bit: inverte bits com probabilidade p_mut"""
            individuo_mutado = individuo.copy()
            
            for i in range(len(individuo_mutado)):
                if random.random() < p_mut:
                    # Inverte o bit (0->1 ou 1->0)
                    individuo_mutado[i] = 1 - individuo_mutado[i]
            
            return individuo_mutado
        
        def obter_elite(populacao, fitness_populacao, num_elite=elitismo):
            """Obtém os melhores indivíduos (elitismo)"""
            indices_ordenados = sorted(range(len(populacao)), 
                                     key=lambda i: fitness_populacao[i], 
                                     reverse=True)
            
            elite = []
            for i in range(min(num_elite, len(populacao))):
                elite.append(populacao[indices_ordenados[i]].copy())
            
            return elite
        
        def calcular_estatisticas(populacao, fitness_populacao):
            """Calcula estatísticas da população"""
            melhor_fitness = max(fitness_populacao)
            pior_fitness = min(fitness_populacao)
            fitness_medio = sum(fitness_populacao) / len(fitness_populacao)
            
            melhor_indice = fitness_populacao.index(melhor_fitness)
            melhor_individuo = populacao[melhor_indice]
            melhor_peso = calcular_peso(melhor_individuo)
            
            return melhor_fitness, melhor_peso, fitness_medio, pior_fitness
        
        # ========== INICIALIZAÇÃO ==========
        if mostrar_processo:
            print("🧬 ALGORITMO GENÉTICO - PROBLEMA DA MOCHILA")
            print(f"📊 Configuração: {len(itens)} itens, {capacidade_maxima}kg")
            print(f"🧬 População: {pop_size} indivíduos, {geracoes} gerações")
            print(f"⚔️  Seleção: Torneio k={k_torneio}")
            print(f"💏 Crossover: 1 ponto, p={p_cross}")
            print(f"🎲 Mutação: Flip bit, p={p_mut}")
            print(f"👑 Elitismo: {elitismo} melhores")
            print("=" * 70)
        
        # Gera população inicial
        if mostrar_processo:
            print("🌱 Gerando população inicial...")
        
        populacao = gerar_populacao_inicial()
        
        # Inicializa controle de melhor solução global
        melhor_solucao_global = None
        melhor_fitness_global = 0
        melhor_peso_global = 0
        
        # Histórico: (geração, melhor_fitness, fitness_medio, pior_fitness, melhor_peso)
        historico = []
        
        # ========== LOOP PRINCIPAL DO ALGORITMO GENÉTICO ==========
        for geracao in range(geracoes):
            
            # 1. AVALIAÇÃO: Calcula fitness de toda população
            fitness_populacao = [calcular_fitness(individuo) for individuo in populacao]
            
            # 2. ESTATÍSTICAS da geração atual
            melhor_fitness, melhor_peso, fitness_medio, pior_fitness = calcular_estatisticas(populacao, fitness_populacao)
            
            # 3. ATUALIZA melhor solução global
            if melhor_fitness > melhor_fitness_global:
                melhor_indice = fitness_populacao.index(melhor_fitness)
                melhor_solucao_global = populacao[melhor_indice].copy()
                melhor_fitness_global = melhor_fitness
                melhor_peso_global = melhor_peso
            
            # 4. ADICIONA ao histórico
            historico.append((geracao, melhor_fitness, fitness_medio, pior_fitness, melhor_peso))
            
            # 5. RELATÓRIO da geração
            if mostrar_processo and (geracao == 0 or (geracao + 1) % 20 == 0 or geracao == geracoes - 1):
                print(f"Gen {geracao+1:3d}: Melhor=R${melhor_fitness:3.0f} | Médio=R${fitness_medio:5.1f} | Pior=R${pior_fitness:3.0f} | Peso={melhor_peso:4.1f}kg")
            
            # 6. CONDIÇÃO DE PARADA (opcional: se não há melhoria por muitas gerações)
            if geracao == geracoes - 1:
                break
            
            # ========== CRIAÇÃO DA NOVA GERAÇÃO ==========
            
            # 7. ELITISMO: Preserva os melhores
            nova_populacao = obter_elite(populacao, fitness_populacao, elitismo)
            
            # 8. REPRODUÇÃO: Completa população com novos indivíduos
            while len(nova_populacao) < pop_size:
                
                # SELEÇÃO: Escolhe dois pais por torneio
                pai1 = selecao_torneio(populacao, fitness_populacao)
                pai2 = selecao_torneio(populacao, fitness_populacao)
                
                # CROSSOVER: Gera dois filhos
                filho1, filho2 = crossover_um_ponto(pai1, pai2)
                
                # MUTAÇÃO: Aplica mutação nos filhos
                filho1 = mutacao_bit(filho1)
                filho2 = mutacao_bit(filho2)
                
                # ADICIONA filhos à nova população
                nova_populacao.append(filho1)
                if len(nova_populacao) < pop_size:
                    nova_populacao.append(filho2)
            
            # 9. SUBSTITUI população antiga pela nova
            populacao = nova_populacao[:pop_size]  # Garante tamanho exato
        
        # ========== RESULTADO FINAL ==========
        if mostrar_processo:
            print("\n" + "=" * 70)
            print("🧬 RESULTADO FINAL DO ALGORITMO GENÉTICO")
            print("=" * 70)
        
        itens_selecionados = [itens[i] for i in range(len(melhor_solucao_global)) if melhor_solucao_global[i] == 1]
        
        if mostrar_processo:
            print(f"✅ Melhor valor encontrado: R$ {melhor_fitness_global:.2f}")
            print(f"⚖️  Peso utilizado: {melhor_peso_global:.2f}kg / {capacidade_maxima}kg ({(melhor_peso_global/capacidade_maxima)*100:.1f}%)")
            print(f"📈 Eficiência: {(melhor_fitness_global/melhor_peso_global):.2f} valor/kg")
            print(f"🧬 Total de gerações: {geracoes}")
            print(f"👥 Tamanho da população: {pop_size}")
            print(f"🎒 Itens selecionados: {len(itens_selecionados)}")
            
            # Análise da evolução
            fitness_inicial = historico[0][1]
            fitness_final = historico[-1][1] 
            melhoria = fitness_final - fitness_inicial
            print(f"📊 Evolução: R$ {fitness_inicial:.0f} → R$ {fitness_final:.0f} (+{melhoria:.0f})")
            
            print(f"\n📋 COMPOSIÇÃO FINAL DA MOCHILA:")
            valor_check = 0
            peso_check = 0
            
            for i, item in enumerate(itens_selecionados, 1):
                print(f"{i:2d}. {item.nome:8s}: R${item.valor:6.2f} ({item.peso:5.1f}kg) | Ratio: {item.ratio_valor_peso():5.2f}")
                valor_check += item.valor
                peso_check += item.peso
            
            print(f"\n🧮 Verificação: R$ {valor_check:.2f} | {peso_check:.1f}kg")
        
        return melhor_solucao_global, melhor_fitness_global, melhor_peso_global, historico
