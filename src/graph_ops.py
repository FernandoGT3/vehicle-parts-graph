
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
from .data import V_CARROS, V_PECAS, EDGES_BIPARTIDO

def build_bipartite_graph():
    """Builds the Bipartite Graph (Cars + Parts)."""
    B = nx.Graph()
    B.add_nodes_from(V_CARROS, bipartite=0, type='car')
    B.add_nodes_from(V_PECAS, bipartite=1, type='part')
    B.add_edges_from(EDGES_BIPARTIDO)
    return B

def build_projected_graph(B):
    """Builds the Projected Graph (Car-to-Car) based on shared parts."""
    P = nx.Graph()
    P.add_nodes_from(V_CARROS)
    
    # Manually calculate to add weights and details
    for i in range(len(V_CARROS)):
        u = V_CARROS[i]
        u_parts = set(n for n in B.neighbors(u))
        for j in range(i + 1, len(V_CARROS)):
            v = V_CARROS[j]
            v_parts = set(n for n in B.neighbors(v))
            
            shared = u_parts.intersection(v_parts)
            if shared:
                P.add_edge(u, v, weight=len(shared), shared_parts=list(shared))
                
    return P

def get_graph_info(G):
    """Returns basic info string."""
    info = f"Nodes: {G.number_of_nodes()}\n"
    info += f"Edges: {G.number_of_edges()}\n"
    info += f"Density: {nx.density(G):.4f}\n"
    if nx.is_connected(G):
        info += "Connected: Yes\n"
        info += f"Diameter: {nx.diameter(G)}\n"
        center = nx.center(G)
        info += f"Center: {center}\n"
        info += f"Avg Path Length: {nx.average_shortest_path_length(G):.4f}\n"
    else:
        info += "Connected: No\n"
        info += f"Connected Components: {nx.number_connected_components(G)}\n"
        
    return info

def get_degrees(G):
    """Returns sorted degrees."""
    degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)
    return degrees

def get_mst(G):
    """Returns Maximum Spanning Tree."""
    if G.number_of_edges() == 0:
        return nx.Graph()
    return nx.maximum_spanning_tree(G)

def get_bridges_and_cuts(G):
    """Returns bridges and articulation points."""
    try:
        bridges = list(nx.bridges(G))
        articulation_points = list(nx.articulation_points(G))
        return bridges, articulation_points
    except:
        return [], []

# ==================== ADVANCED ANALYSIS (TG.txt) ====================

def detect_communities(G):
    """
    Detects communities (Clusters/Platforms) using Greedy Modularity.
    Returns a dictionary mapping node -> community_id.
    """
    communities = list(greedy_modularity_communities(G))
    community_map = {}
    for i, c in enumerate(communities):
        for node in c:
            community_map[node] = i
    return community_map, communities

def get_part_criticality(B):
    """
    Identifies 'Hubs' (Parts) by calculating Degree Centrality on the Bipartite Graph.
    Returns sorted list of (part, centrality_score, raw_degree).
    """
    # Filter only part nodes
    parts = [n for n, d in B.nodes(data=True) if d.get('type') == 'part']
    
    # We can use simple degree or degree centrality
    criticality = []
    for p in parts:
        degree = B.degree(p)
        # Calculate how many unique car families this part connects
        neighbors = list(B.neighbors(p))
        criticality.append((p, degree))
        
    return sorted(criticality, key=lambda x: x[1], reverse=True)

def simulate_part_failure(B, part_node):
    """
    Simulates the failure of a specific part.
    Returns:
    - affected_cars: List of cars that rely on this part.
    - severity_score: Proportion of total cars affected.
    """
    if part_node not in B:
        return [], 0.0
    
    affected_cars = list(B.neighbors(part_node))
    severity = len(affected_cars) / len(V_CARROS) if V_CARROS else 0
    return affected_cars, severity

def simulate_supplier_collapse(B, parts_to_fail):
    """
    Simulates collapse of a supplier providing multiple parts.
    Returns the impact on the projected graph connectivity.
    """
    # Create copy of bipartite graph without these parts
    B_damaged = B.copy()
    B_damaged.remove_nodes_from(parts_to_fail)
    
    # Rebuild projected graph to see connectivity loss
    P_damaged = build_projected_graph(B_damaged)
    
    # Measure fragmentation
    num_components = nx.number_connected_components(P_damaged)
    largest_cc = len(max(nx.connected_components(P_damaged), key=len)) if len(P_damaged) > 0 else 0
    
    return num_components, largest_cc, P_damaged

def analyze_stock_savings(B):
    """
    Calculates stock savings vs independent stock.
    Stock Reduction = 1 - (Unique Parts / Sum of Parts per Car)
    """
    unique_parts = len(V_PECAS)
    
    sum_parts_needed = 0
    for car in V_CARROS:
        sum_parts_needed += B.degree(car)
        
    reduction_factor = 1 - (unique_parts / sum_parts_needed) if sum_parts_needed > 0 else 0
    return sum_parts_needed, unique_parts, reduction_factor

def simulate_cumulative_failure(B, parts_list):
    """
    Simulates sequential failure of parts in the list.
    Returns a list of stats: [(num_parts_failed, cars_remaining, giant_component_size)]
    """
    stats = []
    
    # Initial State
    total_cars = len(V_CARROS)
    g_size = len(max(nx.connected_components(build_projected_graph(B)), key=len)) if len(V_CARROS) > 0 else 0
    stats.append((0, total_cars, g_size))
    
    current_B = B.copy()
    failed_parts = set()
    
    for part in parts_list:
        if part in current_B:
            # "Failure" means the part is gone. 
            # Cars relying on it might be considered "STOPPED"
            # For this sim, let's track Connectivity of the Remaining production capability
            current_B.remove_node(part)
            failed_parts.add(part)
            
            # Rebuild projected graph to check industry connectivity
            P = build_projected_graph(current_B)
            if len(P) > 0:
                gc = len(max(nx.connected_components(P), key=len))
            else:
                gc = 0
                
            # Count cars that have lost at least 1 connection to a part?
            # Or just count connectivity? Let's use GC size as a proxy for "functional industry network"
            stats.append((len(failed_parts), len(P), gc))
            
    return stats

# ==================== NEW ADVANCED LOGIC (EXPANSION) ====================

def get_vehicle_segments():
    """Manual mapping of vehicles to market segments."""
    segments = {}
    for v in V_CARROS:
        if any(x in v for x in ['Audi', 'BMW', 'Mercedes', 'Porsche', 'Volvo', 'Jeep']):
            segments[v] = 'Premium'
        else:
            segments[v] = 'Economy'
    return segments

def calculate_assortativity(G):
    """
    Calculates the assortativity coefficient based on vehicle segment.
    Do Premium cars only connect to Premium cars?
    """
    segments = get_vehicle_segments()
    nx.set_node_attributes(G, segments, 'segment')
    
    # Calculate numeric assortativity
    coeff = nx.attribute_assortativity_coefficient(G, 'segment')
    
    # Calculate mixing matrix
    mixing_matrix = nx.attribute_mixing_matrix(G, 'segment', mapping={'Economy': 0, 'Premium': 1})
    
    return coeff, mixing_matrix

def get_k_core_decomposition(G):
    """
    Decomposes the graph into k-shells.
    Returns the core number for each node and the max k-core subgraph.
    """
    core_numbers = nx.core_number(G)
    max_k = max(core_numbers.values())
    k_core_subgraph = nx.k_core(G, k=max_k)
    
    return core_numbers, k_core_subgraph, max_k

def predict_demand(B, communities):
    """
    Predicts missing parts for vehicles based on their community standard.
    Returns: {Community_ID: [Common_Parts]}, {Vehicle: [Suggested_Parts]}
    """
    # 1. Identify "Standard Parts" for each community (present in >70% of members)
    comm_standards = {}
    suggestions = {}
    
    for i, comm_nodes in enumerate(communities):
        if len(comm_nodes) < 2: continue
        
        # Count part frequency in this community
        part_counts = {}
        for car in comm_nodes:
            parts = list(B.neighbors(car))
            for p in parts:
                part_counts[p] = part_counts.get(p, 0) + 1
        
        # Filter parts that define this cluster (Threshold 70%)
        standard_parts = [p for p, count in part_counts.items() if count >= len(comm_nodes) * 0.7]
        comm_standards[i] = standard_parts
        
        # 2. Find Gaps (Which car is missing a standard part?)
        for car in comm_nodes:
            existing = set(B.neighbors(car))
            missing = [p for p in standard_parts if p not in existing]
            if missing:
                suggestions[car] = missing
                
    return comm_standards, suggestions
