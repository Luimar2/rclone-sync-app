# RcloneSync - Interface gráfica para rclone com Google Drive no Linux
# Copyright (C) 2026 Luimar2
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from routes.config import router as config_router
from routes.sync import router as sync_router
from routes.logs import router as logs_router
from routes.agendamento import router as agendamento_router

app = FastAPI(
    title="RcloneSync",
    description="Interface gráfica para gerenciar backups com rclone",
    version="0.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(config_router)
app.include_router(sync_router)
app.include_router(logs_router)
app.include_router(agendamento_router)

# Serve o frontend compilado se existir
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "dist"
INSTALL_FRONTEND = Path.home() / ".local/share/rclone-sync-app/frontend"

def frontend_path() -> Path | None:
    if INSTALL_FRONTEND.exists():
        return INSTALL_FRONTEND
    if FRONTEND_DIR.exists():
        return FRONTEND_DIR
    return None

frontend = frontend_path()

if frontend:
    app.mount("/assets", StaticFiles(directory=frontend / "assets"), name="assets")

    @app.get("/")
    async def root():
        return FileResponse(frontend / "index.html")

    @app.get("/{full_path:path}")
    async def spa_fallback(full_path: str):
        # Rotas da API não caem aqui pois são registradas antes
        index = frontend / "index.html"
        return FileResponse(index)
else:
    @app.get("/")
    async def root():
        return {"status": "ok", "message": "Frontend não compilado ainda."}