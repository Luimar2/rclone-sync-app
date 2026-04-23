import re


def detectar_tipo_erro(conteudo_log: str) -> str:
    linhas = conteudo_log.splitlines()[-50:]
    trecho = "\n".join(linhas).lower()

    if "bisync critical" in trecho:
        return "CRITICAL"

    if re.search(r"rate limit|timeout|connection|503", trecho):
        return "TRANSIENT"

    return "UNKNOWN"