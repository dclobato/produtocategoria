from sqlalchemy import select
from sqlalchemy.orm import Session

from models.categoria import Categoria
from models.produto import Produto


def seed_database(motor):
    with Session(motor) as sessao:
        if sessao.execute(select(Categoria).limit(1)).scalar_one_or_none():
            return
        from seed import seed_data
        for categoria in seed_data:
            cat = Categoria()
            print(f"Semeando a categoria {categoria['categoria']}...")
            cat.nome = categoria["categoria"]
            for produto in categoria["produtos"]:
                p = Produto()
                p.nome = produto["nome"]
                p.preco = produto["preco"]
                p.estoque = 0
                p.ativo = True
                p.categoria = cat
                sessao.add(p)
            sessao.commit()
