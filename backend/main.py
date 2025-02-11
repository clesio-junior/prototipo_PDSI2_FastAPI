from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
#aaa
import requests
from bs4 import BeautifulSoup
#aaaa

from typing import List
from fastapi.middleware.cors import CORSMiddleware

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
 'http://localhost:3000'
]
app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=['*'],
 allow_headers=['*']
)


@app.get("/")
def read_root():
    return {"Hello" : "lala"}


@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/quadrado/{num}")
def square (num: int):
    return num ** 2


@app.post("/desafioUFU", status_code=status.HTTP_201_CREATED)
def criar_valores1(db: Session = Depends(get_db)):
    url = "https://ufu.br/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    barra_esquerda = soup.find('ul', class_="sidebar-nav nav-level-0")
    linhas_barra_esquerda = barra_esquerda.find_all('a', class_='nav-link')

    iniciar = False  # Flag para controlar quando começar
    menus_inseridos = []  # Lista para armazenar os menus inseridos

    for linha in linhas_barra_esquerda:
        if linha.text.strip() == "Graduação":  # Verifica se encontrou o texto "Graduação"
            iniciar = True  # Ativa a flag para começar a imprimir nas próximas iterações

        if iniciar:
            print(linha.text.strip())  # Exibe o texto do link
            menuNav = linha.text.strip()
            link = "https://ufu.br"+linha.get('href')

            novo_menu = model.Model_Menu(menuNav=menuNav, link=link)
    
            db.add(novo_menu)
            menus_inseridos.append(novo_menu)

    if menus_inseridos:
        db.commit()  # Commit para salvar todos os menus
        return {"Menus": [menu.menuNav for menu in menus_inseridos]}  # Retorna todos os menus inseridos
    
    else:
        return {"message": "Nenhum menu foi inserido."}  # Resposta mais estruturada para quando não houver menus

@app.get("/mensagens", response_model =List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens