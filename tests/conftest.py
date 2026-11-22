"""Plugin do pytest que exporta os resultados reais para a interface.

Quando a variável de ambiente CODELAB_RESULTS_PATH está definida, o laboratório
escreve um JSON com o estado, a duração e as propriedades de cada teste. É este
ficheiro que a página de validação apresenta — nunca valores fixos.

Exemplo:

    CODELAB_RESULTS_PATH=data/resultados_testes.json pytest -q
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

_RESULTADOS = []


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    propriedades = dict(report.user_properties)
    _RESULTADOS.append(
        {
            "nodeid": report.nodeid,
            "nome": report.nodeid.split("::")[-1],
            "estado": report.outcome,
            "duracao": round(report.duration, 4),
            "descricao": propriedades.get("descricao", ""),
            "esperado": propriedades.get("esperado", ""),
            "obtido": propriedades.get("obtido", ""),
            "detalhe": str(report.longrepr) if report.failed else "",
        }
    )


def pytest_sessionfinish(session, exitstatus):
    destino = os.environ.get("CODELAB_RESULTS_PATH")
    if not destino:
        return

    gerado_em = datetime.now(timezone(timedelta(hours=1))).isoformat(timespec="seconds")
    with open(destino, "w", encoding="utf-8") as ficheiro:
        json.dump(
            {
                "exitstatus": int(exitstatus),
                "gerado_em": gerado_em,
                "resultados": _RESULTADOS,
                "aprovados": sum(r["estado"] == "passed" for r in _RESULTADOS),
                "falhados": sum(r["estado"] == "failed" for r in _RESULTADOS),
                "total": len(_RESULTADOS),
            },
            ficheiro,
            ensure_ascii=False,
            indent=2,
        )
