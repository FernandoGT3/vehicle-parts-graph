
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
