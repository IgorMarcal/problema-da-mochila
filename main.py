import importlib
from itens import ItensPreDefinidos
from HC import HC
from SA import SA
from AG import AG

def executar_otimizacao(algoritmo):
    todos_itens = ItensPreDefinidos.obter_todos_itens()

    print(f"Algoritmo: {algoritmo.upper()}")
    print(f"Itens: {todos_itens}")
    print("-" * 50)
    
    print()
    
    if algoritmo.upper() == 'HC':
        HC.executa_hc(todos_itens)
        return "HC executado com sucesso"
    
    elif algoritmo.upper() == 'SA':
        SA.executa_sa(todos_itens, mostrar_processo=True)
        return "SA executado com sucesso"

    elif algoritmo.upper() == 'AG':
        AG.executa_ag(todos_itens, mostrar_processo=True)
        return "SA executado com sucesso"
    
    elif algoritmo.upper() == 'COMPARACAO_DETALHADA':
        print("📊 COMPARAÇÃO DETALHADA DE TODOS OS ALGORITMOS")
        print("=" * 80)
        
        # Executa cada algoritmo uma vez para comparação
        print("\n🏔️ HILL CLIMBING:")
        solucao_hc, valor_hc, peso_hc, hist_hc = HC.executa_hc(todos_itens, mostrar_processo=False)
        itens_hc = [todos_itens[i].nome for i in range(len(solucao_hc)) if solucao_hc[i] == 1]
        
        print("\n🔥 SIMULATED ANNEALING:")  
        solucao_sa, valor_sa, peso_sa, hist_sa = SA.executa_sa(todos_itens, mostrar_processo=False)
        itens_sa = [todos_itens[i].nome for i in range(len(solucao_sa)) if solucao_sa[i] == 1]
        
        print("\n🧬 ALGORITMO GENÉTICO:")
        solucao_ag, valor_ag, peso_ag, hist_ag = AG.executa_ag(todos_itens, mostrar_processo=False)
        itens_ag = [todos_itens[i].nome for i in range(len(solucao_ag)) if solucao_ag[i] == 1]
        
        # Tabela comparativa
        print("\n" + "=" * 80)
        print("📋 RESULTADOS COMPARATIVOS")
        print("=" * 80)
        
        print(f"{'ALGORITMO':<20} {'VALOR':<12} {'PESO':<12} {'EFICIÊNCIA':<12} {'ITERAÇÕES':<12}")
        print("-" * 80)
        print(f"{'Hill Climbing':<20} R$ {valor_hc:<8.0f} {peso_hc:<8.1f}kg {(valor_hc/peso_hc):<8.2f} {len(hist_hc)-1:<12}")
        print(f"{'Simulated Annealing':<20} R$ {valor_sa:<8.0f} {peso_sa:<8.1f}kg {(valor_sa/peso_sa):<8.2f} {len(hist_sa)-1:<12}")  
        print(f"{'Algoritmo Genético':<20} R$ {valor_ag:<8.0f} {peso_ag:<8.1f}kg {(valor_ag/peso_ag):<8.2f} {len(hist_ag)-1:<12}")
        
        # Itens selecionados
        print(f"\n🎒 ITENS SELECIONADOS:")
        print(f"HC  ({len(itens_hc)} itens): {', '.join(itens_hc)}")
        print(f"SA  ({len(itens_sa)} itens): {', '.join(itens_sa)}")
        print(f"AG  ({len(itens_ag)} itens): {', '.join(itens_ag)}")
        
        # Análise de sobreposição
        set_hc = set(itens_hc)
        set_sa = set(itens_sa)  
        set_ag = set(itens_ag)
        
        comum_todos = set_hc & set_sa & set_ag
        print(f"\n🤝 ITENS COMUNS A TODOS: {list(comum_todos) if comum_todos else 'Nenhum'}")
        
        # Melhor algoritmo
        melhor_valor = max(valor_hc, valor_sa, valor_ag)
        if valor_hc == melhor_valor:
            vencedor = "Hill Climbing"
        elif valor_sa == melhor_valor:
            vencedor = "Simulated Annealing"
        else:
            vencedor = "Algoritmo Genético"
        
        print(f"\n🏆 MELHOR RESULTADO: {vencedor} com R$ {melhor_valor:.0f}")
        
        print(f"\nHC - Valor R$ {valor_hc}, peso {peso_hc:.0f} Kg, itens>: {itens_hc}")
        print(f"\nSA - Valor R$ {valor_sa}, peso {peso_sa:.0f} Kg, itens: {itens_sa}")
        print(f"\nAG - Valor R$ {peso_ag}, peso {peso_ag:.0f} Kg, itens: {itens_ag}")

        return f"vencedor {vencedor}"
    elif algoritmo.upper() == 'ANALISE_HC':
        resultados = []
        for i in range(20):
            _, valor, _, _ = HC.executa_hc(todos_itens)
            resultados.append(valor)
        
        variacao = max(resultados) - min(resultados)
        
        if variacao > 50:
            return "SIM - Muitos ótimos locais (variação alta)"
        else:
            return "NÃO - Instância bem comportada (variação baixa)"
    else:
        print(f"Algoritmo {algoritmo} ainda não implementado")