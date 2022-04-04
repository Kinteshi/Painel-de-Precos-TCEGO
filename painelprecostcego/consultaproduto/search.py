from whoosh.index import open_dir
from whoosh.qparser import QueryParser, FuzzyTermPlugin
from painelprecostcego.settings import WHOOSH_DIR
from unidecode import unidecode

ix = open_dir(WHOOSH_DIR)

qp = QueryParser('description', ix.schema)
qp.add_plugin(FuzzyTermPlugin())


def search_produto(query, N=100):
    query = unidecode(query).lower()
    q = qp.parse(query)
    results = ix.searcher().search(
        q,
        limit=N,
    )
    return results
