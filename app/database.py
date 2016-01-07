# -*- encoding: utf-8 -*-
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime as dt

engine = create_engine(config.DATABASE_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

class SuperSaver(Base):
    __tablename__ = "supersaver"

    id = Column(Integer, primary_key=True)
    cupom = Column(String(50), unique=True)
    usado = Column(Boolean)

    def __init__(self,cupom):
        self.cupom = cupom
        self.usado = False


class Venda(Base):
    __tablename__ = 'vendas'
    # id_pagador - Identificador que vai junto à venda no Moip
    id = Column(Integer, primary_key=True)
    #Id da transacao que vai junto à venda no Moip
    id_proprio = Column(String(100), unique=True)
    data_hora = Column(DateTime)
    quantidade = Column(Integer)
    nome_cliente = Column(String(200))
    telefone_cliente = Column(String(50))
    email_cliente = Column(String(500))
    cpf_cliente = Column(String(20))
    pagamento = Column(String(100))
    email_enviado = Column(Boolean)
    data_envio = Column(String(50))
    token_moip = Column(String(1000))
    cupom_usado = Column(String(50))
    super_savers = Column(String(2000))
    valor_pago = Column(Float)
    falhou = Column(Boolean)

    def __init__(self, nome):
        self.falhou = False
        self.pagamento = "Cartao"
        self.nome_cliente = nome
        self.data_hora = dt.now()
        self.id_proprio = dt.now().strftime("V%m%d%H%M%S")

    def __repr__(self):
        return '<Venda %r>' % (self.nome_cliente)

#============================================================================

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

def create(obj):
    db_session.add(obj)
    db_session.commit()
