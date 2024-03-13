import uuid

from sqlalchemy import Column, Uuid, String
from sqlalchemy.orm import relationship

from models.base import Base, DatasMixin


class Categoria(Base, DatasMixin):
    __tablename__ = 'tbl_categorias'

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(256), nullable=False)

    # Propriedade de navegação
    lista_de_produtos = relationship("Produto", back_populates="categoria",
                                     cascade="all, delete-orphan", lazy="selectin")
