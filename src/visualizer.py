
import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(G, title="Graph", filename="graph.png", weighted=False, groups=None):
    """
    Plots the graph G.
    - groups: dict mapping node -> community_id for coloring.
    """
    plt.figure(figsize=(16, 12))
    
    # Advanced Layout (Kamada-Kawai often nice for clusters)
    try:
        pos = nx.kamada_kawai_layout(G)
    except:
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # 1. Node Colors
    if groups:
        # If groups provided, color by community
        node_colors = [groups.get(n, 0) for n in G.nodes()]
        cmap = plt.cm.tab20  # Good disparate colormap
    elif nx.is_bipartite(G):
        # Bipartite default
        top = {n for n, d in G.nodes(data=True) if d.get('bipartite') == 0}
        node_colors = ['#1f77b4' if n in top else '#ff7f0e' for n in G.nodes()]
        cmap = None
        title += " (Blue=Cars, Orange=Parts)"
    else:
        # Default single color
        node_colors = 'skyblue'
        cmap = None

    # 2. Draw Nodes
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color=node_colors, cmap=cmap, alpha=0.9, edgecolors='black')
    
    # 3. Draw Labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    # 4. Draw Edges
    width = 1.0
    if weighted:
        # Scale width by weight
        weights = [G[u][v].get('weight', 1) for u, v in G.edges()]
        if weights:
            max_w = max(weights)
            width = [(w / max_w) * 4 + 0.5 for w in weights]
        else:
            width = 1.0
        
    nx.draw_networkx_edges(G, pos, width=width, alpha=0.3)
    
    if weighted:
        # Only show weights > 1 to avoid clutter, or top edges
        labels = nx.get_edge_attributes(G, 'weight')
        # Filter for high weights only?
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)

    plt.title(title, fontsize=18)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Graph saved to {filename}")
    plt.close()

def plot_criticality(parts_data, top_n=15, filename="criticality.png"):
    """
    Plots a bar chart of the top N critical parts.
    parts_data: list of (part_name, score)
    """
    top_parts = parts_data[:top_n]
    names = [p[0] for p in top_parts]
    scores = [p[1] for p in top_parts]
    
    plt.figure(figsize=(12, 8))
    plt.barh(names[::-1], scores[::-1], color='salmon')
    plt.xlabel("Number of Vehicles Using Part")
    plt.title(f"Top {top_n} Critical Parts (Hubs)", fontsize=16)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Criticality chart saved to {filename}")
    plt.close()

def plot_resilience_curve(stats, filename="resilience_curve.png"):
    """
    Plots the resilience curve (Giant Component Size vs Failed Parts).
    stats: [(num_failed, cars_rem, gc_size)]
    """
    x = [s[0] for s in stats]
    y = [s[2] for s in stats]  # GC Size
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='crimson', linewidth=2)
    plt.fill_between(x, y, color='crimson', alpha=0.1)
    
    plt.xlabel("Number of Critical Suppliers Failed")
    plt.ylabel("Size of Largest Connected Component")
    plt.title("Supply Chain Resilience Stress Test", fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Resilience curve saved to {filename}")
    plt.close()

def plot_k_core(G, core_numbers, filename="k_core.png"):
    """
    Plots the graph with nodes colored by their K-Core shell.
    """
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=2, seed=88)
    
    # Color based on Core Number
    cores = [core_numbers[n] for n in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color=cores, cmap=plt.cm.magma_r, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color='white')
    nx.draw_networkx_edges(G, pos, alpha=0.2, edge_color='#cccccc')
    
    plt.title("K-Core Decomposition (Yellow=Shell, Black=Core)", fontsize=16)
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.magma_r), ax=plt.gca(), label='K-Shellness')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"K-Core plot saved to {filename}")
    plt.close()


# ==================== NEW VISUALIZATIONS ====================

def plot_jaccard_heatmap(P, filename="fig7_jaccard_heatmap.png"):
    """
    Plots a heatmap of Jaccard similarity between vehicles.
    P: Projected graph with 'jaccard' edge attribute.
    """
    import numpy as np
    
    nodes = sorted(list(P.nodes()))
    n = len(nodes)
    matrix = np.zeros((n, n))
    
    # Fill matrix with Jaccard values
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i == j:
                matrix[i][j] = 1.0  # Self-similarity
            elif P.has_edge(u, v):
                matrix[i][j] = P[u][v].get('jaccard', 0)
            else:
                matrix[i][j] = 0
    
    plt.figure(figsize=(14, 12))
    
    # Create heatmap
    im = plt.imshow(matrix, cmap='YlOrRd', aspect='auto', vmin=0, vmax=1)
    
    # Add colorbar
    cbar = plt.colorbar(im, shrink=0.8)
    cbar.set_label('Índice de Jaccard', fontsize=12)
    
    # Add labels
    plt.xticks(range(n), nodes, rotation=90, fontsize=7)
    plt.yticks(range(n), nodes, fontsize=7)
    
    plt.title("Similaridade de Jaccard entre Veículos", fontsize=16)
    plt.xlabel("Veículos", fontsize=12)
    plt.ylabel("Veículos", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Jaccard heatmap saved to {filename}")
    plt.close()


def plot_degree_distribution(G, filename="fig8_degree_distribution.png", log_scale=True):
    """
    Plots the degree distribution histogram.
    If log_scale=True, uses log-log scale to reveal Power Law.
    """
    import numpy as np
    from collections import Counter
    
    degrees = [d for n, d in G.degree()]
    degree_counts = Counter(degrees)
    
    x = sorted(degree_counts.keys())
    y = [degree_counts[k] for k in x]
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Left: Linear histogram
    axes[0].bar(x, y, color='steelblue', edgecolor='black', alpha=0.8)
    axes[0].set_xlabel("Grau (k)", fontsize=12)
    axes[0].set_ylabel("Frequência", fontsize=12)
    axes[0].set_title("Distribuição de Graus (Escala Linear)", fontsize=14)
    axes[0].grid(True, alpha=0.3)
    
    # Right: Log-log plot (Power Law verification)
    if log_scale and min(x) > 0 and min(y) > 0:
        axes[1].scatter(x, y, color='crimson', s=80, edgecolors='black', alpha=0.8)
        axes[1].set_xscale('log')
        axes[1].set_yscale('log')
        axes[1].set_xlabel("Grau (k) [log]", fontsize=12)
        axes[1].set_ylabel("Frequência [log]", fontsize=12)
        axes[1].set_title("Distribuição de Graus (Log-Log) - Verificação Power Law", fontsize=14)
        axes[1].grid(True, which='both', alpha=0.3, linestyle='--')
        
        # Add trend line approximation
        if len(x) > 2:
            log_x = np.log10([k for k in x if k > 0])
            log_y = np.log10([degree_counts[k] for k in x if k > 0])
            if len(log_x) > 1:
                coeffs = np.polyfit(log_x, log_y, 1)
                axes[1].text(0.05, 0.95, f'γ ≈ {-coeffs[0]:.2f}', 
                           transform=axes[1].transAxes, fontsize=12,
                           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat'))
    else:
        axes[1].bar(x, y, color='crimson', edgecolor='black', alpha=0.8)
        axes[1].set_xlabel("Grau (k)", fontsize=12)
        axes[1].set_ylabel("Frequência", fontsize=12)
        axes[1].set_title("Distribuição de Graus", fontsize=14)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Degree distribution saved to {filename}")
    plt.close()


def plot_mixing_matrix(mixing_matrix, filename="fig9_mixing_matrix.png"):
    """
    Plots the assortativity mixing matrix as a heatmap.
    mixing_matrix: 2x2 numpy array from nx.attribute_mixing_matrix()
    """
    import numpy as np
    
    labels = ['Economy', 'Premium']
    
    plt.figure(figsize=(8, 6))
    
    im = plt.imshow(mixing_matrix, cmap='Blues', vmin=0, vmax=np.max(mixing_matrix))
    
    # Add colorbar
    cbar = plt.colorbar(im, shrink=0.8)
    cbar.set_label('Proporção de Arestas', fontsize=11)
    
    # Add labels
    plt.xticks([0, 1], labels, fontsize=12)
    plt.yticks([0, 1], labels, fontsize=12)
    
    # Add values in cells
    for i in range(2):
        for j in range(2):
            value = mixing_matrix[i, j]
            color = 'white' if value > np.max(mixing_matrix) / 2 else 'black'
            plt.text(j, i, f'{value:.3f}', ha='center', va='center', 
                    fontsize=16, fontweight='bold', color=color)
    
    plt.title("Matriz de Mistura: Segmentação de Mercado\n(Assortatividade por Segmento)", fontsize=14)
    plt.xlabel("Segmento de Destino", fontsize=12)
    plt.ylabel("Segmento de Origem", fontsize=12)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Mixing matrix saved to {filename}")
    plt.close()


def plot_local_clustering(G, local_clustering, filename="fig10_local_clustering.png"):
    """
    Plots local clustering coefficient for each node as a bar chart.
    local_clustering: dict from nx.clustering(G)
    """
    # Sort by clustering coefficient
    sorted_items = sorted(local_clustering.items(), key=lambda x: x[1], reverse=True)
    nodes = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]
    
    # Truncate labels if too long
    short_labels = [n[:20] + '...' if len(n) > 20 else n for n in nodes]
    
    plt.figure(figsize=(14, 8))
    
    colors = plt.cm.viridis([v for v in values])
    bars = plt.barh(range(len(nodes)), values, color=colors, edgecolor='black', alpha=0.8)
    
    plt.yticks(range(len(nodes)), short_labels, fontsize=8)
    plt.xlabel("Coeficiente de Clustering Local", fontsize=12)
    plt.ylabel("Veículos", fontsize=12)
    plt.title("Coeficiente de Clustering por Veículo\n(Maturidade de Plataforma)", fontsize=14)
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.6)
    cbar.set_label('Clustering', fontsize=10)
    
    plt.xlim(0, 1)
    plt.grid(True, axis='x', alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Local clustering chart saved to {filename}")
    plt.close()


def plot_bridges_and_cuts(G, bridges, articulation_points, filename="fig11_bridges_cuts.png"):
    """
    Plots the graph highlighting bridges (critical edges) and articulation points.
    bridges: list of edge tuples
    articulation_points: list of node names
    """
    plt.figure(figsize=(16, 12))
    
    try:
        pos = nx.kamada_kawai_layout(G)
    except:
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)
    
    # 1. Draw all edges first (light)
    regular_edges = [e for e in G.edges() if e not in bridges and (e[1], e[0]) not in bridges]
    nx.draw_networkx_edges(G, pos, edgelist=regular_edges, alpha=0.2, edge_color='#cccccc', width=1)
    
    # 2. Draw bridges (critical edges) in red
    bridge_set = set(bridges) | set((v, u) for u, v in bridges)  # Both directions
    bridge_edges = [e for e in G.edges() if e in bridge_set or (e[1], e[0]) in bridge_set]
    if bridge_edges:
        nx.draw_networkx_edges(G, pos, edgelist=bridge_edges, alpha=0.9, 
                              edge_color='red', width=3, style='solid')
    
    # 3. Draw regular nodes
    regular_nodes = [n for n in G.nodes() if n not in articulation_points]
    nx.draw_networkx_nodes(G, pos, nodelist=regular_nodes, node_size=400, 
                          node_color='skyblue', alpha=0.8, edgecolors='black')
    
    # 4. Draw articulation points (critical nodes) in red
    if articulation_points:
        nx.draw_networkx_nodes(G, pos, nodelist=articulation_points, node_size=700, 
                              node_color='red', alpha=0.9, edgecolors='darkred', linewidths=2)
    
    # 5. Draw labels
    nx.draw_networkx_labels(G, pos, font_size=7, font_weight='bold')
    
    # Add legend
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor='skyblue', edgecolor='black', label='Nó Regular'),
        Patch(facecolor='red', edgecolor='darkred', label=f'Ponto de Articulação ({len(articulation_points)})'),
        Line2D([0], [0], color='#cccccc', linewidth=2, label='Aresta Regular'),
        Line2D([0], [0], color='red', linewidth=3, label=f'Ponte ({len(bridges)})')
    ]
    plt.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    plt.title("Pontes e Pontos de Articulação\n(Elementos Críticos para Conectividade)", fontsize=16)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Bridges and cuts plot saved to {filename}")
    plt.close()


def plot_centrality_comparison(parts_data, filename="fig12_centrality_comparison.png"):
    """
    Scatter plot comparing Degree Centrality vs Betweenness Centrality.
    parts_data: list of tuples (part, degree, deg_cent, betweenness, eigenvector)
    """
    if not parts_data or len(parts_data[0]) < 5:
        print("Insufficient centrality data for comparison plot")
        return
    
    names = [p[0] for p in parts_data]
    degrees = [p[1] for p in parts_data]  # Raw degree for size
    betweenness = [p[3] for p in parts_data]  # Betweenness centrality
    eigenvector = [p[4] for p in parts_data]  # Eigenvector centrality
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    # Left: Degree vs Betweenness
    scatter1 = axes[0].scatter(degrees, betweenness, s=[d*30 for d in degrees], 
                               c=eigenvector, cmap='plasma', alpha=0.7, edgecolors='black')
    
    # Label top 5 points
    for i, (name, deg, betw) in enumerate(zip(names, degrees, betweenness)):
        if i < 5:  # Top 5
            axes[0].annotate(name[:15], (deg, betw), fontsize=8, 
                           xytext=(5, 5), textcoords='offset points')
    
    axes[0].set_xlabel("Grau (Número de Veículos)", fontsize=12)
    axes[0].set_ylabel("Centralidade de Intermediação", fontsize=12)
    axes[0].set_title("Grau vs Intermediação\n(Tamanho = Grau, Cor = Autovetor)", fontsize=14)
    axes[0].grid(True, alpha=0.3)
    cbar1 = plt.colorbar(scatter1, ax=axes[0], shrink=0.8)
    cbar1.set_label('Eigenvector', fontsize=10)
    
    # Right: Degree vs Eigenvector
    scatter2 = axes[1].scatter(degrees, eigenvector, s=[d*30 for d in degrees], 
                               c=betweenness, cmap='viridis', alpha=0.7, edgecolors='black')
    
    # Label top 5 points
    for i, (name, deg, eig) in enumerate(zip(names, degrees, eigenvector)):
        if i < 5:  # Top 5
            axes[1].annotate(name[:15], (deg, eig), fontsize=8, 
                           xytext=(5, 5), textcoords='offset points')
    
    axes[1].set_xlabel("Grau (Número de Veículos)", fontsize=12)
    axes[1].set_ylabel("Centralidade de Autovetor", fontsize=12)
    axes[1].set_title("Grau vs Autovetor\n(Tamanho = Grau, Cor = Intermediação)", fontsize=14)
    axes[1].grid(True, alpha=0.3)
    cbar2 = plt.colorbar(scatter2, ax=axes[1], shrink=0.8)
    cbar2.set_label('Betweenness', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"Centrality comparison saved to {filename}")
    plt.close()
