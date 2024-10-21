import asyncpg
import os
from fastapi import FastAPI, Request,Header,HTTPException,status
from pydantic import BaseModel
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

# Connexion à PostgreSQL
async def connect_to_db():
    conn = await asyncpg.connect(os.getenv("POSTGRES_URL"))
    return conn

# Modèle de données pour la mise à jour du message et de la couleur
class MessageUpdate(BaseModel):
    message: str
    color: str  # Code couleur en hexadécimal (ex : #FF5733)

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

# Créer la table si elle n'existe pas avec les colonnes `message` et `color`
async def create_table(conn):
    await conn.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        message TEXT NOT NULL,
        color VARCHAR(7) NOT NULL -- Stocker la couleur en hexadécimal
    );
    
    -- Insérer un message par défaut si la table est vide
    INSERT INTO messages (id, message, color) 
    VALUES (1, 'Default message', '#111111')
    ON CONFLICT (id) DO NOTHING;
    """)

# Route GET pour lire le message actuel et la couleur
@app.get("/api/py/readMessage")
async def read_message():
    conn = await connect_to_db()
    query = "SELECT message, color FROM messages WHERE id = 1"
    result = await conn.fetchrow(query)
    await conn.close()
    return {"message": result["message"], "color": result["color"]} if result else {"message": "Default message", "color": "#FFFFFF"}

# Route PUT pour mettre à jour le message et la couleur
@app.put("/api/py/updateMessage")
async def update_message(message_update: MessageUpdate, x_token: str = Header(...)):
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    
    # La couleur par défaut est déjà gérée par le modèle, mais tu peux toujours vérifier si besoin
    color_to_use = message_update.color if message_update.color else "#000000"
    
    conn = await connect_to_db()
    query = "UPDATE messages SET message = $1, color = $2 WHERE id = 1"
    await conn.execute(query, message_update.message, color_to_use)
    await conn.close()
    
    return {"updated_message": message_update.message, "updated_color": color_to_use}

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