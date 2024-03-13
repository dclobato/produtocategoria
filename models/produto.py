import uuid

from sqlalchemy import Column, Uuid, String, DECIMAL, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base, DatasMixin


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
