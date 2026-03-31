# Análise de Conclusão da Prova Única

## Sobre a Análise

Essa análise avalia a conclusão da Prova Única pelo alunos do Instituto, considerando a distinção entre Ensino Fundamental e Ensino Médio, além da distribuição por série.

## Arquivos do Projeto

- `analise_Dados_PU.py` - Script principal de análise (planilha fornecida)
- `Dados_PU.xlsx` - Base de dados com informações dos alunos
- `graficos/` - Pasta com os gráficos gerados
- `relatorios/` - Pasta com os relatórios CSV

## Gráficos Gerados

- `grafico_conclusao_prova_unica.png` - Percentual geral de conclusão
- `grafico_prova_unica_por_serie.png` - Percentual de conclusão por série
- `grafico_prova_unica_por_serie_densidade.png` - Quantidade real de alunos por série

## Relatórios Gerados

- `relatorio_prova_unica_analise_Dados_PU.csv` - Detalhamento por aluno
- `relatorio_por_serie_Dados_PU.csv` - Estatísticas agregadas por série

## Interpretação dos Gráficos

### Gráfico Geral
- Barras verdes representam alunos que concluíram a prova
- Barras vermelhas representam alunos que não concluíram
- Valores acima das barras indicam os percentuais

### Gráfico por Série (Percentual)
- Mostra a proporção de conclusão dentro de cada série
- Útil para comparar o desempenho relativo entre séries

### Gráfico por Série (Densidade)
- Mostra a quantidade real de alunos em cada série
- Considera a densidade de alunos concluintes e não concluintes




## Descobertas e Conclusões

### Visão Geral

A análise da Prova Única revelou que 68% do total de alunos concluíram a prova, totalizando 1.247 alunos concluintes em uma base de 1.834 alunos.

### Comparação entre Ensino Fundamental e Médio

Os alunos do Ensino Médio concluíram a prova em maior proporção em comparação com os alunos do Ensino Fundamental. Essa diferença pode estar relacionada à maior maturidade acadêmica e à familiaridade com o formato da avaliação.

- **Ensino Fundamental**: 62% de conclusão (742 alunos de 1.197)
- **Ensino Médio**: 74% de conclusão (505 alunos de 637)

### Desempenho por Série

**Ensino Fundamental (6º ao 9º ano)**

O 9º ano apresentou o maior número de alunos concluintes

As séries iniciais merecem atenção especial:
- 6º ano: 74 alunos não concluintes (46% da série)
- 7º ano: 113 alunos não concluintes (39% da série)

**Ensino Médio (1º ao 3º ano)**
- O 3º ano teve o melhor desempenho, com alta concentração de alunos concluintes
- O 1º ano apresentou queda em relação ao 9º ano, possivelmente devido à adaptação ao novo ciclo de ensino


### Densidade versus Percentual

Os gráficos de densidade (quantidade real de alunos) complementaram a análise percentual, revelando que:
- As séries finais de cada etapa (9º ano e 3º ano) concentram o maior volume de alunos
- Estratégias de reforço devem considerar tanto a proporção quanto o número absoluto de alunos em cada série

### Recomendações 

- Focar intervenções no 6º ano, que tem a menor taxa (54%) e 74 alunos não concluintes
- Manter estratégias bem-sucedidas no 3º ano, que alcançou 91% de conclusão
- Priorizar ações para as séries com maior densidade (9º e 3º anos) devido ao volume de alunos
- Utilizar tanto métricas percentuais quanto absolutas para planejamento de intervenções




## Dependências

pip install pandas matplotlib openpyxl

## Execução

python analise_Dados_PU.py




## Autora

Agatha Ferreira Marcilio  
htamarcilio@gmail.com

## Data

Março/2026