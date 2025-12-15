# Relatório de Análise de Grafos: Cadeia de Suprimentos Automotiva
**Data:** 15/12/2025 10:47

## 1. Contextualização e Modelagem
Este relatório utiliza propriedades avançadas de Teoria dos Grafos para diagnosticar a maturidade e riscos da cadeia.
- **Total de Veículos Analisados:** 36
- **Total de Peças Únicas:** 48
- **Média de Peças por Veículo:** 3.9

## 2. Agrupamentos Naturais (Clusters)
> *Pergunta: Quais agrupamentos naturais de veículos existem segundo compartilhamento de peças?*

Utilizando **Modularity Maximization**, identificamos **3 plataformas virtuais**:

### Família 1 (Tam: 25)
- **Veículos:** VW Touareg 7L, Toyota Corolla, Honda Civic, VW Golf Mk7, Porsche Cayenne, Mercedes E-Class (W213), Nissan Qashqai J11, Nissan Micra K14 ...
### Família 2 (Tam: 7)
- **Veículos:** Toyota RAV4, Peugeot 3008, Citroen C3, Volvo XC60, Mercedes C-Class, Peugeot 208, Opel Corsa F 
### Família 3 (Tam: 4)
- **Veículos:** Ford Focus, Audi A3 8P, Ford Kuga, Volvo XC40 

## 3. Análise de Vitalidade (Hubs e Gargalos)
> *Pergunta: Quais peças são vitais por volume e quais são gargalos estratégicos?*

Diferenciamos peças por duas métricas de centralidade:
1. **Degree Centrality:** Volume absoluto de uso (Economia de Escala).
2. **Betweenness Centrality:** Peças que conectam famílias diferentes (Risco de Contágio).

| Rank | Peça (Hub) | Uso (Degree) | Importância (Eigen) | Gargalo (Betweenness) |
|---|---|---|---|---|
| 1 | Sistema ABS Bosch | 28 | 0.562 | 0.648 |
| 2 | Suspensão Multilink | 9 | 0.213 | 0.023 |
| 3 | Turbocompressor KKK | 8 | 0.200 | 0.020 |
| 4 | Transmissão DSG DQ250 | 6 | 0.142 | 0.006 |
| 5 | Motor EA888 2.0T | 4 | 0.099 | 0.001 |
| 6 | Central Multimídia MIB | 4 | 0.096 | 0.002 |
| 7 | Plataforma CMP | 4 | 0.019 | 0.023 |
| 8 | Motor PureTech 1.2 | 4 | 0.019 | 0.023 |
| 9 | Controle de Estabilidade ESP | 4 | 0.031 | 0.046 |
| 10 | Motor EA111 1.6 | 3 | 0.059 | 0.001 |

## 4. Análise de Resiliência e Falhas
Simulação de falha da peça principal **'Sistema ABS Bosch'**:
- **Impacto Direto:** 28 veículos parariam a produção.
- **Severidade:** 77.8% da frota analisada.

## 5. Eficiência de Estoque
- **Redução de SKUs:** 65.7% em comparação a estoques independentes.

## 6. Topologia Avançada e Coesão
> *Pergunta: Quão maduras são as plataformas e os compartilhamentos?*

- **Coeficiente de Clustering Médio (0.901):** Indica a probabilidade de que dois carros que compartilham peças com um terceiro também compartilhem entre si. Alto valor sugere plataformas bem definidas.
- **Transitividade (0.949):** Reforça a análise de coesão global.

**Índice de Similaridade de Jaccard (Exemplo):**
Normaliza o compartilhamento pelo tamanho total dos veículos, evitando viés de complexidade.
- **Renault Clio IV ↔ Nissan Micra K13:** J = 1.00 (Compartilham 3 peças)
- **Renault Clio IV ↔ Renault Captur:** J = 1.00 (Compartilham 3 peças)
- **Nissan Micra K13 ↔ Renault Captur:** J = 1.00 (Compartilham 3 peças)

## 7. Segmentação de Mercado (Assortatividade)
> *Pergunta: A estratégia de peças respeita a segmentação de mercado (Premium vs Economy)?*

- **Assortatividade por Segmento:** -0.008
  *Interpretação:* Neutra. O compartilhamento independe do segmento mercadológico.
