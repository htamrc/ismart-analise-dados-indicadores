import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar as três abas do arquivo Excel
filename = 'Base_Indicadores.xlsx'
print('Carregando arquivo:', filename)

# Aba 1: Base_Alunos_ADI_2026
df_alunos = pd.read_excel(filename, sheet_name='Base_Alunos_ADI_2026', engine='openpyxl')
print(f'Base_Alunos_ADI_2026: {len(df_alunos)} registros')

# Aba 2: Base_PS_2026
df_ps = pd.read_excel(filename, sheet_name='Base_PS_2026', engine='openpyxl')
print(f'Base_PS_2026: {len(df_ps)} registros')

# Aba 3: Base_Alunos_Veteranos
df_veteranos = pd.read_excel(filename, sheet_name='Base_Alunos_Veteranos', engine='openpyxl')
print(f'Base_Alunos_Veteranos: {len(df_veteranos)} registros')

# Padronizar colunas de identificação
df_alunos = df_alunos.rename(columns={'ID': 'id_aluno'})
df_ps = df_ps.rename(columns={'ID': 'id_aluno'})
df_veteranos = df_veteranos.rename(columns={'ID': 'id_aluno'})

df_alunos['id_aluno'] = df_alunos['id_aluno'].astype(str)
df_ps['id_aluno'] = df_ps['id_aluno'].astype(str)
df_veteranos['id_aluno'] = df_veteranos['id_aluno'].astype(str)

# 1) Criar coluna de região a partir do estado
def mapear_regiao(estado):
    if pd.isna(estado):
        return 'Não informado'
    estado = str(estado).strip().upper()
    if '(' in estado:
        estado = estado.split('(')[0].strip()
    
    regioes = {
        'SUDESTE': ['SAO PAULO', 'RIO DE JANEIRO', 'MINAS GERAIS', 'ESPIRITO SANTO'],
        'SUL': ['RIO GRANDE DO SUL', 'SANTA CATARINA', 'PARANA'],
        'NORDESTE': ['BAHIA', 'PERNAMBUCO', 'CEARA', 'MARANHAO', 'RIO GRANDE DO NORTE', 
                     'PARAIBA', 'PIAUI', 'ALAGOAS', 'SERGIPE'],
        'NORTE': ['AMAZONAS', 'PARA', 'RONDONIA', 'ACRE', 'RORAIMA', 'AMAPA', 'TOCANTINS'],
        'CENTRO-OESTE': ['GOIAS', 'MATO GROSSO', 'MATO GROSSO DO SUL', 'DISTRITO FEDERAL']
    }
    for regiao, estados in regioes.items():
        if any(uf in estado for uf in estados):
            return regiao
    return 'Outros'

# 2) Criar dataframe base com informações de conclusão da prova
df_base = df_alunos[['id_aluno', 'prova_unica_26.1']].copy()
df_base = df_base.rename(columns={'prova_unica_26.1': 'concluiu_prova'})
df_base['concluiu_prova'] = df_base['concluiu_prova'] == 1

# 3) Função para criar gráfico de barras MOSTRANDO QUANTIDADES REAIS (densidade)
def criar_grafico_barras_absoluto(dados, titulo, xlabel, filename, figsize=(12, 6)):
    """
    Cria gráfico de barras mostrando quantidades REAIS de alunos (não percentuais)
    dados: DataFrame com índice = categorias, colunas ['concluiu', 'nao_concluiu'] com quantidades ABSOLUTAS
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    x = range(len(dados))
    width = 0.8
    
    # Usar quantidades absolutas
    bars1 = ax.bar(x, dados['concluiu'], width, label='Concluiu a prova', color='#4caf50', alpha=0.8)
    bars2 = ax.bar(x, dados['nao_concluiu'], width, bottom=dados['concluiu'], 
                    label='Não concluiu a prova', color='#f44336', alpha=0.8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(dados.index, rotation=45, ha='right', fontsize=10)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel('Quantidade de Alunos', fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    
    # Adicionar valores totais nas barras
    for i, (idx, row) in enumerate(dados.iterrows()):
        total = row['concluiu'] + row['nao_concluiu']
        # Valor no topo da barra (total)
        ax.text(i, total + (max(dados.sum(axis=1)) * 0.02), 
                f'Total: {int(total)}', ha='center', fontweight='bold', fontsize=9, color='gray')
        
        # Valor dentro da barra de concluiu (se houver espaço)
        if row['concluiu'] > max(total * 0.1, 5):
            ax.text(i, row['concluiu']/2, f'{int(row["concluiu"])}', ha='center', va='center', 
                    color='white', fontweight='bold', fontsize=9)
        
        # Valor dentro da barra de não concluiu (se houver espaço)
        if row['nao_concluiu'] > max(total * 0.1, 5):
            ax.text(i, row['concluiu'] + row['nao_concluiu']/2, f'{int(row["nao_concluiu"])}', 
                    ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f'Gráfico salvo: {filename}')
    plt.close()
    return dados

# 4) Processar cada parâmetro com quantidades absolutas

print("\n" + "="*60)
print("GERANDO GRÁFICOS COM QUANTIDADES ABSOLUTAS DE ALUNOS")
print("="*60)

# Função auxiliar para processar cada análise com quantidades absolutas
def processar_analise_absoluta(df_base, df_dados, coluna_categoria, titulo, xlabel, filename):
    """
    Processa uma análise mostrando quantidades absolutas de alunos
    """
    df_analise = df_base.merge(df_dados, on='id_aluno', how='left')
    
    resultados = {}
    for categoria in df_analise[coluna_categoria].dropna().unique():
        dados_cat = df_analise[df_analise[coluna_categoria] == categoria]
        total = len(dados_cat)
        concluiu = dados_cat['concluiu_prova'].sum()
        nao_concluiu = total - concluiu
        if total > 0:
            resultados[categoria] = {
                'concluiu': concluiu,  # QUANTIDADE ABSOLUTA
                'nao_concluiu': nao_concluiu,  # QUANTIDADE ABSOLUTA
                'total': total,
                'taxa_conclusao': 100 * concluiu / total  # manter para referência
            }
    
    df_resultado = pd.DataFrame(resultados).T
    df_resultado = df_resultado.sort_index()
    
    print(f'\n--- {titulo} ---')
    print(df_resultado[['concluiu', 'nao_concluiu', 'total']])
    
    # Gerar gráfico com quantidades absolutas
    criar_grafico_barras_absoluto(df_resultado[['concluiu', 'nao_concluiu']], 
                                   titulo, xlabel, filename)
    
    return df_resultado

# ==================== 1. Série ====================
df_base_serie = df_alunos[['id_aluno', 'serie']].copy()
processar_analise_absoluta(df_base, df_base_serie, 'serie', 
                            'Conclusão da Prova Única por Série (Quantidade de Alunos)', 
                            'Série', 'grafico_1_serie_absoluto.png')

# ==================== 2. Ano de Ingresso ====================
df_base_ano = df_alunos[['id_aluno', 'ano_ingresso']].copy()
processar_analise_absoluta(df_base, df_base_ano, 'ano_ingresso', 
                            'Conclusão da Prova Única por Ano de Ingresso (Quantidade de Alunos)', 
                            'Ano de Ingresso', 'grafico_2_ano_ingresso_absoluto.png')

# ==================== 3. Região ====================
# Combinar dados de região das diferentes bases
df_regiao = pd.DataFrame()

if 'estado' in df_alunos.columns:
    df_regiao_alunos = df_alunos[['id_aluno', 'estado']].copy()
    df_regiao_alunos['regiao'] = df_regiao_alunos['estado'].apply(mapear_regiao)
    df_regiao = pd.concat([df_regiao, df_regiao_alunos[['id_aluno', 'regiao']]])

if 'estado' in df_ps.columns:
    df_regiao_ps = df_ps[['id_aluno', 'estado']].copy()
    df_regiao_ps['regiao'] = df_regiao_ps['estado'].apply(mapear_regiao)
    df_regiao = pd.concat([df_regiao, df_regiao_ps[['id_aluno', 'regiao']]])

if 'estado' in df_veteranos.columns:
    df_regiao_vet = df_veteranos[['id_aluno', 'estado']].copy()
    df_regiao_vet['regiao'] = df_regiao_vet['estado'].apply(mapear_regiao)
    df_regiao = pd.concat([df_regiao, df_regiao_vet[['id_aluno', 'regiao']]])

df_regiao = df_regiao.drop_duplicates(subset=['id_aluno'], keep='first')

processar_analise_absoluta(df_base, df_regiao, 'regiao', 
                            'Conclusão da Prova Única por Região (Quantidade de Alunos)', 
                            'Região', 'grafico_3_regiao_absoluto.png')

# ==================== 4. Média de Engajamento ====================
df_base_eng = df_alunos[['id_aluno', 'media_engajamento']].copy()
df_analise = df_base.merge(df_base_eng, on='id_aluno', how='left')
df_analise['media_engajamento'] = df_analise['media_engajamento'].fillna(0)

bins = [-0.1, 0, 0.25, 0.5, 0.75, 1.01]
labels = ['0%', '1-25%', '26-50%', '51-75%', '76-100%']
df_analise['faixa_engajamento'] = pd.cut(df_analise['media_engajamento'], bins=bins, labels=labels)

processar_analise_absoluta(df_base, df_analise[['id_aluno', 'faixa_engajamento']], 'faixa_engajamento', 
                            'Conclusão da Prova Única por Média de Engajamento (Quantidade de Alunos)', 
                            'Média de Engajamento', 'grafico_4_engajamento_absoluto.png')

# ==================== 5. Cadastro Atualizado ====================
df_base_cad = df_alunos[['id_aluno', 'cadastro_atualizado']].copy()
df_analise = df_base.merge(df_base_cad, on='id_aluno', how='left')
df_analise['cadastro_atualizado'] = df_analise['cadastro_atualizado'].fillna(0)
df_analise['status_cadastro'] = df_analise['cadastro_atualizado'].map({0: 'Não atualizado', 1: 'Atualizado'})

processar_analise_absoluta(df_base, df_analise[['id_aluno', 'status_cadastro']], 'status_cadastro', 
                            'Conclusão da Prova Única por Atualização de Cadastro (Quantidade de Alunos)', 
                            'Status do Cadastro', 'grafico_5_cadastro_absoluto.png')

# ==================== 6. Presença em Encontro de Clubes ====================
df_base_pres = df_alunos[['id_aluno', 'presença_encontroclubes', 'justificativa_ausência']].copy()

def participacao(row):
    if row['presença_encontroclubes'] == 1:
        return 1
    if row['justificativa_ausência'] == 1:
        return 1
    return 0

df_base_pres['participou'] = df_base_pres.apply(participacao, axis=1)
df_base_pres['status_presenca'] = df_base_pres['participou'].map({0: 'Não participou', 1: 'Participou'})

processar_analise_absoluta(df_base, df_base_pres[['id_aluno', 'status_presenca']], 'status_presenca', 
                            'Conclusão da Prova Única por Participação em Encontro de Clubes (Quantidade de Alunos)', 
                            'Participação', 'grafico_6_presenca_absoluto.png')

# ==================== 7. Acessou Discord ====================
df_base_discord = df_alunos[['id_aluno', 'acessou_discord']].copy()
df_base_discord['acessou_discord'] = df_base_discord['acessou_discord'].fillna('Não')
df_base_discord['acessou_discord'] = df_base_discord['acessou_discord'].apply(
    lambda x: 'Sim' if str(x).strip().upper() in ['SIM', '1'] else 'Não'
)

processar_analise_absoluta(df_base, df_base_discord, 'acessou_discord', 
                            'Conclusão da Prova Única por Acesso ao Discord (Quantidade de Alunos)', 
                            'Acesso ao Discord', 'grafico_7_discord_absoluto.png')

# ==================== 8. Gênero ====================
df_genero = pd.DataFrame()

if 'genero' in df_ps.columns:
    df_genero_ps = df_ps[['id_aluno', 'genero']].copy()
    df_genero = pd.concat([df_genero, df_genero_ps])

if 'genero' in df_veteranos.columns:
    df_genero_vet = df_veteranos[['id_aluno', 'genero']].copy()
    df_genero = pd.concat([df_genero, df_genero_vet])

df_genero = df_genero.drop_duplicates(subset=['id_aluno'], keep='first')
df_genero['genero'] = df_genero['genero'].fillna('Não informado')

processar_analise_absoluta(df_base, df_genero, 'genero', 
                            'Conclusão da Prova Única por Gênero (Quantidade de Alunos)', 
                            'Gênero', 'grafico_8_genero_absoluto.png')

# ==================== 9. Etnia ====================
df_etnia = pd.DataFrame()

if 'etnia' in df_ps.columns:
    df_etnia_ps = df_ps[['id_aluno', 'etnia']].copy()
    df_etnia = pd.concat([df_etnia, df_etnia_ps])

if 'etnia' in df_veteranos.columns:
    df_etnia_vet = df_veteranos[['id_aluno', 'etnia']].copy()
    df_etnia = pd.concat([df_etnia, df_etnia_vet])

df_etnia = df_etnia.drop_duplicates(subset=['id_aluno'], keep='first')
df_etnia['etnia'] = df_etnia['etnia'].fillna('Não informado')

processar_analise_absoluta(df_base, df_etnia, 'etnia', 
                            'Conclusão da Prova Única por Etnia (Quantidade de Alunos)', 
                            'Etnia', 'grafico_9_etnia_absoluto.png')

# ==================== 10. Acesso à Plataforma ====================
df_base_plataforma = df_ps[['id_aluno', 'acesso_plataforma']].copy()
df_base_plataforma['acesso_plataforma'] = df_base_plataforma['acesso_plataforma'].fillna('Não')
df_base_plataforma['acesso_plataforma'] = df_base_plataforma['acesso_plataforma'].apply(
    lambda x: 'Sim' if str(x).strip().upper() in ['SIM', 'S', '1'] else 'Não'
)

processar_analise_absoluta(df_base, df_base_plataforma, 'acesso_plataforma', 
                            'Conclusão da Prova Única por Acesso à Plataforma (Quantidade de Alunos)', 
                            'Acesso à Plataforma', 'grafico_10_plataforma_absoluto.png')

# ==================== 11. Progresso nas Aulas ====================
df_base_progresso = df_ps[['id_aluno', 'progresso_aulas']].copy()
df_analise = df_base.merge(df_base_progresso, on='id_aluno', how='left')
df_analise['progresso_aulas'] = df_analise['progresso_aulas'].fillna(0)

bins_progresso = [-0.1, 0, 0.25, 0.5, 0.75, 1.01]
labels_progresso = ['0%', '1-25%', '26-50%', '51-75%', '76-100%']
df_analise['faixa_progresso'] = pd.cut(df_analise['progresso_aulas'], bins=bins_progresso, labels=labels_progresso)

processar_analise_absoluta(df_base, df_analise[['id_aluno', 'faixa_progresso']], 'faixa_progresso', 
                            'Conclusão da Prova Única por Progresso nas Aulas (Quantidade de Alunos)', 
                            'Progresso nas Aulas', 'grafico_11_progresso_absoluto.png')

# ==================== 12. Fez PD e Dentro do Critério PD ====================
df_base_pd = df_ps[['id_aluno', 'fez_PD', 'dentro_criterio_PD']].copy()
df_analise = df_base.merge(df_base_pd, on='id_aluno', how='left')

def categoria_pd(row):
    if pd.isna(row['fez_PD']) or row['fez_PD'] == 'Não':
        return 'Não fez PD'
    if row['dentro_criterio_PD'] == 'Sim':
        return 'Fez PD e dentro do critério'
    return 'Fez PD, fora do critério'

df_analise['categoria_pd'] = df_analise.apply(categoria_pd, axis=1)

processar_analise_absoluta(df_base, df_analise[['id_aluno', 'categoria_pd']], 'categoria_pd', 
                            'Conclusão da Prova Única por Participação no PD (Quantidade de Alunos)', 
                            'Status PD', 'grafico_12_pd_absoluto.png')

# ==================== 13. Cluster Nota MAT ====================
df_base_cluster = df_ps[['id_aluno', 'cluster_nota_MAT']].copy()
df_analise = df_base.merge(df_base_cluster, on='id_aluno', how='left')
df_analise['cluster_nota_MAT'] = df_analise['cluster_nota_MAT'].fillna('Sem nota')

processar_analise_absoluta(df_base, df_analise[['id_aluno', 'cluster_nota_MAT']], 'cluster_nota_MAT', 
                            'Conclusão da Prova Única por Cluster de Nota em Matemática (Quantidade de Alunos)', 
                            'Cluster Nota MAT', 'grafico_13_cluster_absoluto.png')

# =====================================================
# ANÁLISES DE INTERRELAÇÕES ENTRE VARIÁVEIS
# =====================================================

print('\n' + '='*60)
print('ANÁLISES DE INTERRELAÇÕES ENTRE VARIÁVEIS')
print('='*60)

# Preparar dataframe base para análises cruzadas
df_analise_cruzada = df_alunos[['id_aluno', 'serie', 'ano_ingresso', 'media_engajamento', 
                                 'prova_unica_26.1', 'cadastro_atualizado', 'acessou_discord']].copy()
df_analise_cruzada['concluiu_prova'] = df_analise_cruzada['prova_unica_26.1'] == 1

# Adicionar dados de presença em clubes (considerando justificativa)
def participacao_clubes(row):
    if row['presença_encontroclubes'] == 1:
        return 1
    if row['justificativa_ausência'] == 1:
        return 1
    return 0

df_analise_cruzada = df_analise_cruzada.merge(
    df_alunos[['id_aluno', 'presença_encontroclubes', 'justificativa_ausência']], 
    on='id_aluno', how='left'
)
df_analise_cruzada['participou_clubes'] = df_analise_cruzada.apply(participacao_clubes, axis=1)
df_analise_cruzada['participou_clubes'] = df_analise_cruzada['participou_clubes'].fillna(0)

# Adicionar dados de acesso à plataforma e progresso nas aulas (da base PS)
df_ps_cruzada = df_ps[['id_aluno', 'acesso_plataforma', 'progresso_aulas']].copy()
df_ps_cruzada['acesso_plataforma'] = df_ps_cruzada['acesso_plataforma'].apply(
    lambda x: 1 if str(x).strip().upper() in ['SIM', 'S', '1'] else 0
)
df_analise_cruzada = df_analise_cruzada.merge(df_ps_cruzada, on='id_aluno', how='left')

# Adicionar dados de região
df_regiao_cruzada = df_regiao.copy()
df_analise_cruzada = df_analise_cruzada.merge(df_regiao_cruzada, on='id_aluno', how='left')
df_analise_cruzada['regiao'] = df_analise_cruzada['regiao'].fillna('Não informado')

# =====================================================
# 1. Engajamento × Presença em clubes (Gráfico com quantidades absolutas)
# =====================================================
print('\n--- 1. Engajamento × Presença em clubes ---')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Gráfico 1: Boxplot (mostra distribuição)
participou_eng = df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 1]['media_engajamento'].dropna()
nao_participou_eng = df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 0]['media_engajamento'].dropna()

axes[0].boxplot([participou_eng, nao_participou_eng], 
                labels=['Participou', 'Não participou'],
                patch_artist=True,
                boxprops=dict(facecolor='#4caf50', alpha=0.7),
                medianprops=dict(color='black', linewidth=2))
axes[0].set_title('Distribuição do Engajamento por Participação em Clubes', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Média de Engajamento')
axes[0].set_ylim(0, 1.1)
axes[0].text(1, 0.05, f'n={len(participou_eng)}', ha='center', fontsize=10, fontweight='bold')
axes[0].text(2, 0.05, f'n={len(nao_participou_eng)}', ha='center', fontsize=10, fontweight='bold')

# Gráfico 2: Barras com quantidades absolutas
participou_concluiu = df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 1]['concluiu_prova'].sum()
participou_total = len(df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 1])
nao_participou_concluiu = df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 0]['concluiu_prova'].sum()
nao_participou_total = len(df_analise_cruzada[df_analise_cruzada['participou_clubes'] == 0])

# Barras empilhadas com quantidades absolutas
bars_concluiu = axes[1].bar(['Participou'], [participou_concluiu], label='Concluiu', color='#4caf50', alpha=0.8)
bars_nao_concluiu = axes[1].bar(['Participou'], [participou_total - participou_concluiu], 
                                 bottom=[participou_concluiu], label='Não concluiu', color='#f44336', alpha=0.8)

bars_concluiu2 = axes[1].bar(['Não participou'], [nao_participou_concluiu], color='#4caf50', alpha=0.8)
bars_nao_concluiu2 = axes[1].bar(['Não participou'], [nao_participou_total - nao_participou_concluiu], 
                                  bottom=[nao_participou_concluiu], color='#f44336', alpha=0.8)

axes[1].set_title('Conclusão da Prova por Participação em Clubes\n(Quantidade Absoluta de Alunos)', 
                  fontsize=12, fontweight='bold')
axes[1].set_ylabel('Quantidade de Alunos')
axes[1].legend(loc='upper right')

# Adicionar valores nas barras
axes[1].text(0, participou_concluiu/2, str(participou_concluiu), ha='center', va='center', 
             color='white', fontweight='bold', fontsize=10)
axes[1].text(0, participou_concluiu + (participou_total - participou_concluiu)/2, 
             str(participou_total - participou_concluiu), ha='center', va='center', 
             color='white', fontweight='bold', fontsize=10)
axes[1].text(1, nao_participou_concluiu/2, str(nao_participou_concluiu), ha='center', va='center', 
             color='white', fontweight='bold', fontsize=10)
axes[1].text(1, nao_participou_concluiu + (nao_participou_total - nao_participou_concluiu)/2, 
             str(nao_participou_total - nao_participou_concluiu), ha='center', va='center', 
             color='white', fontweight='bold', fontsize=10)

# Adicionar totais no topo
axes[1].text(0, participou_total + 5, f'Total: {participou_total}', ha='center', fontweight='bold', fontsize=9, color='gray')
axes[1].text(1, nao_participou_total + 5, f'Total: {nao_participou_total}', ha='center', fontweight='bold', fontsize=9, color='gray')

plt.tight_layout()
plt.savefig('analise_engajamento_clubes_absoluto.png', dpi=150)
print('Gráfico salvo: analise_engajamento_clubes_absoluto.png')
plt.close()

# =====================================================
# 2. Matriz de correlação
# =====================================================
print('\n--- 2. Matriz de Correlação ---')

variaveis_numericas = ['media_engajamento', 'progresso_aulas', 'cadastro_atualizado', 
                       'participou_clubes', 'acesso_plataforma']
df_corr = df_analise_cruzada[variaveis_numericas].dropna()
corr_matrix = df_corr.corr()

fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr_matrix.values, cmap='RdBu_r', vmin=-1, vmax=1, aspect='auto')
ax.set_xticks(range(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right', fontsize=10)
ax.set_yticks(range(len(corr_matrix.columns)))
ax.set_yticklabels(corr_matrix.columns, fontsize=10)
ax.set_title('Matriz de Correlação entre Variáveis', fontsize=14, fontweight='bold')
plt.colorbar(im, ax=ax, label='Correlação')

for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        corr_val = corr_matrix.values[i, j]
        text_color = 'white' if abs(corr_val) > 0.5 else 'black'
        ax.text(j, i, f'{corr_val:.2f}', ha='center', va='center', 
                color=text_color, fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('analise_matriz_correlacao_absoluto.png', dpi=150)
print('Gráfico salvo: analise_matriz_correlacao_absoluto.png')
plt.close()

print('\nPrincipais correlações encontradas:')
for i, var1 in enumerate(corr_matrix.columns):
    for j, var2 in enumerate(corr_matrix.columns):
        if i < j and abs(corr_matrix.values[i, j]) > 0.1:
            print(f'  {var1} × {var2}: {corr_matrix.values[i, j]:.3f}')

print('\n' + '='*60)
print('TODOS OS GRÁFICOS FORAM GERADOS COM QUANTIDADES ABSOLUTAS!')
print('='*60)
print('\nArquivos gerados (mostrando quantidade real de alunos):')
print('GRÁFICOS PRINCIPAIS:')
print('1. grafico_1_serie_absoluto.png - Série')
print('2. grafico_2_ano_ingresso_absoluto.png - Ano de Ingresso')
print('3. grafico_3_regiao_absoluto.png - Região')
print('4. grafico_4_engajamento_absoluto.png - Média de Engajamento')
print('5. grafico_5_cadastro_absoluto.png - Cadastro Atualizado')
print('6. grafico_6_presenca_absoluto.png - Presença em Encontro de Clubes')
print('7. grafico_7_discord_absoluto.png - Acesso ao Discord')
print('8. grafico_8_genero_absoluto.png - Gênero')
print('9. grafico_9_etnia_absoluto.png - Etnia')
print('10. grafico_10_plataforma_absoluto.png - Acesso à Plataforma')
print('11. grafico_11_progresso_absoluto.png - Progresso nas Aulas')
print('12. grafico_12_pd_absoluto.png - Fez PD e Critério PD')
print('13. grafico_13_cluster_absoluto.png - Cluster Nota MAT')
print('\nANÁLISES DE INTERRELAÇÕES:')
print('14. analise_engajamento_clubes_absoluto.png - Engajamento × Presença em clubes')
print('15. analise_matriz_correlacao_absoluto.png - Matriz de correlação')