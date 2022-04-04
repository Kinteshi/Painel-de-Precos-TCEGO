from whoosh.fields import Schema, TEXT, ID, STORED, NUMERIC
from whoosh.index import create_in
import os
import pandas as pd


if __name__ == '__main__':
    schema = Schema(
        ean=TEXT(stored=True),
        description=TEXT(stored=True),
        price=STORED,
        )

    if not os.path.exists('whoosh_index'):
        os.mkdir('whoosh_index')

    ix = create_in('whoosh_index', schema)

    writer = ix.writer()
    
    df = pd.read_csv('../../data/nfedata_clean_non_empty_ean_desc.csv', low_memory=False) # Inserção de dados espera descrição limpa e normalizada de dados que contenham ean

    for index, row in df.iterrows():
        writer.add_document(
            ean=str(row['produto_codigo_ean']),
            description=row['produto_descricao'],
            price=row['produto_valor_unidade']
            )
    writer.commit()
