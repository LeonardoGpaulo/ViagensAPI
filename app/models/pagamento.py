from sqlalchemy import Column, BigInteger, Integer, DECIMAL, DateTime, ForeignKey
from app.database import Base


class PagamentoModels(Base):
    __tablename__ = "pagamento"

    id_pagamento = Column(BigInteger, primary_key=True, autoincrement=True)
    id_metodo_pagamento = Column(Integer,ForeignKey("metodo_pagamento.id_metodo_pagamento"))
    id_corrida = Column(BigInteger, ForeignKey("corrida.id_corrida"))
    
    valor = Column(DECIMAL(10,2))
    datahora_transacao = Column(DateTime)