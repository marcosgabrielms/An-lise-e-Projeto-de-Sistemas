from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

DATABASE_URL = "sqlite:///./test.db"  # Use o banco de dados de sua preferência

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100))
    endereco = Column(String(200))
    telefone = Column(String(20))
    bairro = Column(String(100))

class Pedido(Base):
    __tablename__ = "pedido"
    id_pedido = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    data_pedido = Column(TIMESTAMP)
    sabor = Column(String(100))
    tamanho = Column(String(50))

    cliente = relationship("Cliente")

# (Outros modelos permanecem os mesmos ou atualize conforme necessário)

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/clientes/novo")
def create_cliente(
    request: Request,
    nome: str = Form(...),
    endereco: str = Form(...),
    telefone: str = Form(...),
    bairro: str = Form(...),
    db: Session = Depends(get_db)
):
    cliente = Cliente(
        nome=nome,
        endereco=endereco,
        telefone=telefone,
        bairro=bairro
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return RedirectResponse(url="/", status_code=303)

@app.post("/pedidos/novo")
def create_pedido(
    request: Request,
    sabor: str = Form(...),
    tamanho: str = Form(...),
    db: Session = Depends(get_db)
):
    # Aqui, para simplificar, associamos o pedido ao primeiro cliente
    cliente = db.query(Cliente).first()
    if not cliente:
        raise HTTPException(status_code=400, detail="Nenhum cliente cadastrado.")
    
    pedido = Pedido(
        id_cliente=cliente.id_cliente,
        sabor=sabor,
        tamanho=tamanho
    )
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return RedirectResponse(url="/", status_code=303)
