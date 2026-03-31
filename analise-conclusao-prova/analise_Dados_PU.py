import re
import pandas as pd
import matplotlib.pyplot as plt

# 1) Abrir o arquivo específico
filename = 'Dados_PU.xlsx'
if not pd.io.common.file_exists(filename):
    raise FileNotFoundError('Arquivo Dados_PU.xlsx não encontrado no diretório atual.')

print('Usando arquivo:', filename)
df = pd.read_excel(filename, engine='openpyxl')
print('Registros (linhas):', len(df))
print('Colunas:', list(df.columns))

if 'AREA' not in df.columns:
    df['AREA'] = df['NOMEPROCESSO']

# 2) Extrair série e categoria (fundamental/médio) a partir do NOMEPROCESSO

def parse_serie_categoria(nome):
    if isinstance(nome, str):
        m = re.search(r'\b(EF|EM)_(\d+)\b', nome.upper())
        if m:
            tipo = m.group(1)
            ano = int(m.group(2))
            if tipo == 'EF' and 6 <= ano <= 9:
                return ano, 'fundamental'
            if tipo == 'EM' and 1 <= ano <= 3:
                return ano, 'medio'
    return None, 'outro' 

serie_cat = df['NOMEPROCESSO'].apply(parse_serie_categoria)
df['serie'] = serie_cat.apply(lambda x: x[0])
df['categoria'] = serie_cat.apply(lambda x: x[1])

# 3) Estado de conclusão por área

def area_key(area):
    if not isinstance(area, str):
        return 'outro'
    a = area.strip().upper()
    if 'CIENCIAS HUMANAS' in a:
        return 'ciencias_humanas'
    if 'CIENCIAS DA NATUREZA' in a:
        return 'ciencias_natureza'
    if 'LINGUAGENS' in a:
        return 'linguagens'
    if 'MATEMATICA' in a:
        return 'matematica'

    # Para casos curtos como EM_3 - CH, EM_2 - CN etc.
    parts = [p.strip() for p in re.split(r'[-/]', a) if p.strip()]
    for p in parts:
        if p == 'LI':
            return 'linguagens'
        if p == 'MA':
            return 'matematica'
        if p == 'CH':
            return 'ciencias_humanas'
        if p == 'CN':
            return 'ciencias_natureza'

    return 'outro'


df['area_key'] = df['AREA'].apply(area_key)
df['concluido'] = df['STATUS'].astype(str).str.upper() == 'FINALIZADO'

# 4) Agregar por candidato
key = 'CODCANDIDATO' if 'CODCANDIDATO' in df.columns else 'ID/RA'

groups = []
for cid, sub in df.groupby(key):
    serie_vals = sub['serie'].dropna().unique()
    cat_vals = sub['categoria'].dropna().unique()

    serie = int(serie_vals[0]) if len(serie_vals) == 1 and pd.notna(serie_vals[0]) else None
    categoria = cat_vals[0] if len(cat_vals) == 1 else 'outro'

    status = {
        'linguagens': False,
        'matematica': False,
        'ciencias_humanas': False,
        'ciencias_natureza': False,
    }

    for _, row in sub.iterrows():
        ak = row['area_key']
        if ak in status and row['concluido']:
            status[ak] = True

    concl_fund = categoria == 'fundamental' and status['linguagens'] and status['matematica']
    concl_med = categoria == 'medio' and status['linguagens'] and status['matematica'] and status['ciencias_humanas'] and status['ciencias_natureza']

    groups.append({
        key: cid,
        'serie': serie,
        'categoria': categoria,
        'linguagens': status['linguagens'],
        'matematica': status['matematica'],
        'ciencias_humanas': status['ciencias_humanas'],
        'ciencias_natureza': status['ciencias_natureza'],
        'concluiu_fundamental': concl_fund,
        'concluiu_medio': concl_med,
        'concluiu_prova_unica': concl_fund or concl_med,
    })

res = pd.DataFrame(groups)

# 5) Cálculos solicitados

total_alunos = res.shape[0]

fund = res[res['categoria'] == 'fundamental']
med = res[res['categoria'] == 'medio']

fund_concluida = fund['concluiu_fundamental'].sum()
fund_nao = fund.shape[0] - fund_concluida

med_concluida = med['concluiu_medio'].sum()
med_nao = med.shape[0] - med_concluida

print('\n===== RESULTADOS GERAIS =====')
print('Total de alunos no relatório:', total_alunos)
print('\nEnsino Fundamental:')
print('  Total:', fund.shape[0])
print('  Concluíram Prova Única:', fund_concluida)
print('  Não concluíram Prova Única:', fund_nao)
print('\nEnsino Médio:')
print('  Total:', med.shape[0])
print('  Concluíram Prova Única:', med_concluida)
print('  Não concluíram Prova Única:', med_nao)

# 6) Relatório completo por aluno
res.to_csv('relatorio_prova_unica_analise_Dados_PU.csv', index=False)
print('\nRelatório detalhado salvo em relatorio_prova_unica_analise_Dados_PU.csv')

# Estatística geral de conclusão
percent_total = res['concluiu_prova_unica'].mean() * 100
percent_nao = 100 - percent_total
stats = pd.DataFrame({
    'Status': ['Concluiu', 'Não concluiu'],
    'Quantidade': [res['concluiu_prova_unica'].sum(), res.shape[0] - res['concluiu_prova_unica'].sum()],
    'Percentual': [percent_total, percent_nao]
})
print('\n===== ESTATÍSTICAS DE PROVA ÚNICA =====')
print(stats.to_string(index=False))

# 7) Estatística por série
serie_stats = res.groupby('serie').agg(
    total=('concluiu_prova_unica', 'size'),
    concluiu=('concluiu_prova_unica', 'sum')
).reset_index()
serie_stats['nao_concluiu'] = serie_stats['total'] - serie_stats['concluiu']
serie_stats['pct_concluiu'] = 100 * serie_stats['concluiu'] / serie_stats['total']
serie_stats['pct_nao_concluiu'] = 100 - serie_stats['pct_concluiu']
print('\n===== ESTATÍSTICAS POR SÉRIE =====')
print(serie_stats.to_string(index=False))
serie_stats.to_csv('relatorio_por_serie_Dados_PU.csv', index=False)
print('\nRelatório por série salvo em relatorio_por_serie_Dados_PU.csv')

# 8) Gráficos
plt.figure(figsize=(10, 6))
plt.bar(stats['Status'], stats['Percentual'], color=['#4caf50', '#f44336'])
plt.title('Porcentagem de alunos que concluíram vs não concluíram Prova Única')
plt.xlabel('Status')
plt.ylabel('Percentual (%)')
for i, p in enumerate(stats['Percentual']):
    plt.text(i, p + 1, f'{p:.1f}%', ha='center', fontweight='bold')
plt.ylim(0, 100)
plt.tight_layout()
plt.savefig('grafico_conclusao_prova_unica.png')
print('Gráfico geral salvo em grafico_conclusao_prova_unica.png')
plt.close()

plt.figure(figsize=(12, 6))
x = serie_stats['serie'].astype(str)
plt.bar(x, serie_stats['pct_concluiu'], label='Concluiu (%)', alpha=0.7)
plt.bar(x, serie_stats['pct_nao_concluiu'], bottom=serie_stats['pct_concluiu'], label='Não concluiu (%)', alpha=0.7)
plt.title('Percentual concluído vs não concluído por série (proporção por série)')
plt.xlabel('Série')
plt.ylabel('Percentual (%)')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('grafico_prova_unica_por_serie.png')
print('Gráfico por série salvo em grafico_prova_unica_por_serie.png')
plt.close()

# Densidade por série (ponderado pela quantidade de alunos de cada série)
serie_stats['densidade_concluiu'] = serie_stats['concluiu'] / total_alunos * 100
serie_stats['densidade_nao_concluiu'] = serie_stats['nao_concluiu'] / total_alunos * 100

plt.figure(figsize=(12, 6))
plt.bar(x, serie_stats['densidade_concluiu'], label='Concluiu (densidade % do total)', alpha=0.7)
plt.bar(x, serie_stats['densidade_nao_concluiu'], bottom=serie_stats['densidade_concluiu'], label='Não concluiu (densidade % do total)', alpha=0.7)
plt.title('Densidade por série (concluiu vs não concluiu, % do total de alunos)')
plt.xlabel('Série')
plt.ylabel('Percentual do total (%)')
plt.legend()
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('grafico_prova_unica_por_serie_densidade.png')
print('Gráfico por série (densidade) salvo em grafico_prova_unica_por_serie_densidade.png')
plt.close()
