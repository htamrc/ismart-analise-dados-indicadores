# CASE ISMART - Análise de Indicadores Educacionais

## Sobre o Projeto

Este repositório contém duas análises desenvolvidas para o Case Ismart com o objetivo de avaliar diferentes aspectos do desempenho e engajamento dos alunos.

## Estrutura do Repositório

- `README.md` - Documentação principal

- **analise-conclusao-prova/**
  - `README.md`
  - `analise_Dados_PU.py`
  - `Dados_PU.xlsx`
  - `graficos/`
  - `relatorios/`

- **analise-indicadores/**
  - `README.md`
  - `analise_indicadores.py`
  - `Base_Indicadores.xlsx`
  - `graficos/`

## Análises Realizadas

### 1. Análise de Conclusão da Prova Única (analise-conclusao-prova)

Avalia a conclusão da Prova Única pelos alunos, com distribuição por série e por etapa de ensino (Fundamental e Médio). Gera gráficos e relatórios em CSV.

### 2. Análise de Indicadores (analise-indicadores)

Investiga 13 fatores associados à conclusão da Prova Única, considerando a densidade real de alunos em cada categoria. Inclui gráficos de barras com quantidades absolutas, análises de interrelações e matriz de correlação.




## Principais Descobertas e Conclusões Obtidas a Partir da Analise Realizada

### Análise de Conclusão da Prova Única

A análise revelou que os alunos do Ensino Médio apresentaram maior taxa de conclusão da Prova Única em comparação com os alunos do Ensino Fundamental. Dentro do Ensino Fundamental, os alunos do 9º ano tiveram o melhor desempenho, enquanto no Ensino Médio, o 3º ano se destacou. Quando considerada a densidade real de alunos, observou-se que as séries finais de cada etapa concentram o maior número de alunos, o que reforça a importância de estratégias específicas para esses grupos.

### Análise de Indicadores

A análise dos 13 indicadores mostrou que variáveis relacionadas ao engajamento e ao uso das plataformas da instituição estão fortemente associadas à conclusão da prova. Alunos com maior média de engajamento, que acessaram o Discord e a plataforma de estudos, e que participaram dos encontros de clubes apresentaram quantidades absolutas significativamente maiores de conclusão.

Em relação ao perfil demográfico, a região Sudeste concentra o maior número de alunos, seguida pelas regiões Sul e Nordeste. Quanto ao desempenho acadêmico, alunos classificados nos clusters de nota mais altos em Matemática (acima de 80) concluíram a prova em maior número.

A matriz de correlação confirmou relações positivas entre engajamento e progresso nas aulas (correlação de 0.67) e entre acesso à plataforma e conclusão da prova (correlação de 0.58).


> [!IMPORTANTE]
> Recomendo fortemente a leitura dos arquivos README.md de cada análise realizada, onde é possível acessar detalhes quantitativos e recomendações fornecidas com base nos dados.


## Tecnologias Utilizadas

- Python 3.9+
- pandas
- matplotlib
- numpy
- openpyxl

## Dependências

pip install pandas matplotlib numpy openpyxl




## Autora

Agatha Ferreira Marcilio  
htamarcilio@gmail.com

## Data

Março/2026
