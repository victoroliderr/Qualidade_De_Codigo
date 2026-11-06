from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from components import (
    carregar_css,
    hero,
    section_title,
    card,
    test_row,
    console,
    callout,
    stat,
)
from components.componentes_visuais import badge

carregar_css()

CATALOGO = [
    ("test_cliente_comum", "Cliente COMUM — sem desconto", "R$ 100,00"),
    ("test_cliente_vip", "Cliente VIP — desconto de 10%", "R$ 90,00"),
    ("test_cliente_premium", "Cliente PREMIUM — desconto de 15%", "R$ 170,00"),
    (
        "test_equivalencia_entre_implementacoes",
        "Equivalência de comportamento entre as duas versões",
        "Mesmo valor e fatura idêntica",
    ),
    ("test_multiplos_produtos", "Múltiplos produtos — soma correcta", "R$ 130,00"),
    (
        "test_tipo_cliente_sem_desconto",
        "Tipo de cliente desconhecido — sem desconto",
        "R$ 100,00",
    ),
]

hero(
    "Ambiente de execução · pytest",
    "Testes automatizados",
    "A suíte é executada num subprocesso real. A interface lê o relatório produzido pelo pytest e mostra o estado efectivo de cada teste.",
    ["6 testes", "pytest", "resultados reais"],
)

if "resultado_testes" not in st.session_state:
    st.session_state.resultado_testes = None


def executar_pytest():
    descritor, caminho = tempfile.mkstemp(prefix="codelab_pytest_", suffix=".json")
    os.close(descritor)
    ambiente = os.environ.copy()
    ambiente["CODELAB_RESULTS_PATH"] = caminho
    comando = [
        sys.executable,
        "-m",
        "pytest",
        "tests/test_processamento_pedidos.py",
        "-v",
        "--tb=short",
        "-p",
        "no:cacheprovider",
    ]
    inicio = time.perf_counter()
    processo = subprocess.run(
        comando,
        cwd=ROOT,
        env=ambiente,
        capture_output=True,
        text=True,
        timeout=180,
    )
    duracao = time.perf_counter() - inicio
    dados = None
    try:
        with open(caminho, encoding="utf-8") as ficheiro:
            dados = json.load(ficheiro)
    except (OSError, json.JSONDecodeError):
        dados = None
    finally:
        try:
            os.unlink(caminho)
        except OSError:
            pass
    return {
        "dados": dados,
        "stdout": processo.stdout,
        "stderr": processo.stderr,
        "returncode": processo.returncode,
        "duracao": duracao,
        "comando": " ".join(comando),
    }


col_info, col_botao = st.columns([1.7, 1.3], gap="medium")
with col_info:
    st.markdown(
        '<div class="cl-callout"><strong>O que a suíte verifica:</strong> os três casos do '
        "relatório académico (COMUM, VIP e PREMIUM), a equivalência entre implementações, "
        "o cálculo com múltiplos produtos e o comportamento de um tipo de cliente sem taxa "
        "de desconto.</div>",
        unsafe_allow_html=True,
    )
with col_botao:
    st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)
    correr = st.button("EXECUTAR TESTES AUTOMATIZADOS", type="primary", use_container_width=True)

if correr:
    try:
        with st.status("A executar o pytest…", expanded=True) as estado:
            st.write("A recolher os testes de `tests/test_processamento_pedidos.py`.")
            resultado = executar_pytest()
            st.write(f"Processo terminado com código de saída {resultado['returncode']}.")
            estado.update(
                label=f"pytest concluído em {resultado['duracao']:.2f}s",
                state="complete" if resultado["dados"] else "error",
                expanded=False,
            )
        st.session_state.resultado_testes = resultado
    except FileNotFoundError:
        st.session_state.resultado_testes = {
            "dados": None,
            "stdout": "",
            "stderr": "pytest não está instalado neste ambiente.",
            "returncode": -1,
            "duracao": 0.0,
            "comando": "",
        }
    except subprocess.TimeoutExpired:
        st.session_state.resultado_testes = {
            "dados": None,
            "stdout": "",
            "stderr": "A execução do pytest excedeu o limite de 180 segundos.",
            "returncode": -1,
            "duracao": 180.0,
            "comando": "",
        }
    except Exception as excecao:  # pragma: no cover - apresentado na interface
        st.session_state.resultado_testes = {
            "dados": None,
            "stdout": "",
            "stderr": f"{type(excecao).__name__}: {excecao}",
            "returncode": -1,
            "duracao": 0.0,
            "comando": "",
        }

resultado = st.session_state.resultado_testes

if resultado is None:
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("Testes planeados", "Estado pendente até à primeira execução real.")
    for nome, descricao, esperado in CATALOGO:
        test_row(nome, descricao, esperado, "—", "pending")
else:
    dados = resultado["dados"]
    if dados is None:
        st.error(
            "Não foi possível obter o relatório do pytest. Verifica se o pytest está "
            "instalado no ambiente activo: `python -m pip install pytest`."
        )
        if resultado["stdout"] or resultado["stderr"]:
            console(resultado["stdout"] + "\n" + resultado["stderr"])
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        section_title("Resumo da execução", "Números lidos directamente do relatório do pytest.")
        c1, c2, c3, c4 = st.columns(4, gap="medium")
        with c1:
            stat(str(dados["total"]), "Testes recolhidos", "Executados nesta sessão", "accent")
        with c2:
            stat(str(dados["aprovados"]), "Aprovados", "Estado passed", "green")
        with c3:
            stat(str(dados["falhados"]), "Falhados", "Estado failed", "red" if dados["falhados"] else "")
        with c4:
            stat(f"{resultado['duracao']:.2f}s", "Duração do subprocesso", "Tempo real de execução", "")

        if dados["total"] == 0:
            st.markdown(
                '<div class="cl-callout danger"><strong>NENHUM TESTE RECOLHIDO</strong><br>'
                "O pytest terminou sem recolher testes. Verifica a consola e o caminho do "
                "ficheiro de testes.</div>",
                unsafe_allow_html=True,
            )
        elif dados["falhados"] == 0:
            st.markdown(
                '<div class="cl-callout success"><strong>SUÍTE APROVADA</strong><br>'
                f'{dados["aprovados"]} de {dados["total"]} testes passaram. A interface não '
                "fixou este resultado: ele foi lido do relatório gerado pelo pytest.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="cl-callout danger"><strong>EXISTEM FALHAS</strong><br>'
                f'{dados["falhados"]} teste(s) falharam. Consulta o detalhe e a consola abaixo.</div>',
                unsafe_allow_html=True,
            )

        section_title("Resultados por teste", "Nome, descrição, valor esperado, valor obtido e estado.")
        for item in dados["resultados"]:
            test_row(
                item["nome"],
                item["descricao"] or "Sem descrição.",
                item["esperado"] or "—",
                item["obtido"] or "—",
                item["estado"],
                f"{item['duracao']:.3f}s",
            )
            if item["estado"] == "failed" and item["detalhe"]:
                with st.expander(f"Detalhe da falha · {item['nome']}"):
                    console(item["detalhe"])

        section_title("Consola do pytest", "Saída integral do subprocesso.")
        with st.expander("Mostrar stdout / stderr", expanded=False):
            console(resultado["stdout"] or "(stdout vazio)")
            if resultado["stderr"]:
                st.caption("stderr")
                console(resultado["stderr"])

        st.caption(f"Comando executado: `{resultado['comando']}`")

st.markdown("<br>", unsafe_allow_html=True)
section_title("Porque é que estes testes importam", "A refatoração só é segura quando o comportamento é verificado.")
t1, t2, t3 = st.columns(3, gap="medium")
with t1:
    card("Casos do relatório", "COMUM, VIP e PREMIUM verificam as três regras de desconto com os valores oficiais: 100, 90 e 170.", "accent", "01")
with t2:
    card("Equivalência", "O mesmo pedido é executado nas duas versões e compara-se o valor devolvido e o texto da fatura.", "violet", "02")
with t3:
    card("Robustez", "Múltiplos produtos e tipos sem taxa confirmam que o comportamento se mantém fora dos casos básicos.", "green", "03")
