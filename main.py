import uuid

from sqlalchemy import Column, Uuid, String, DateTime, func, DECIMAL, Integer, Boolean, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, relationship, Session

motor = create_engine("sqlite+pysqlite:///banco_de_dados.sqlite", echo=False)

"""
alembic init migrations
alembic revision --autogenerate -m "Migracao inicial"
alembic upgrade head
Editar o alembic.ini com a string de conexao do banco
Editar o migrations/env.py linha 18 e 19 para
    from main import Base
    target_metadata = Base.metadata
"""


class Base(DeclarativeBase):
    pass


class DatasMixin:
    dta_cadastro = Column(DateTime, server_default=func.now(), nullable=False)
    dta_atualizacao = Column(DateTime, onupdate=func.now(), default=func.now(), nullable=False)


class Categoria(Base, DatasMixin):
    __tablename__ = 'tbl_categorias'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(256), nullable=False)

    # Propriedade de navegação
    lista_de_produtos = relationship("Produto", back_populates="categoria",
                                     cascade="all, delete-orphan", lazy="selectin")


class Produto(Base, DatasMixin):
    __tablename__ = 'tbl_produtos'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(256), nullable=False)
    preco = Column(DECIMAL(10, 2), default=0.00)
    estoque = Column(Integer, default=0)
    ativo = Column(Boolean, default=True)
    categoria_id = Column(Uuid(as_uuid=True), ForeignKey("tbl_categorias.id"))

    # Propriedade de navegação
    categoria = relationship("Categoria", back_populates="lista_de_produtos")


def seed_database():
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

def incluir_categoria():
    print("Incluindo categoria")
    nome = input("Qual o nome da categoria que você quer adicionar? ")
    with Session(motor) as sessao:
        categoria = Categoria()
        categoria.nome = nome
        sessao.add(categoria)
        sessao.commit()
    print(f"Categoria {nome} adicionada.")


def listar_categorias():
    print("Categorias cadastradas")
    print(f"Nome                                      # Produtos")
    print(f"----------------------------------------- ----------")
    stmt = select(Categoria)
    stmt = stmt.order_by("nome")
    with Session(motor) as sessao:
        rset = sessao.execute(stmt).scalars()
        for categoria in rset:
            print(f"{categoria.nome:40s}  {len(categoria.lista_de_produtos):10d}")
            # for produto in categoria.lista_de_produtos:
            #     print(f"   {produto.nome}")
    print(f"----------------------------------------- ----------")


if __name__ == "__main__":
    seed_database()
    while True:
        print("Menu de opcoes")
        print("1. Incluir categoria")
        print("2. Listar categorias")
        print("0. Sair")
        opcao = int(input("Qual opcao? "))
        if opcao == 1:
            incluir_categoria()
        elif opcao == 2:
            listar_categorias()
        elif opcao == 0:
            exit(0)
        else:
            print("Opcao invalida...")