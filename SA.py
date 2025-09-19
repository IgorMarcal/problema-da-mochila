import random
import math

class SA:
    @classmethod
    def executa_sa(cls, itens, capacidade_maxima=50, T0=50.0, Tmin=0.1, 
                   alpha=0.95, passos_por_T=30, mostrar_processo=False):
        """
        Executa algoritmo Simulated Annealing para o problema da mochila
        
        Args:
            itens: Lista de ItemDataclass com nome, valor e peso
            capacidade_maxima: Capacidade máxima da mochila (padrão: 50)
            T0: Temperatura inicial (padrão: 50.0)
            Tmin: Temperatura mínima (padrão: 0.1)
            alpha: Taxa de resfriamento (padrão: 0.95)
            passos_por_T: Passos por temperatura (padrão: 30)
            mostrar_processo: Se deve mostrar o processo detalhado
        
        Returns:
            tuple: (melhor_solucao, melhor_valor, melhor_peso, historico)
        """
        
        def calcular_fitness(solucao):
            """Calcula o fitness (valor total) de uma solução - IGUAL ao HC"""
            peso_total = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
            
            if peso_total > capacidade_maxima:
                return 0
            
            valor_total = sum(itens[i].valor for i in range(len(solucao)) if solucao[i] == 1)
            return valor_total
        
        def gerar_solucao_inicial_aleatoria():
            """Gera solução inicial aleatória e reparada - IGUAL ao HC"""
            if mostrar_processo:
                print("🎲 Gerando solução inicial aleatória...")
            
            solucao = [random.randint(0, 1) for _ in range(len(itens))]
            
            if mostrar_processo:
                peso_inicial = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
                valor_inicial = sum(itens[i].valor for i in range(len(solucao)) if solucao[i] == 1)
                print(f"   Solução aleatória: peso={peso_inicial:.1f}kg, valor=R${valor_inicial:.0f}")
            
            # Processo de reparo
            peso_atual = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
            
            while peso_atual > capacidade_maxima:
                itens_selecionados = [i for i in range(len(solucao)) if solucao[i] == 1]
                if not itens_selecionados:
                    break
                
                item_a_remover = min(itens_selecionados, key=lambda i: itens[i].ratio_valor_peso())
                solucao[item_a_remover] = 0
                peso_atual -= itens[item_a_remover].peso
                
                if mostrar_processo:
                    print(f"   Removendo {itens[item_a_remover].nome} (ratio baixo)")
            
            if mostrar_processo:
                peso_final = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
                valor_final = sum(itens[i].valor for i in range(len(solucao)) if solucao[i] == 1)
                print(f"   Solução reparada: peso={peso_final:.1f}kg, valor=R${valor_final:.0f}")
            
            return solucao
        
        def gerar_vizinho_aleatorio(solucao_atual):
            """
            DIFERENÇA PRINCIPAL: Gera apenas 1 vizinho aleatório (não todos os 15)
            """
            vizinho = solucao_atual.copy()
            posicao = random.randint(0, len(solucao_atual) - 1)
            vizinho[posicao] = 1 - vizinho[posicao]  # Flip
            return vizinho, posicao
        
        def aceitar_solucao(fitness_atual, fitness_vizinho, temperatura):
            """
            CORAÇÃO DO SIMULATED ANNEALING: Critério de aceitação probabilístico
            """
            if fitness_vizinho > fitness_atual:
                # Sempre aceita se melhor
                return True, "MELHOR"
            
            if temperatura <= 0:
                # Se temperatura zero, não aceita pior
                return False, "T_ZERO"
            
            # Calcula probabilidade de aceitar solução PIOR
            delta = fitness_vizinho - fitness_atual  # Será negativo (pior)
            try:
                probabilidade = math.exp(delta / temperatura)
            except OverflowError:
                probabilidade = 0.0
            
            # Decisão probabilística
            if random.random() < probabilidade:
                return True, f"PROB_{probabilidade:.3f}"
            else:
                return False, f"REJ_{probabilidade:.3f}"
        
        def calcular_peso(solucao):
            """Calcula o peso total de uma solução"""
            return sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
        
        # ========== INICIALIZAÇÃO ==========
        if mostrar_processo:
            print("🔥 SIMULATED ANNEALING - PROBLEMA DA MOCHILA")
            print(f"📊 Configuração: {len(itens)} itens, {capacidade_maxima}kg")
            print(f"🌡️  Temperatura: {T0:.1f} → {Tmin:.1f} (α={alpha}, {passos_por_T} passos/T)")
            print("=" * 70)
        
        # Gera solução inicial
        solucao_atual = gerar_solucao_inicial_aleatoria()
        fitness_atual = calcular_fitness(solucao_atual)
        peso_atual = calcular_peso(solucao_atual)
        
        # Inicializa melhor solução
        melhor_solucao = solucao_atual.copy()
        melhor_fitness = fitness_atual
        melhor_peso = peso_atual
        
        # Controle de temperatura
        temperatura = T0
        iteracao_global = 0
        aceitos_total = 0
        rejeitados_total = 0
        
        # Histórico
        historico = [(iteracao_global, fitness_atual, peso_atual, temperatura)]
        
        if mostrar_processo:
            print(f"\n🏁 Solução inicial:")
            print(f"   Valor: R$ {fitness_atual:.0f}, Peso: {peso_atual:.1f}kg")
            print(f"   Temperatura: {temperatura:.2f}")
            print()
        
        # ========== LOOP PRINCIPAL DO SIMULATED ANNEALING ==========
        ciclo_temperatura = 0
        
        while temperatura > Tmin:
            ciclo_temperatura += 1
            
            if mostrar_processo:
                print(f"🌡️  CICLO {ciclo_temperatura}: T = {temperatura:.2f}")
            
            aceitos_neste_ciclo = 0
            rejeitados_neste_ciclo = 0
            
            # Executa 'passos_por_T' iterações nesta temperatura
            for passo in range(passos_por_T):
                iteracao_global += 1
                
                # Gera UM vizinho aleatório
                vizinho, posicao_flip = gerar_vizinho_aleatorio(solucao_atual)
                fitness_vizinho = calcular_fitness(vizinho)
                
                # DECISÃO: Aceita ou rejeita usando critério SA?
                aceita, motivo = aceitar_solucao(fitness_atual, fitness_vizinho, temperatura)
                
                if aceita:
                    # ACEITA a solução (pode ser pior!)
                    solucao_atual = vizinho
                    fitness_atual = fitness_vizinho
                    peso_atual = calcular_peso(solucao_atual)
                    aceitos_total += 1
                    aceitos_neste_ciclo += 1
                    
                    # Atualiza melhor global se necessário
                    if fitness_atual > melhor_fitness:
                        melhor_solucao = solucao_atual.copy()
                        melhor_fitness = fitness_atual
                        melhor_peso = peso_atual
                        
                        if mostrar_processo:
                            acao = "ADD" if solucao_atual[posicao_flip] == 1 else "REM"
                            print(f"   ⭐ NOVO MELHOR! {acao} Item {posicao_flip+1}: R$ {fitness_atual:.0f} ({motivo})")
                    
                    elif mostrar_processo and motivo.startswith("PROB"):
                        acao = "ADD" if solucao_atual[posicao_flip] == 1 else "REM"
                        print(f"   🎲 Aceita pior! {acao} Item {posicao_flip+1}: R$ {fitness_atual:.0f} ({motivo})")
                
                else:
                    # REJEITA a solução
                    rejeitados_total += 1
                    rejeitados_neste_ciclo += 1
                
                # Adiciona ao histórico
                historico.append((iteracao_global, fitness_atual, peso_atual, temperatura))
            
            # Relatório do ciclo de temperatura
            taxa_aceitacao = (aceitos_neste_ciclo / passos_por_T) * 100
            if mostrar_processo:
                print(f"   📊 Aceitos: {aceitos_neste_ciclo}/{passos_por_T} ({taxa_aceitacao:.1f}%)")
            
            # ========== RESFRIAMENTO ==========
            temperatura *= alpha
        
        if mostrar_processo:
            print(f"\n❄️  RESFRIAMENTO COMPLETO (T final = {temperatura:.3f})")
        
        # ========== RESULTADO FINAL ==========
        if mostrar_processo:
            print("\n" + "=" * 70)
            print("🔥 RESULTADO FINAL DO SIMULATED ANNEALING")
            print("=" * 70)
        
        itens_selecionados = [itens[i] for i in range(len(melhor_solucao)) if melhor_solucao[i] == 1]
        
        if mostrar_processo:
            print(f"✅ Melhor valor encontrado: R$ {melhor_fitness:.2f}")
            print(f"⚖️  Peso utilizado: {melhor_peso:.2f}kg / {capacidade_maxima}kg ({(melhor_peso/capacidade_maxima)*100:.1f}%)")
            print(f"📈 Eficiência: {(melhor_fitness/melhor_peso):.2f} valor/kg")
            print(f"🔢 Total de iterações: {iteracao_global}")
            print(f"🌡️  Ciclos de temperatura: {ciclo_temperatura}")
            print(f"✅ Soluções aceitas: {aceitos_total} ({(aceitos_total/iteracao_global)*100:.1f}%)")
            print(f"❌ Soluções rejeitadas: {rejeitados_total} ({(rejeitados_total/iteracao_global)*100:.1f}%)")
            print(f"🎒 Itens selecionados: {len(itens_selecionados)}")
            
            print(f"\n📋 COMPOSIÇÃO FINAL DA MOCHILA:")
            valor_check = 0
            peso_check = 0
            
            for i, item in enumerate(itens_selecionados, 1):
                print(f"{i:2d}. {item.nome:8s}: R${item.valor:6.2f} ({item.peso:5.1f}kg) | Ratio: {item.ratio_valor_peso():5.2f}")
                valor_check += item.valor
                peso_check += item.peso
            
            print(f"\n🧮 Verificação: R$ {valor_check:.2f} | {peso_check:.1f}kg")
        
        return melhor_solucao, melhor_fitness, melhor_peso, historico
