import pandas as pd

from pathlib import Path
import requests
import wget

DOWNLOAD_URLS = [
    'https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2022.zip',
    'https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_PB.zip',
    'https://cdn.tse.jus.br/estatistica/sead/odsele/prestacao_contas/prestacao_de_contas_eleitorais_candidatos_2022.zip',
    'https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_2022.zip'
]

OUTPUT_DIR = 'dados/tse'

def download_file(url, output_dir='.'):
    local_filename = Path(output_dir) / url.split('/')[-1]
    with requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'}) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def main():
    for url in DOWNLOAD_URLS:
        print("Downloading ", url)
        download_file(url, OUTPUT_DIR)

if __name__ == "__main__":
    main()