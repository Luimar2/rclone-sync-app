from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.config import router as config_router
from routes.sync import router as sync_router
from routes.agendamento import router as agendamento_router
from routes.logs import router as logs_router


app = FastAPI(
    title="RcloneSync",
    description="Interface gráfica para gerenciar backups com rclone",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # porta padrão do Vite
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router)
app.include_router(sync_router)
app.include_router(agendamento_router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "RcloneSync API rodando"}


app.include_router(logs_router)