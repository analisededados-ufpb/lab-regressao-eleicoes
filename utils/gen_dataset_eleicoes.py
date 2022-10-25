import pandas as pd
from pathlib import Path
import zipfile

DATA_DIR = Path().resolve().parent / 'dados'
TSE_DATA_DIR = DATA_DIR / 'tse'

def read_tse_csv_from_zip(zip_file, csv_file):
    zf = zipfile.ZipFile(zip_file)
    with zf.open(csv_file) as csv_f:
        return pd.read_csv(csv_f, encoding='latin1', delimiter=';', decimal=',')  

candidatos = (
    read_tse_csv_from_zip(TSE_DATA_DIR / 'consulta_cand_2022.zip',
                          'consulta_cand_2022_PB.csv')
    .query("DS_CARGO == 'DEPUTADO ESTADUAL'")
    .set_index('SQ_CANDIDATO')
)
candidatos

votacao = (
    read_tse_csv_from_zip(TSE_DATA_DIR / 'votacao_secao_2022_PB.zip',
                          'votacao_secao_2022_PB.csv')
    .groupby(['SQ_CANDIDATO'])
    .agg({'QT_VOTOS': 'sum'})
)
votacao

receitas = (
    read_tse_csv_from_zip(
        TSE_DATA_DIR / 'prestacao_de_contas_eleitorais_candidatos_2022.zip',
        'receitas_candidatos_2022_PB.csv')
    .groupby(['SQ_CANDIDATO'])
    .agg({'VR_RECEITA': 'sum'})

)
receitas

bens = (
    read_tse_csv_from_zip(TSE_DATA_DIR / 'bem_candidato_2022.zip',
                          'bem_candidato_2022_PB.csv')
    .groupby(['SQ_CANDIDATO'])
    .agg({'VR_BEM_CANDIDATO': 'sum'})
)
bens

df = (
    candidatos
    .join(votacao)
    .join(receitas)
    .join(bens)
    .filter(['ANO_ELEICAO', 'SG_UF', 'DS_CARGO', 'NR_CANDIDATO', 'NM_URNA_CANDIDATO',
             'SG_PARTIDO', 'DT_NASCIMENTO', 'NR_IDADE_DATA_POSSE', 'DS_GENERO',
             'DS_GRAU_INSTRUCAO', 'DS_ESTADO_CIVIL', 'DS_COR_RACA', 'DS_OCUPACAO',
             'DS_SIT_TOT_TURNO', 'QT_VOTOS', 'VR_RECEITA', 'VR_BEM_CANDIDATO'             
    ])
)
df
df.to_csv(DATA_DIR / 'eleicao_2022_pb_deputado_estadual.csv')
