
from datetime import datetime
from . import graph_ops
from .data import V_CARROS, V_PECAS

def generate_full_report(B, P, save_path="relatorio_completo.md"):
    """
    Generates a comprehensive markdown report answering TG.txt questions.
    """
    
    # 1. Basic Stats
    num_cars = B.degree(V_CARROS)
    avg_per_car = sum(d for n, d in num_cars) / len(V_CARROS)
    
    # 2. Communities (Clusters)
    community_map, communities = graph_ops.detect_communities(P)
    
    # 3. Hubs (Critical Parts)
    critical_parts = graph_ops.get_part_criticality(B)
    top_5_parts = critical_parts[:5]
    
    # 4. Resilience (Simulate failure of top part)
    top_part = top_5_parts[0][0]
    affected, impact_severity = graph_ops.simulate_part_failure(B, top_part)
    
    # 5. Stock Savings
    total_needed, unique, savings = graph_ops.analyze_stock_savings(B)
    
    with open(save_path, "w") as f:
        f.write(f"# Relatório de Análise de Grafos: Cadeia de Suprimentos Automotiva\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        f.write("## 1. Contextualização e Modelagem\n")
        f.write("Este relatório utiliza Teoria dos Grafos para responder perguntas estratégicas sobre compartilhamento de peças.\n")
        f.write(f"- **Total de Veículos Analisados:** {len(V_CARROS)}\n")
        f.write(f"- **Total de Peças Únicas:** {len(V_PECAS)}\n")
        f.write(f"- **Média de Peças por Veículo (no dataset):** {avg_per_car:.1f}\n\n")
        
        f.write("## 2. Agrupamentos Naturais (Clusters)\n")
        f.write("> *Pergunta: Quais agrupamentos naturais de veículos existem segundo compartilhamento de peças?*\n\n")
        f.write(f"Utilizando algoritmos de detecção de comunidades (Modularity Maximization), identificamos **{len(communities)} famílias principais** de veículos:\n\n")
        
        for i, comm in enumerate(communities):
            f.write(f"### Família {i+1} (Tam: {len(comm)})\n")
            f.write(f"- **Veículos:** {', '.join(list(comm)[:8])} {'...' if len(comm)>8 else ''}\n")
            # Try to guess name based on membership
            guess_name = "Grupo Misture"
            if "VW Golf Mk7" in comm or "Audi A3 8V" in comm: guess_name = "Plataforma MQB (VW Group)"
            elif "Jeep Compass" in comm: guess_name = "Stellantis (Small Wide)"
            elif "Renault Clio IV" in comm: guess_name = "Aliança Renault-Nissan"
            f.write(f"- **Identificação Provável:** {guess_name}\n\n")
            
        f.write("## 3. Identificação de Hubs (Peças Críticas)\n")
        f.write("> *Pergunta: Quais peças são “hubs” — usadas por muitos veículos?*\n\n")
        f.write("As peças com maior **Grau de Centralidade** (conectadas a mais veículos) são:\n\n")
        f.write("| Rank | Peça (Hub) | Veículos Afetados |\n")
        f.write("|---|---|---|\n")
        for i, (part, deg) in enumerate(top_5_parts):
            f.write(f"| {i+1} | {part} | {deg} |\n")
            
        f.write("\nEssas peças representam o maior risco de gargalo, mas também a maior oportunidade de economia de escala.\n\n")
        
        f.write("## 4. Análise de Resiliência e Falhas\n")
        f.write("> *Pergunta: Se uma peça crítica ficar indisponível, quantos veículos ficam afetados?*\n\n")
        f.write(f"Simulação de falha da peça **'{top_part}'**:\n")
        f.write(f"- **Impacto Direto:** {len(affected)} veículos parariam a produção.\n")
        f.write(f"- **Severidade:** {impact_severity*100:.1f}% da frota analisada.\n")
        f.write(f"- **Lista de Afetados:** {', '.join(affected[:5])}...\n\n")
        
        f.write("## 5. Otimização de Estoques\n")
        f.write("> *Pergunta: Como minimizar custo total de estoque?*\n\n")
        f.write("A análise comparativa entre SKUs únicos e demanda total mostra o ganho da estratégia de plataforma:\n\n")
        f.write(f"- **Total de Peças Necessárias (sem compartilhamento):** {total_needed}\n")
        f.write(f"- **Total de SKUs Reais (com compartilhamento):** {unique}\n")
        f.write(f"- **Fator de Redução de Estoque:** {savings*100:.1f}%\n\n")
        f.write("Isso indica que a estratégia de compartilhamento está reduzindo a complexidade logística significativamente.\n")
    
    print(f"Report generated successfully: {save_path}")

