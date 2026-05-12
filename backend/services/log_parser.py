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
import re


def detectar_tipo_erro(conteudo_log: str) -> str:
    linhas = conteudo_log.splitlines()[-50:]
    trecho = "\n".join(linhas).lower()

    if "bisync critical" in trecho:
        return "CRITICAL"

    if re.search(r"rate limit|timeout|connection|503", trecho):
        return "TRANSIENT"

    return "UNKNOWN"