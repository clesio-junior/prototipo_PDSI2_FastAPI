from pydantic import BaseModel

class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool = True

class Menu(BaseModel):
    menuNav: str
    link: str
    