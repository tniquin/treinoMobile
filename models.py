from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)


class Livro(Base):
    __tablename__ = 'livros'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=False)
    categoria = Column(String(50), nullable=False)

    def serialize(self):
        try:
            dados = {
                "titulo": self.titulo,
                "autor": self.autor,
                "descricao": self.descricao,
                "categoria": self.categoria,
            }
            return dados
        except Exception as e:
            print(f"Erro ao serializar o livro: {e}")
            return None

class Nome(Base):
    __tablename__ = 'Nomes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    profissao = Column(String(200), nullable=False)
    salario = Column(String(200), nullable=False)


    def serialize(self):
        try:
            dados = {
                "nome": self.nome,
                "profissao": self.profissao,
                "salario": self.salario,
            },
            return dados
        except Exception as e:
            print(f"Erro ao serializar o Pessoa: {e}")
            return None

Base.metadata.create_all(engine)
