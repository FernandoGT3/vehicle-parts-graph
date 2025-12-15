# Vehicle Parts Graph Analysis

**Análise Topológica e Resiliência na Cadeia de Suprimentos Automotiva via Teoria dos Grafos**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-green.svg)](https://networkx.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Visão Geral

Este projeto aplica **Teoria dos Grafos Complexos** para modelar e analisar a estrutura oculta de compartilhamento de componentes na indústria automotiva. A análise revela como a estratégia de "plataformas modulares" cria interdependências que, embora reduzam custos, introduzem riscos sistêmicos significativos.

### Principais Descobertas

- **65.7% de redução** na complexidade de estoque
- **77% de vulnerabilidade** - um único componente pode paralisar a maioria da frota
- **3 clusters industriais** detectados automaticamente (VW Group, Renault-Nissan/Stellantis, Premium/Asiáticos)
- **Super-Hub identificado**: Sistema ABS Bosch (presente em 28 de 36 veículos)

---

## Arquitetura do Projeto

```
vehicle-parts/
├── src/
│   ├── __init__.py              # Inicialização do pacote
│   ├── data.py                  # Dataset: veículos, peças e relações
│   ├── graph_ops.py             # Operações de grafos e métricas
│   ├── visualizer.py            # Geração de visualizações
│   ├── report_generator.py      # Gerador de relatórios automáticos
│   ├── article_generator.py     # Gerador do artigo científico
│   └── main.py                  # Interface interativa (CLI)
├── docs/
│   ├── artigo_final.md          # Artigo em Markdown
│   ├── artigo_final.tex         # Artigo em LaTeX
│   └── relatorio_completo.md    # Relatório detalhado gerado
├── assets/                      # Figuras geradas (PNG)
├── tests/
│   └── test_sanity.py           # Testes básicos
├── requirements.txt             # Dependências
├── pyproject.toml               # Configuração do projeto
├── LICENSE                      # Licença MIT
└── README.md                    # Este arquivo
```

---

## Funcionalidades

### Modelagem de Grafos

| Funcionalidade | Descrição |
|----------------|-----------|
| **Grafo Bipartido** | Modela relações Veículo ↔ Peça |
| **Grafo Projetado** | Relações Veículo ↔ Veículo (baseado em peças compartilhadas) |
| **Pesos de Aresta** | Número de peças compartilhadas entre veículos |

### Métricas de Análise

| Métrica | Implementação | Arquivo |
|---------|---------------|---------|
| Detecção de Comunidades | Greedy Modularity Maximization | `graph_ops.detect_communities()` |
| Centralidade de Grau | Degree Centrality | `graph_ops.get_part_criticality()` |
| Centralidade de Intermediação | Betweenness Centrality | `graph_ops.get_part_criticality()` |
| Centralidade de Autovetor | Eigenvector Centrality | `graph_ops.get_part_criticality()` |
| Assortatividade | Attribute Assortativity (Premium/Economy) | `graph_ops.calculate_assortativity()` |
| Decomposição K-Core | K-Shell Analysis | `graph_ops.get_k_core_decomposition()` |
| Coeficiente de Clustering | Average Clustering | `graph_ops.get_clustering_analysis()` |
| Similaridade de Jaccard | Jaccard Index para pares | `graph_ops.calculate_jaccard_weights()` |
| Árvore Geradora Máxima | Maximum Spanning Tree | `graph_ops.get_mst()` |

### Simulações

| Simulação | Descrição |
|-----------|-----------|
| Falha de Peça Individual | Impacto da remoção de uma peça específica |
| Colapso de Fornecedor | Impacto da remoção de múltiplas peças |
| Falha em Cascata | Remoção sequencial dos top hubs |

### Predição

| Funcionalidade | Descrição |
|----------------|-----------|
| Recomendação de Padronização | Sugere peças "faltantes" baseado no cluster |
| Análise de Eficiência de Estoque | Calcula economia de SKUs |

---

## Requisitos

### Dependências

```
Python >= 3.8
networkx >= 3.0
matplotlib >= 3.5
```

### Instalação

```bash
# Clone o repositório
git clone https://github.com/FernandoGT3/vehicle-parts-graph.git
cd vehicle-parts-graph

# Crie um ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## Como Executar

### Interface Interativa (Recomendado)

```bash
python -m src.main
```

O menu interativo oferece as seguintes opções:

```
==================================================
Vehicle Graph Theory Analysis System (Advanced)
==================================================
1.  [Basic] Show Bipartite Graph Info
2.  [Basic] Show Projected Graph Info
3.  [Basic] Analyze Degrees (Max/Min)
4.  [Basic] Minimum Spanning Tree (Max Sharing)
5.  [Advanced] Detect Communities (Car Families)
6.  [Advanced] Identify Hubs (Critical Parts)
7.  [Advanced] Resilience Test (Simulate Failure)
8.  [Reporting] Generate Full Report for Article
9.  [Visuals] Generate All Visualizations
11. [Extra] Advanced Topology Metrics (New)
10. Exit
==================================================
```

### Gerar Relatório Completo

```bash
python -c "from src import graph_ops, report_generator; B = graph_ops.build_bipartite_graph(); P = graph_ops.build_projected_graph(B); report_generator.generate_full_report(B, P)"
```

### Gerar Artigo Científico

```bash
python -m src.article_generator
```

Isso gera:
- `docs/artigo_final.tex` - Versão LaTeX
- Figuras em alta resolução (`fig1_network.png`, `fig2_clusters.png`, etc.)

### Gerar Visualizações

```bash
python -c "
from src import graph_ops, visualizer

B = graph_ops.build_bipartite_graph()
P = graph_ops.build_projected_graph(B)
comm_map, _ = graph_ops.detect_communities(P)

visualizer.plot_graph(B, title='Rede Bipartida', filename='bipartite.png')
visualizer.plot_graph(P, title='Clusters', filename='clusters.png', groups=comm_map, weighted=True)
"
```

---

## Testes

```bash
# Executar testes básicos
python -m pytest tests/

# ou diretamente
python tests/test_sanity.py
```

---

## Dataset

O dataset atual inclui:

- **36 Veículos** de múltiplas montadoras:
  - VW Group (Golf, Polo, Audi A3, TT, Q7, Touareg, Porsche Cayenne)
  - Renault-Nissan (Clio, Captur, Micra, Qashqai, Kadjar)
  - Stellantis (Jeep Compass, Renegade, Fiat Toro, Peugeot 208/3008, Citroen C3, Opel Corsa)
  - Premium (BMW X3/3-Series, Mercedes C/E-Class, Volvo XC40/XC60)
  - Asiáticos (Toyota Corolla/RAV4, Honda Civic/CR-V)
  - Ford (Focus, Kuga)

- **48 Peças/Sistemas**:
  - Plataformas (MQB, PQ35, PQ25, CMF-B, CMP, TNGA, CMA, etc.)
  - Motores (EA888, EA111, VTEC, EcoBoost, PureTech, etc.)
  - Transmissões (DSG, CVT, e-CVT, PowerShift, etc.)
  - Sistemas (ABS Bosch, ESP, Airbags, etc.)
  - Componentes Premium (Som Bose, Farol LED Matrix, etc.)

---

## Exemplos de Uso

### Análise Básica

```python
from src import graph_ops

# Construir grafos
B = graph_ops.build_bipartite_graph()  # Grafo Bipartido
P = graph_ops.build_projected_graph(B)  # Grafo Projetado

# Informações básicas
print(graph_ops.get_graph_info(B))
print(graph_ops.get_graph_info(P))
```

### Detectar Comunidades

```python
from src import graph_ops

B = graph_ops.build_bipartite_graph()
P = graph_ops.build_projected_graph(B)

comm_map, communities = graph_ops.detect_communities(P)
print(f"Comunidades detectadas: {len(communities)}")
for i, c in enumerate(communities):
    print(f"  Família {i+1}: {list(c)[:5]}...")
```

### Identificar Peças Críticas

```python
from src import graph_ops

B = graph_ops.build_bipartite_graph()
critical = graph_ops.get_part_criticality(B)

print("Top 5 Peças Críticas:")
for part, degree, deg_cent, betw, eigen in critical[:5]:
    print(f"  {part}: {degree} veículos (Betweenness: {betw:.3f})")
```

### Simular Falha

```python
from src import graph_ops

B = graph_ops.build_bipartite_graph()

# Simular falha do ABS Bosch
affected, severity = graph_ops.simulate_part_failure(B, "Sistema ABS Bosch")
print(f"Veículos afetados: {len(affected)} ({severity*100:.1f}%)")
```

### Análise de Segmentação

```python
from src import graph_ops

B = graph_ops.build_bipartite_graph()
P = graph_ops.build_projected_graph(B)

coeff, mixing = graph_ops.calculate_assortativity(P)
print(f"Assortatividade Premium/Economy: {coeff:.4f}")
# Valor ~0: homogeneização tecnológica
# Valor >0: segregação (Premium só compartilha com Premium)
# Valor <0: compartilhamento cruzado
```

---

## Limitações Conhecidas

1. **Dataset representativo**: Cobre 36 veículos; não representa a totalidade do mercado global
2. **Pesos uniformes**: Arestas não diferenciam criticidade individual de cada peça
3. **Análise estática**: Não modela evolução temporal da rede
4. **Fornecedores**: Não inclui cadeia de segundo/terceiro nível

---

## Próximos Passos

- [ ] Modelagem temporal (evolução da rede ao longo dos anos)
- [ ] Pesos diferenciados por criticidade (peça de segurança vs conforto)
- [ ] Simulações de Monte Carlo para análise probabilística
- [ ] Inclusão de fornecedores de segundo e terceiro nível
- [ ] Interface web interativa (Dashboard)
- [ ] Exportação para formatos padrão (GraphML, GEXF)

---

## Referências

- Newman, M. E. J. (2010). *Networks: An Introduction*. Oxford University Press.
- Barabási, A.-L. (2016). *Network Science*. Cambridge University Press.
- Documentação NetworkX: https://networkx.org/documentation/

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

---

## Autores

- **Caio Bonani** - Desenvolvimento e Análise
- **Luiz Fernando de Cristo Moloni** - Desenvolvimento e Análise
