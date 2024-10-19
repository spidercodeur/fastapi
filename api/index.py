import asyncpg
import os
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# Connexion à PostgreSQL
async def connect_to_db():
    conn = await asyncpg.connect(os.getenv("POSTGRES_URL"))
    return conn

# Modèle de données pour la mise à jour du message
class MessageUpdate(BaseModel):
    message: str

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

# Créer la table si elle n'existe pas
async def create_table(conn):
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        message TEXT NOT NULL
    )
    """)

# Route GET pour lire le message actuel
@app.get("/api/py/readMessage")
async def read_message():
    conn = await connect_to_db()
    query = "SELECT message FROM messages ORDER BY id DESC LIMIT 1"
    result = await conn.fetchrow(query)
    await conn.close()
    return {"message": result["message"]} if result else {"message": "Default message"}

# Route PUT pour mettre à jour le message
@app.put("/api/py/updateMessage")
async def update_message(message_update: MessageUpdate, x_token: str = Header(...)):
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    conn = await connect_to_db()
    query = "INSERT INTO messages (message) VALUES ($1)"
    await conn.execute(query, message_update.message)
    await conn.close()
    return {"updated_message": message_update.message}

# Vérification du fonctionnement du serveur
@app.get("/api/py/healthcheck")
def healthchecker():
    return {"status": "success", "message": "Integrated FastAPI Framework with Next.js successfully!"}

# Création de la table à la connexion
@app.on_event("startup")
async def startup():
    conn = await connect_to_db()
    await create_table(conn)
    await conn.close()
