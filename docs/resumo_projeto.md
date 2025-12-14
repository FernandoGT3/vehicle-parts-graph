# Resumo do Projeto: Gráfos de Compatibilidade de Peças de Veículos

## Visão Geral
Este projeto utiliza Teoria dos Grafos para modelar e analisar a compatibilidade e compartilhamento de peças entre diferentes modelos de veículos. O objetivo é identificar "famílias" de veículos, gargalos de produção (peças críticas) e o grau de intercambialidade na indústria automotiva.

## Modelagem
O problema foi modelado de duas formas principais:

1.  **Grafo Bipartido $G = (U \cup W, E)$**:
    *   $U$: Conjunto de Veículos (36 modelos, ex: VW Golf, Toyota Corolla, Volvo XC60).
    *   $W$: Conjunto de Peças (48+ tipos, ex: Plataforma MQB, Motor VTEC 1.5, Sensor Lidar).
    *   $E$: Arestas representando que o veículo $u$ utiliza a peça $w$.
    *   **Total de Nós**: ~84.

2.  **Grafo Projetado (Veículo-Veículo) $P$**:
    *   Projeção do grafo bipartido sobre o conjunto $U$ de veículos.
    *   Dois veículos são conectados se compartilham pelo menos uma peça.
    *   **Pesos**: O peso da aresta representa a *quantidade* de peças compartilhadas (força da conexão).

## Funcionalidades Implementadas (`src/`)

### Estrutura do Código
*   `vehicle_parts.py`: Base de dados expandida (apenas dados).
*   `src/graph_ops.py`: Motor de processamento usando `networkx`. Implementa construção dos grafos, cálculo de graus, MST, componentes conexos e cortes.
*   `src/visualizer.py`: Motor de renderização usando `matplotlib`.
*   `src/menu.py`: Interface interativa via terminal.

### Análises Disponíveis
*   **Graus e Centralidade**: Identificação dos carros mais "universais" (que compartilham mais peças) e os mais "isolados".
*   **Árvore Geradora (MST/MaxST)**: Visualização da "espinha dorsal" da indústria, conectando os carros pelas relações mais fortes.
*   **Componentes Conexos**: Agrupamento automático de veículos por alianças (ex: Grupo VW, Stellantis, Aliança Renault-Nissan).
*   **Pontes e Cortes**: Identificação de conexões frágeis entre grupos maiores.

## Como Executar
1.  Certifique-se de ter o `uv` instalado.
2.  Instale as dependências: `uv sync` ou use o ambiente virtual criado.
3.  Execute o menu:
    ```bash
    uv run python src/menu.py
    ```
4.  Escolha as opções no menu para gerar relatórios e visualizar os grafos (imagens `.png` serão salvas na raiz).

## Resultados Esperados
Ao executar a visualização, observa-se claramente a formação de clusters baseados nas plataformas (MQB, TNGA, CMP, etc.), demonstrando a estratégia de modularização das grandes montadoras.
