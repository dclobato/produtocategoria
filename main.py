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

    categoria = relationship("Categoria", back_populates="lista_de_produtos")


# cat = Categoria()
# cat.nome = "Salgadinhos"
#
# prod = Produto()
# prod.nome = "Doritos, 600g"
# prod.ativo = True
# prod.preco = 12.74
# prod.estoque = 0
# prod.categoria = cat
#
# with Session(motor) as sessao:
#     sessao.add(prod)
#     sessao.commit()

with Session(motor) as sessao:
    lista_de_categorias = sessao.execute(select(Categoria)).scalars()
    for categoria in lista_de_categorias:
        print(f"A categoria {categoria.nome} tem {len(categoria.lista_de_produtos)} produtos")
        for produto in categoria.lista_de_produtos:
            print(f"    Produto {produto.nome} que tem {produto.estoque} unidades no estoque")
