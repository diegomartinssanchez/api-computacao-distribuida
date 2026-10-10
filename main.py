import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Carrega as variáveis do ficheiro .env
load_dotenv()

app = FastAPI()

# Modelo de dados usando Pydantic
class Item(BaseModel):
    id: int
    nome: str
    preco: float

# Rota 1: GET / (Retorna página HTML estilizada com hiperligações para as rotas)
@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de Computação Distribuída</title>
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            body {
                background-color: #0f172a;
                color: #f8fafc;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 20px;
            }
            .card {
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 16px;
                padding: 36px;
                max-width: 480px;
                width: 100%;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            }
            .badge {
                display: inline-block;
                background-color: #0ea5e9;
                color: #ffffff;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                padding: 4px 10px;
                border-radius: 9999px;
                margin-bottom: 12px;
            }
            h1 {
                font-size: 24px;
                font-weight: 700;
                color: #f1f5f9;
                margin-bottom: 8px;
            }
            p {
                font-size: 14px;
                color: #94a3b8;
                margin-bottom: 24px;
            }
            .nav-links {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .link-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                background-color: #334155;
                color: #f8fafc;
                text-decoration: none;
                padding: 14px 18px;
                border-radius: 10px;
                font-weight: 500;
                font-size: 14px;
                transition: all 0.2s ease;
                border: 1px solid transparent;
            }
            .link-item:hover {
                background-color: #475569;
                border-color: #38bdf8;
                transform: translateY(-2px);
            }
            .tag {
                background-color: #0f172a;
                color: #38bdf8;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 12px;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <span class="badge">FastAPI + Docker</span>
            <h1>API de Computação Distribuída</h1>
            <p>Selecione um dos recursos abaixo para navegar pelos endpoints disponíveis:</p>
            <div class="nav-links">
                <a href="/docs" class="link-item" target="_blank">
                    <span>Documentação Interativa</span>
                    <span class="tag">/docs</span>
                </a>
                <a href="/health" class="link-item">
                    <span>Verificação de Estado</span>
                    <span class="tag">/health</span>
                </a>
                <a href="/config/envs" class="link-item">
                    <span>Variáveis de Ambiente</span>
                    <span class="tag">/config/envs</span>
                </a>
            </div>
        </div>
    </body>
    </html>
    """

# Rota 2: GET /health (Indicação de que a aplicação está a funcionar)
@app.get("/health")
async def health():
    return {"status": "ok", "app": "em execucao"}

# Rota 3: GET /config/envs (Retorna as variáveis de ambiente)
@app.get("/config/envs")
async def get_envs():
    return {
        "APP_NAME": os.getenv("APP_NAME", "Nao definido"),
        "AMBIENTE": os.getenv("AMBIENTE", "Nao definido"),
        "VERSAO": os.getenv("VERSAO", "Nao definido")
    }

# Rota 4: POST /items (Cria lista de itens e retorna com tratamento mínimo)
@app.post("/items")
async def criar_items(items: List[Item]):
    items_processados = []
    for item in items:
        items_processados.append({
            "id": item.id,
            "nome": item.nome.upper(),
            "preco": item.preco
        })
    return {"total": len(items_processados), "items": items_processados}