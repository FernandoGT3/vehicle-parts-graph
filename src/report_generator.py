
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
    
    # 3. Hubs (Critical Parts) - Expanded Analysis
    critical_parts = graph_ops.get_part_criticality(B)
    top_critical = critical_parts[:10]
    
    # 4. Resilience (Simulate failure of top degree part)
    top_part = top_critical[0][0]
    affected, impact_severity = graph_ops.simulate_part_failure(B, top_part)
    
    # 5. Stock Savings
    total_needed, unique, savings = graph_ops.analyze_stock_savings(B)
    
    # 6. Advanced Topology (Clustering & Jaccard)
    avg_clust, transitivity, local_clust = graph_ops.get_clustering_analysis(P)
    P = graph_ops.calculate_jaccard_weights(B, P)
    
    # 7. Market Segmentation (Assortativity)
    assortativity, _ = graph_ops.calculate_assortativity(P)
    
    with open(save_path, "w") as f:
        f.write(f"# Relatório de Análise de Grafos: Cadeia de Suprimentos Automotiva\n")
        f.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        f.write("## 1. Contextualização e Modelagem\n")
        f.write("Este relatório utiliza propriedades avançadas de Teoria dos Grafos para diagnosticar a maturidade e riscos da cadeia.\n")
        f.write(f"- **Total de Veículos Analisados:** {len(V_CARROS)}\n")
        f.write(f"- **Total de Peças Únicas:** {len(V_PECAS)}\n")
        f.write(f"- **Média de Peças por Veículo:** {avg_per_car:.1f}\n\n")
        
        f.write("## 2. Agrupamentos Naturais (Clusters)\n")
        f.write("> *Pergunta: Quais agrupamentos naturais de veículos existem segundo compartilhamento de peças?*\n\n")
        f.write(f"Utilizando **Modularity Maximization**, identificamos **{len(communities)} plataformas virtuais**:\n\n")
        
        for i, comm in enumerate(communities):
            f.write(f"### Família {i+1} (Tam: {len(comm)})\n")
            f.write(f"- **Veículos:** {', '.join(list(comm)[:8])} {'...' if len(comm)>8 else ''}\n")
            
        f.write("\n## 3. Análise de Vitalidade (Hubs e Gargalos)\n")
        f.write("> *Pergunta: Quais peças são vitais por volume e quais são gargalos estratégicos?*\n\n")
        f.write("Diferenciamos peças por duas métricas de centralidade:\n")
        f.write("1. **Degree Centrality:** Volume absoluto de uso (Economia de Escala).\n")
        f.write("2. **Betweenness Centrality:** Peças que conectam famílias diferentes (Risco de Contágio).\n\n")
        
        f.write("| Rank | Peça (Hub) | Uso (Degree) | Importância (Eigen) | Gargalo (Betweenness) |\n")
        f.write("|---|---|---|---|---|\n")
        for i, (part, deg, dc, bc, ec) in enumerate(top_critical):
            f.write(f"| {i+1} | {part} | {deg} | {ec:.3f} | {bc:.3f} |\n")
            
        f.write("\n## 4. Análise de Resiliência e Falhas\n")
        f.write(f"Simulação de falha da peça principal **'{top_part}'**:\n")
        f.write(f"- **Impacto Direto:** {len(affected)} veículos parariam a produção.\n")
        f.write(f"- **Severidade:** {impact_severity*100:.1f}% da frota analisada.\n\n")
        
        f.write("## 5. Eficiência de Estoque\n")
        f.write(f"- **Redução de SKUs:** {savings*100:.1f}% em comparação a estoques independentes.\n\n")
        
        f.write("## 6. Topologia Avançada e Coesão\n")
        f.write("> *Pergunta: Quão maduras são as plataformas e os compartilhamentos?*\n\n")
        f.write(f"- **Coeficiente de Clustering Médio ({avg_clust:.3f}):** Indica a probabilidade de que dois carros que compartilham peças com um terceiro também compartilhem entre si. Alto valor sugere plataformas bem definidas.\n")
        f.write(f"- **Transitividade ({transitivity:.3f}):** Reforça a análise de coesão global.\n\n")
        f.write("**Índice de Similaridade de Jaccard (Exemplo):**\n")
        f.write("Normaliza o compartilhamento pelo tamanho total dos veículos, evitando viés de complexidade.\n")
        
        # Get top 3 pairs by Jaccard
        edges = sorted(P.edges(data=True), key=lambda x: x[2].get('jaccard', 0), reverse=True)
        for u, v, d in edges[:3]:
            f.write(f"- **{u} ↔ {v}:** J = {d.get('jaccard', 0):.2f} (Compartilham {d.get('weight')} peças)\n")
            
        f.write("\n## 7. Segmentação de Mercado (Assortatividade)\n")
        f.write("> *Pergunta: A estratégia de peças respeita a segmentação de mercado (Premium vs Economy)?*\n\n")
        f.write(f"- **Assortatividade por Segmento:** {assortativity:.3f}\n")
        if assortativity > 0.1:
            f.write("  *Interpretação:* Positiva. Veículos tendem a compartilhar peças apenas dentro do seu próprio segmento (Premium com Premium, Economy com Economy).\n")
        elif assortativity < -0.1:
            f.write("  *Interpretação:* Negativa. Há muito compartilhamento cruzado (Peças Premium em carros de entrada ou vice-versa).\n")
        else:
            f.write("  *Interpretação:* Neutra. O compartilhamento independe do segmento mercadológico.\n")

    print(f"Report generated successfully: {save_path}")

