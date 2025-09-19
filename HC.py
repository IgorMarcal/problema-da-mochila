import random

class HC:
    @classmethod
    def executa_hc(cls, itens, capacidade_maxima=50, max_iteracoes=300, mostrar_processo=False):
        def calcular_fitness(solucao):
            peso_total = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
            
            if peso_total > capacidade_maxima:
                return 0
            
            valor_total = sum(itens[i].valor for i in range(len(solucao)) if solucao[i] == 1)
            return valor_total
        
        def gerar_solucao_inicial_aleatoria():
            print("Gerando solução inicial aleatória...")
            
            solucao = [random.randint(0, 1) for _ in range(len(itens))]
            
            if mostrar_processo:
                peso_inicial = sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
                valor_inicial = sum(itens[i].valor for i in range(len(solucao)) if solucao[i] == 1)
                print(f"   Solução aleatória: peso={peso_inicial:.1f}kg, valor=R${valor_inicial:.0f}")
            
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
        
        def gerar_vizinhos_por_flip(solucao_atual):
            """
            REGRA 2: Geração de vizinhos por flip de 1 item por vez
            """
            vizinhos = []
            for i in range(len(solucao_atual)):
                vizinho = solucao_atual.copy()
                vizinho[i] = 1 - vizinho[i]
                vizinhos.append(vizinho)
            return vizinhos
        
        def calcular_peso(solucao):
            """Calcula o peso total de uma solução"""
            return sum(itens[i].peso for i in range(len(solucao)) if solucao[i] == 1)
        
        print("🔍 HILL CLIMBING - PROBLEMA DA MOCHILA")
        print(f"📊 Configuração: {len(itens)} itens, {capacidade_maxima}kg, máx {max_iteracoes} iterações")
        print("📋 Regras: Solução aleatória reparada + Flip de 1 item + Parada por iteração/estagnação")
        print("=" * 70)
        
        solucao_atual = gerar_solucao_inicial_aleatoria()
        fitness_atual = calcular_fitness(solucao_atual)
        peso_atual = calcular_peso(solucao_atual)
        
        melhor_solucao = solucao_atual.copy()
        melhor_fitness = fitness_atual
        melhor_peso = peso_atual
        
        historico = [(0, fitness_atual, peso_atual)]
        
        if mostrar_processo:
            itens_iniciais = [itens[i].nome for i in range(len(solucao_atual)) if solucao_atual[i] == 1]
            print(f"\n🏁 Solução inicial:")
            print(f"Item  0: Valor=R${fitness_atual:6.0f}, Peso={peso_atual:5.1f}kg, Itens={len(itens_iniciais)}")
            if len(itens_iniciais) <= 8:
                print(f"         Itens: {', '.join(itens_iniciais)}")
            print()
        
        iteracao_atual = 0
        
        for iteracao in range(1, max_iteracoes + 1):
            iteracao_atual = iteracao
            
            vizinhos = gerar_vizinhos_por_flip(solucao_atual)

            melhor_vizinho = None
            melhor_fitness_vizinho = fitness_atual
            
            for vizinho in vizinhos:
                fitness_vizinho = calcular_fitness(vizinho)
                if fitness_vizinho > melhor_fitness_vizinho:
                    melhor_vizinho = vizinho
                    melhor_fitness_vizinho = fitness_vizinho
            
            if melhor_vizinho is None:
                print(f"ESTAGNAÇÃO na iteração {iteracao-1}")
                print("   Nenhum vizinho oferece melhoria no fitness!")
                break
            
            solucao_atual = melhor_vizinho
            fitness_atual = melhor_fitness_vizinho
            peso_atual = calcular_peso(solucao_atual)
            
            if fitness_atual > melhor_fitness:
                melhor_solucao = solucao_atual.copy()
                melhor_fitness = fitness_atual
                melhor_peso = peso_atual
            
            historico.append((iteracao, fitness_atual, peso_atual))
            
            if mostrar_processo and (iteracao <= 5 or iteracao % 50 == 0):
                print(f"Item {iteracao:3d}: Valor=R${fitness_atual:6.0f}, Peso={peso_atual:5.1f}kg")
        
        if iteracao_atual == max_iteracoes:
            print(f"⏱️  LIMITE DE ITERAÇÕES atingido ({max_iteracoes})")
        
        print("\n" + "=" * 70)
        print("🏆 RESULTADO FINAL DO HILL CLIMBING")
        print("=" * 70)
        
        itens_selecionados = [itens[i] for i in range(len(melhor_solucao)) if melhor_solucao[i] == 1]
        
        print(f"Melhor valor encontrado: R$ {melhor_fitness:.2f}")
        print(f"Peso utilizado: {melhor_peso:.2f}kg / {capacidade_maxima}kg ({(melhor_peso/capacidade_maxima)*100:.1f}%)")
        print(f"Eficiência: {(melhor_fitness/melhor_peso):.2f} valor/kg")
        print(f"Total de iterações executadas: {len(historico)-1}")
        print(f"Quantidade de itens selecionados: {len(itens_selecionados)}")
        
        print(f"\n📋 COMPOSIÇÃO FINAL DA MOCHILA:")
        valor_check = 0
        peso_check = 0
        
        for i, item in enumerate(itens_selecionados, 1):
            print(f"{i:2d}. {item.nome:8s}: R${item.valor:6.2f} ({item.peso:5.1f}kg) | Ratio: {item.ratio_valor_peso():5.2f}")
            valor_check += item.valor
            peso_check += item.peso
        
        print(f"\n🧮 Verificação: R$ {valor_check:.2f} | {peso_check:.1f}kg")

        return melhor_solucao, melhor_fitness, melhor_peso, historico
