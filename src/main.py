import networkx as nx
from . import graph_ops
from . import visualizer
from . import report_generator
from .data import V_CARROS, V_PECAS

def main():
    print("Loading data and building graphs...")
    B = graph_ops.build_bipartite_graph()
    P = graph_ops.build_projected_graph(B)
    
    while True:
        # clear_screen()
        print("\n" + "="*50)
        print("Vehicle Graph Theory Analysis System (Advanced)")
        print("="*50)
        print(f"Data Loaded: {len(V_CARROS)} Cars, {len(V_PECAS)} Parts")
        print("-" * 50)
        print("1.  [Basic] Show Bipartite Graph Info")
        print("2.  [Basic] Show Projected Graph Info")
        print("3.  [Basic] Analyze Degrees (Max/Min)")
        print("4.  [Basic] Minimum Spanning Tree (Max Sharing)")
        print("5.  [Advanced] Detect Communities (Car Families)")
        print("6.  [Advanced] Identify Hubs (Critical Parts)")
        print("7.  [Advanced] Resilience Test (Simulate Failure)")
        print("8.  [Reporting] Generate Full Report for Article")
        print("9.  [Visuals] Generate All Visualizations")
        print("10. Exit")
        print("="*50)
        
        choice = input("Enter choice (1-10): ").strip()
        
        if choice == '1':
            print("\n[Bipartite Graph Info]")
            print(graph_ops.get_graph_info(B))
            
        elif choice == '2':
            print("\n[Projected Graph Info]")
            print(graph_ops.get_graph_info(P))
            print("Density:", nx.density(P))
            
        elif choice == '3':
            print("\n[Degree Analysis - Projected Graph]")
            degrees = graph_ops.get_degrees(P)
            print("Top 5 Connected Cars:")
            for n, d in degrees[:5]:
                print(f"  {n}: {d}")
                
        elif choice == '4':
            print("\n[Maximum Spanning Tree]")
            T = graph_ops.get_mst(P)
            print(f"MST Edges: {T.number_of_edges()}")
            print("Backbone Edges (Strongest Links):")
            for u, v, d in list(T.edges(data=True))[:5]:
                print(f"  {u} - {v} (Weight: {d.get('weight')})")
                
        elif choice == '5':
            print("\n[Community Detection - Natural Clusters]")
            comm_map, comms = graph_ops.detect_communities(P)
            print(f"Detected {len(comms)} communities:")
            for i, c in enumerate(comms):
                print(f"  Family {i+1}: {list(c)[:5]}...")
                
        elif choice == '6':
            print("\n[Hub Identification - Critical Parts]")
            hubs = graph_ops.get_part_criticality(B)
            print("Top 10 Critical Parts:")
            for i, (p, d) in enumerate(hubs[:10]):
                print(f"  {i+1}. {p} (Used by {d} cars)")

        elif choice == '7':
            print("\n[Resilience Simulation]")
            hubs = graph_ops.get_part_criticality(B)
            top_part = hubs[0][0]
            print(f"Simulating failure of top part: {top_part}")
            affected, sev = graph_ops.simulate_part_failure(B, top_part)
            print(f"Impact: {len(affected)} cars affected ({sev*100:.1f}%)")
            print(f"Cars: {affected[:5]}...")
            
        elif choice == '8':
            print("\n[Generating Full Report]")
            report_generator.generate_full_report(B, P)
            print("Generated 'relatorio_completo.md'.")
            
        elif choice == '9':
            print("\n[Generating Visualizations]")
            # Bipartite
            visualizer.plot_graph(B, title="Automotive Supply Chain (Bipartite)", filename="bipartite.png")
            
            # Projected with Communities
            comm_map, _ = graph_ops.detect_communities(P)
            visualizer.plot_graph(P, title="Vehicle Clusters (Projected)", filename="clusters.png", groups=comm_map, weighted=True)
            
            # MST
            T = graph_ops.get_mst(P)
            visualizer.plot_graph(T, title="Industry Backbone (MaxST)", filename="backbone.png", weighted=True)
            
            # Criticality Chart
            hubs = graph_ops.get_part_criticality(B)
            visualizer.plot_criticality(hubs, filename="criticality_chart.png")
            print("Done! Check PNG files.")
            
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
