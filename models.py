from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)


class Livro(Base):  # Renomeado para Livro (singular)
    __tablename__ = 'livros'  # Renomeado para letras minúsculas e plural
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)  # Adicionado tamanho máximo
    autor = Column(String(100), nullable=False)  # Adicionado tamanho máximo
    descricao = Column(String(500), nullable=False)  # Adicionado tamanho máximo
    categoria = Column(String(50), nullable=False)  # Adicionado tamanho máximo

    def serialize(self):
        """Converte o objeto Livro em um dicionário."""
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
            return None  # Ou levante a exceção, dependendo do seu caso de uso


Base.metadata.create_all(engine)  # Cria as tabelas
