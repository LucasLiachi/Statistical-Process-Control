# Exercícios Completos - Controle Estatístico de Processo

## Índice

1. [Exercício 1 - Cartas de Controle Básicas](#exercício-1---cartas-de-controle-básicas)
2. [Exercício 2 - Análise Avançada de Processo](#exercício-2---análise-avançada-de-processo)
3. [Exercício 3 - Índices de Capacidade de Processo](#exercício-3---índices-de-capacidade-de-processo)
4. [Exercício 4 - CEP por Batelada](#exercício-4---cep-por-batelada)

---

# Exercício 1 - Cartas de Controle Básicas

## Enunciado

Olá, estudante!

Este é o momento em que você colocará a mão na massa. Na proposta a seguir, você será convidado(a) a realizar uma atividade prática aplicando os conteúdos estudados até aqui.

### Habilidades Contempladas

- Compreensão teórica das expressões matemáticas para definição dos limites de controle tanto para cartas de média quanto para cartas de amplitude;
- Aplicação prática dessas expressões e conhecimento dos limites de controle.

### Situação Problema

Como parte integrante de uma equipe de melhoria de processos, você participa como suporte técnico de um grupo de estudo que busca avaliar um processo de usinagem específico e, junto com seus colegas, recebe os dados de um lote-piloto de cem peças produzidas por um equipamento previamente definido. Com os respectivos dados em mãos, a equipe deve realizar uma análise estatística, a fim de determinar os limites de controle para as duas cartas de controle por variável, sendo uma para média e outra para amplitude.

**Especificações da Peça:**
- Eixo usinado em centro de usinagens
- Material: aço AISI 410
- Comprimento total especificado: 140 mm
- Tolerância: ± 4mm

### Dados das Amostras

| Itens obs. | 1   | 2   | 3   | 4   | 5   |
|------------|-----|-----|-----|-----|-----|
| 1          | 137 | 145 | 143 | 137 | 138 |
| 2          | 141 | 142 | 147 | 140 | 140 |
| 3          | 142 | 137 | 145 | 140 | 132 |
| 4          | 137 | 147 | 142 | 137 | 135 |
| 5          | 137 | 146 | 142 | 142 | 140 |
| 6          | 140 | 137 | 135 | 135 | 140 |
| 7          | 137 | 145 | 144 | 137 | 140 |
| 8          | 144 | 142 | 143 | 135 | 144 |
| 9          | 142 | 135 | 144 | 145 | 141 |
| 10         | 132 | 135 | 136 | 140 | 145 |
| 11         | 137 | 142 | 142 | 145 | 143 |
| 12         | 142 | 142 | 143 | 140 | 135 |
| 13         | 136 | 142 | 140 | 139 | 137 |
| 14         | 144 | 145 | 144 | 140 | 143 |
| 15         | 139 | 146 | 143 | 140 | 139 |
| 16         | 141 | 146 | 143 | 140 | 140 |
| 17         | 130 | 140 | 143 | 140 | 140 |
| 18         | 138 | 145 | 141 | 137 | 141 |
| 19         | 140 | 145 | 143 | 144 | 138 |
| 20         | 145 | 145 | 140 | 140 | 143 |

### Fórmulas a Utilizar

**Cálculos básicos:**
- X̄ = (x₁ + x₂ + ... + xₙ)/n
- R = xMáximo - xMínimo  
- R̄ = (R₁ + R₂ + ... + Rₙ)/n
- X̿ = (X̄₁ + X̄₂ + ... + X̄ₙ)/n

**Limites de controle para carta da média:**
- LSC = X̿ + A₂.R̄
- LIC = X̿ - A₂.R̄
- LC = X̿

**Limites de controle para carta da amplitude:**
- LSC = D₄.R̄
- LIC = D₃.R̄
- LC = R̄

### Fatores para Cálculo (n=5)
- A₂ = 0,577
- D₃ = 0  
- D₄ = 2,114

### Tarefa

Com os dados e as informações disponíveis, construa o gráfico de controle por variável para cada uma das operações e, assim, faça uma análise desses dados e dessas informações, identificando e relatando a situação do processo de usinagem avaliado e as respectivas estabilidades desse processo.

## Solução

### Cálculo das Médias e Amplitudes por Amostra

| Amostra | X̄     | R  |
|---------|-------|----| 
| 1       | 140,0 | 8  |
| 2       | 142,0 | 7  |
| 3       | 139,2 | 13 |
| 4       | 139,6 | 12 |
| 5       | 141,4 | 9  |
| 6       | 137,4 | 5  |
| 7       | 140,6 | 8  |
| 8       | 141,6 | 9  |
| 9       | 141,4 | 10 |
| 10      | 137,6 | 13 |
| 11      | 141,8 | 8  |
| 12      | 140,4 | 8  |
| 13      | 138,8 | 6  |
| 14      | 143,2 | 5  |
| 15      | 141,4 | 7  |
| 16      | 142,0 | 6  |
| 17      | 138,6 | 13 |
| 18      | 140,4 | 8  |
| 19      | 142,0 | 7  |
| 20      | 142,6 | 5  |

### Cálculos Finais

- **X̿** (média das médias) = 140,8 mm
- **R̄** (amplitude média) = 8,35 mm

### Limites de Controle

**Carta da Média:**
- **LSC** = 140,8 + 0,577 × 8,35 = **145,6 mm**
- **LIC** = 140,8 - 0,577 × 8,35 = **136,0 mm**  
- **LC** = **140,8 mm**

**Carta da Amplitude:**
- **LSC** = 2,114 × 8,35 = **17,7 mm**
- **LIC** = 0 × 8,35 = **0 mm**
- **LC** = **8,35 mm**

### Análise e Conclusões

**Estabilidade:** O processo está estatisticamente sob controle, com todos os pontos dentro dos limites.

**Capacidade:** O processo está centrado próximo ao nominal, mas algumas amostras podem ultrapassar a especificação superior (144 mm). Recomenda-se reduzir a variabilidade.

---

# Exercício 2 - Análise Avançada de Processo

## 📋 ENUNCIADO DO EXERCÍCIO

### Objetivos da Atividade

Este exercício tem como objetivo aplicar os conceitos de Controle Estatístico de Processo (CEP) através da construção e análise de cartas de controle com análise mais aprofundada.

### Habilidades Contempladas

- Compreensão teórica das expressões matemáticas para definição dos limites de controle
- Aplicação prática para cartas de média (X̄) e cartas de amplitude (R)
- Análise da estabilidade e capacidade de processos

### Situação Problema

Como membro de uma equipe de melhoria de processos, você deve analisar um processo de usinagem e determinar os limites de controle para cartas de controle por variável.

**Especificações da Peça:**
- Eixo usinado em centro de usinagem
- Material: Aço AISI 410
- Comprimento especificado: **140 mm ± 4 mm**
- Limites de especificação: LIE = 136 mm | LSE = 144 mm

### Dados Coletados

*[Mesmos dados do Exercício 1]*

### ❓ TAREFA

**Construa os gráficos de controle por variável (média e amplitude) e faça uma análise completa:**

1. Calcule os limites de controle para ambas as cartas
2. Verifique a estabilidade estatística do processo
3. Analise a capacidade do processo
4. Apresente conclusões e recomendações

## 📊 RESOLUÇÃO COMPLETA

### Análise da Estabilidade Estatística

#### ✅ Verificação dos Pontos de Controle

**Carta da Média:**
- Todas as médias estão entre 136,0 e 145,6 mm
- Nenhum ponto fora dos limites de controle
- **Processo sob controle estatístico** ✓

**Carta da Amplitude:**
- Todas as amplitudes estão entre 0 e 17,7 mm
- Nenhum ponto fora dos limites de controle
- **Variabilidade sob controle** ✓

### Análise da Capacidade do Processo

#### 🎯 Comparação com Especificações

| Parâmetro | Especificação | Processo | Status |
|-----------|---------------|----------|--------|
| LIE       | 136,0 mm     | 136,0 mm | ⚠️ Tangente |
| LSE       | 144,0 mm     | 145,6 mm | ❌ Excede |
| Centro    | 140,0 mm     | 140,8 mm | ⚠️ Deslocado |

### Conclusões e Recomendações

#### ✅ Aspectos Positivos
1. **Estabilidade confirmada:** Processo sob controle estatístico
2. **Centro próximo ao nominal:** Deslocamento de apenas 0,8 mm

#### ⚠️ Problemas Identificados
1. **Capacidade inadequada:** LSC (145,6) > LSE (144,0)
2. **Variabilidade excessiva:** R̄ = 8,35 mm é elevado
3. **Risco de não conformidade:** Potencial para peças rejeitadas

#### 🔧 Ações Recomendadas
1. **Centralizar processo** em 140,0 mm
2. **Reduzir variabilidade** através de melhorias no setup e manutenção
3. **Implementar monitoramento contínuo**

---

# Exercício 3 - Índices de Capacidade de Processo

## Objetivos da Atividade

Olá, estudante!

Este é o momento em que você colocará a mão na massa. Na proposta a seguir, você será convidado(a) a realizar uma atividade prática, aplicando os conteúdos estudados até aqui.

### Habilidades Contempladas

- Identificar os limites naturais, de especificação e de controle;
- Estruturar os índices de capacidade do processo tradicionais.

## Contexto do Exercício

Como parte integrante de uma equipe de melhoria de processos, você participa como suporte técnico de um grupo de estudo que está avaliando um processo por meio da utilização da capacidade de processo. Com os respectivos dados em mãos, a equipe deve realizar uma análise, a fim de determinar os chamados índices de capacidade de processo Cp e Cpk e realizar uma avaliação dos índices de capacidade da operação.

### Dados Fornecidos

- LIE = 9
- LSE = 11
- X̄ = 10,49
- R̄ = 0,405
- d₂ = 1,693

### Equações Matemáticas

```
Cp = (LSE - LIE) / (6 × R̄/d₂) = (LSE - LIE) / (6 × s/C₄)

Cpi = (X̄ - LIE) / (3 × R̄/d₂) = (X̄ - LIE) / (3 × s/C₄)

Cps = (LSE - X̄) / (3 × R̄/d₂) = (LSE - X̄) / (3 × s/C₄)
```

### Exercício - Pergunta

**Tendo como base a operação, sua cota nominal e suas tolerâncias, defina e estabeleça a capacidade respectiva do processo e os respectivos valores de Cp, Cpk, Pp e Ppk. Com o resultado dos índices de Cp e Cpk, estabeleça o nível de capacidade do processo e, caso este esteja fora dos parâmetros, defina quais as melhores ações a serem implantadas.**

## Solução

Caro(a) estudante, com a aplicação das equações matemáticas disponibilizadas, podemos obter, inicialmente, o respectivo valor do índice de capacidade Cp. Posteriormente, conseguimos obter o valor, respectivamente, para o índice de capacidade Cpi e Cps e, assim, encontrar aquele com menor valor, que representa o valor de Cpk.

### Cálculos dos Índices

**Cp = 1,39**  
**Cpk = 0,08** (menor valor entre Cpi e Cps)

### Análise dos Resultados

Em relação ao nível de capacidade observado, o valor de Cp igual ou maior a 1,33 representa uma operação já existente e que possui um índice de capacidade demonstrado. Assim, a operação em questão sinaliza um Cp = 1,39, portanto, é um processo capaz, não sendo necessária a tomada de qualquer tipo de ação.

### Conclusão

A diferença de valores entre Cp e Cpk é totalmente possível, e pode ocorrer normalmente. Na condição do exercício em que Cp é igual a 1,39, o processo é considerado como um processo estável, porém, devido ao valor bem menor de Cpk (0,08), esse processo está totalmente deslocado, possibilitando que sejam produzidas muitas peças fora das especificações.

**Ação Recomendada:** É necessário centralizar o processo, ajustando a média para reduzir o deslocamento e melhorar o índice Cpk.

---

# Exercício 4 - CEP por Batelada

## Objetivos da Atividade

Olá, estudante!

Esse é o momento em que você colocará a mão na massa. Na proposta abaixo, você será convidado(a) a realizar uma atividade prática aplicando os conteúdos estudados até aqui.

### Habilidades Contempladas

- Identificar as diferenças entre CEP para processos contínuos e CEP para processos por batelada;
- Estruturar as expressões matemáticas para CEP por batelada.

## Contexto Teórico

De forma mais específica, podemos considerar que os chamados processos por batelada são utilizados, efetivamente, quando há a procura da fabricação de produtos da linha alimentícia, bem como bioquímicos, produtos farmacêuticos e químicos, dentre outros.

O processo por batelada é caracterizado por possuir uma duração específica, considerada finita no tempo.

## Exercício

### Situação-Problema

Como parte integrante de uma equipe de melhoria de processos, você participa como suporte técnico de um grupo de estudo que está avaliando com o objetivo de implantar, em um processo, o CEP por batelada. Para isso, é preciso compreender as expressões matemáticas necessárias para a definição dos limites de controle, tanto para a carta da média quanto a carta para a amplitude.

### Dados Fornecidos

- X̄ = 537,5 mm
- R̄ = 5 mm
- d₂ = 1,128
- D₃ = 0
- D₄ = 3,267

### Questão

Tendo como base a operação em questão, sua cota nominal e suas tolerâncias, defina e estabeleça os limites de controle para o CEP por batelada.

## Resposta

Caro(a) estudante, com a aplicação das equações matemáticas disponibilizadas, podemos obter, respectivamente, os limites de controle para o gráfico da média, assim como os limites de controle para o gráfico da amplitude de um processo por batelada:

### Gráfico X̄

**Limites de Controle para a Média:**
- LSC_X̄ = X̄ + (R̄/d₂) = 537,5 + (5/1,128) = 537,5 + 4,43 = **541,93 mm**
- LC_X̄ = X̄ = **537,5 mm**
- LIC_X̄ = X̄ - (R̄/d₂) = 537,5 - (5/1,128) = 537,5 - 4,43 = **533,07 mm**

### Gráfico R

**Limites de Controle para a Amplitude:**
- LSC_R = D₄ × R̄ = 3,267 × 5 = **16,34 mm**
- LC_R = R̄ = **5 mm**
- LIC_R = D₃ × R̄ = 0 × 5 = **0 mm**

### Conclusão

Os limites de controle estabelecidos permitirão o monitoramento efetivo do processo por batelada, garantindo que tanto a média quanto a amplitude permaneçam dentro dos parâmetros de controle estatístico.

---

## Resumo Geral

Este conjunto de exercícios aborda os principais conceitos do Controle Estatístico de Processo:

1. **Exercício 1-2:** Fundamentos de cartas de controle e análise de estabilidade
2. **Exercício 3:** Índices de capacidade de processo (Cp e Cpk)
3. **Exercício 4:** CEP aplicado a processos por batelada

Cada exercício desenvolve habilidades específicas essenciais para a implementação efetiva do CEP em ambientes industriais.
