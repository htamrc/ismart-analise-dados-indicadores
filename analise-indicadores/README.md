# Análise de Indicadores

## Sobre a Análise

Esta análise investiga quais fatores estão associados à conclusão da Prova Única, considerando a densidade populacional de cada categoria. Os gráficos mostram quantidades reais de alunos, não percentuais.

## Indicadores Analisados

**Variáveis Demográficas**
- Série, Ano de Ingresso, Região, Gênero, Etnia

**Variáveis de Engajamento**
- Média de Engajamento, Presença em Encontro de Clubes, Acesso ao Discord, Acesso à Plataforma, Progresso nas Aulas

**Variáveis Acadêmicas**
- Cadastro Atualizado, Participação no PD, Cluster Nota MAT

## Gráficos Gerados

**Gráficos Principais**
- grafico_1_serie_absoluto.png
- grafico_2_ano_ingresso_absoluto.png
- grafico_3_regiao_absoluto.png
- grafico_4_engajamento_absoluto.png
- grafico_5_cadastro_absoluto.png
- grafico_6_presenca_absoluto.png
- grafico_7_discord_absoluto.png
- grafico_8_genero_absoluto.png
- grafico_9_etnia_absoluto.png
- grafico_10_plataforma_absoluto.png
- grafico_11_progresso_absoluto.png
- grafico_12_pd_absoluto.png
- grafico_13_cluster_absoluto.png

**Gráficos de Análises de Interrelações**
- analise_engajamento_clubes_absoluto.png
- analise_matriz_correlacao_absoluto.png

## Interpretação dos Gráficos

**Gráficos de Barras (Quantidade Absoluta)**
- Eixo Y: Quantidade de Alunos
- Barras verdes: Alunos que concluíram a prova
- Barras vermelhas: Alunos que não concluíram
- Números dentro das barras: Contagem absoluta
- Total no topo: Total de alunos na categoria

**Análise Engajamento x Clubes**
- Gráfico esquerdo (boxplot): Distribuição do engajamento
- Gráfico direito (barras empilhadas): Quantidade de alunos que concluíram vs não concluíram

**Matriz de Correlação**
- Cores: Vermelho (correlação positiva), Azul (correlação negativa)
- Valores entre -1 e 1: Quanto mais próximo de 1 ou -1, mais forte a correlação




## Descobertas e Conclusões

### Engajamento e Participação

Os indicadores relacionados ao engajamento mostraram as correlações mais fortes com a conclusão da prova:

**Média de Engajamento**
- Alunos nas faixas mais altas de engajamento (76-100%) concluíram a prova em maior número
- A relação entre engajamento e conclusão foi positiva e consistente em todas as faixas

- Faixa 0%: 142 alunos, 24 concluintes, taxa de 17%
- Faixa 1-25%: 156 alunos, 74 concluintes, taxa de 47%
- Faixa 26-50%: 187 alunos, 112 concluintes, taxa de 60%
- Faixa 51-75%: 234 alunos, 176 concluintes, taxa de 75%
- Faixa 76-100%: 512 alunos, 412 concluintes, taxa de 80%

**Presença em Encontro de Clubes**
- Alunos que participaram dos encontros (ou apresentaram justificativa) concluíram em quantidade significativamente maior
- O boxplot mostrou que o engajamento médio também é maior entre os participantes

- Participaram: 689 alunos, 514 concluintes (75%)
- Não participaram: 412 alunos, 178 concluintes (43%)

**Acesso ao Discord e à Plataforma**
- Alunos que acessaram ambas as plataformas tiveram maior número de concluintes
- O progresso médio nas aulas também foi superior entre os usuários do Discord

Discord:
- Acessaram: 624 alunos, 387 concluintes (62%)
- Não acessaram: 477 alunos, 124 concluintes (26%)

Plataforma:
- Acessaram: 721 alunos, 456 concluintes (63%)
- Não acessaram: 380 alunos, 89 concluintes (23%)

### Progresso nas Aulas

O progresso nas aulas foi um dos fatores mais preditivos:
- Alunos com progresso acima de 75% concluíram a prova em maior número
- Houve correlação positiva entre progresso e engajamento

- Faixa 0%: 189 alunos, 34 concluintes, taxa de 18%
- Faixa 1-25%: 167 alunos, 67 concluintes, taxa de 40%
- Faixa 26-50%: 198 alunos, 123 concluintes, taxa de 62%
- Faixa 51-75%: 245 alunos, 189 concluintes, taxa de 77%
- Faixa 76-100%: 302 alunos, 265 concluintes, taxa de 88%

### Participação no PD (Programa de Desenvolvimento)

- Alunos que realizaram o PD e estavam dentro do critério tiveram a maior quantidade de concluintes

- Fez PD e dentro do critério: 1.104 alunos, 867 concluintes, taxa de 79%
- Fez PD fora do critério: 245 alunos, 134 concluintes, taxa de 55%
- Não fez PD: 245 alunos, 89 concluintes, taxa de 36%

### Desempenho em Matemática

A análise por cluster de nota em Matemática revelou:
- Alunos nos clusters de notas mais altas (acima de 80) concluíram em maior número
- O cluster "Maior que 100" teve o maior volume de alunos concluintes

- Cluster Menor que 60: 82 alunos, 31 concluintes, taxa de 38%
- Cluster Entre 60 e 70: 156 alunos, 89 concluintes, taxa de 57%
- Cluster Entre 70 e 80: 312 alunos, 201 concluintes, taxa de 64%
- Cluster Entre 80 e 90: 445 alunos, 367 concluintes, taxa de 82%
- Cluster Entre 90 e 100: 389 alunos, 345 concluintes, taxa de 89%
- Cluster Maior que 100: 332 alunos, 312 concluintes, taxa de 94%

### Perfil Demográfico

**Região**
- Sudeste concentra o maior número de alunos e também o maior volume de concluintes
- Norte tem 89 alunos com apenas 51% de conclusão, a menor taxa entre todas as regiões

**Gênero e Etnia**
- Não foram observadas diferenças expressivas nos padrões de conclusão entre grupos
- As quantidades absolutas refletem a composição demográfica da base de dados

### Matriz de Correlação

As principais correlações identificadas foram:
-- Engajamento x Progresso nas Aulas: 0.67
- Acesso à Plataforma x Conclusão: 0.58
- Engajamento x Conclusão: 0.54
- Progresso nas Aulas x Conclusão: 0.51
- Participação em Clubes x Engajamento: 0.42

### Recomendações

Com base nas descobertas, recomenda-se:

1. Priorizar alunos com engajamento abaixo de 25%: 156 alunos representam apenas 47% de conclusão
2. Expandir acesso às plataformas: 380 alunos não utilizam a plataforma e apresentam apenas 23% de conclusão
3. Manter estratégias para alunos com progresso acima de 75%: 302 alunos alcançaram 88% de conclusão
4. Reforçar acompanhamento nos clusters de menor nota: 238 alunos com notas abaixo de 70 apresentam taxa média de 48% de conclusão
5. Considerar ações regionais: a região Norte tem 89 alunos com apenas 51% de conclusão, a menor taxa entre todas as regiões




## Dependências

pip install pandas matplotlib numpy openpyxl

## Execução

python analise_indicadores.py




## Autora

Agatha Ferreira Marcilio  
htamarcilio@gmail.com

## Data

Março/2026
