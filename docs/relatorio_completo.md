# Relatório de Análise de Grafos: Cadeia de Suprimentos Automotiva
**Data:** 10/12/2025 21:59

## 1. Contextualização e Modelagem
Este relatório utiliza Teoria dos Grafos para responder perguntas estratégicas sobre compartilhamento de peças.
- **Total de Veículos Analisados:** 36
- **Total de Peças Únicas:** 48
- **Média de Peças por Veículo (no dataset):** 3.9

## 2. Agrupamentos Naturais (Clusters)
> *Pergunta: Quais agrupamentos naturais de veículos existem segundo compartilhamento de peças?*

Utilizando algoritmos de detecção de comunidades (Modularity Maximization), identificamos **3 famílias principais** de veículos:

### Família 1 (Tam: 25)
- **Veículos:** Renault Captur, Nissan Micra K13, Toyota Corolla, Porsche Cayenne, Fiat Toro, BMW X3, Honda CR-V, Jeep Renegade ...
- **Identificação Provável:** Plataforma MQB (VW Group)

### Família 2 (Tam: 7)
- **Veículos:** Citroen C3, Toyota RAV4, Opel Corsa F, Mercedes C-Class, Volvo XC60, Peugeot 208, Peugeot 3008 
- **Identificação Provável:** Grupo Misture

### Família 3 (Tam: 4)
- **Veículos:** Ford Focus, Audi A3 8P, Ford Kuga, Volvo XC40 
- **Identificação Provável:** Grupo Misture

## 3. Identificação de Hubs (Peças Críticas)
> *Pergunta: Quais peças são “hubs” — usadas por muitos veículos?*

As peças com maior **Grau de Centralidade** (conectadas a mais veículos) são:

| Rank | Peça (Hub) | Veículos Afetados |
|---|---|---|
| 1 | Sistema ABS Bosch | 28 |
| 2 | Suspensão Multilink | 9 |
| 3 | Turbocompressor KKK | 8 |
| 4 | Transmissão DSG DQ250 | 6 |
| 5 | Motor EA888 2.0T | 4 |

Essas peças representam o maior risco de gargalo, mas também a maior oportunidade de economia de escala.

## 4. Análise de Resiliência e Falhas
> *Pergunta: Se uma peça crítica ficar indisponível, quantos veículos ficam afetados?*

Simulação de falha da peça **'Sistema ABS Bosch'**:
- **Impacto Direto:** 28 veículos parariam a produção.
- **Severidade:** 77.8% da frota analisada.
- **Lista de Afetados:** VW Golf Mk6, Audi A3 8P, Audi TT Mk2, VW Polo Mk5, Porsche Cayenne...

## 5. Otimização de Estoques
> *Pergunta: Como minimizar custo total de estoque?*

A análise comparativa entre SKUs únicos e demanda total mostra o ganho da estratégia de plataforma:

- **Total de Peças Necessárias (sem compartilhamento):** 140
- **Total de SKUs Reais (com compartilhamento):** 48
- **Fator de Redução de Estoque:** 65.7%

Isso indica que a estratégia de compartilhamento está reduzindo a complexidade logística significativamente.
