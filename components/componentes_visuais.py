"""Componentes visuais reutilizáveis do CODELAB."""
from __future__ import annotations

import difflib
import html
import re
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent


def carregar_css():
    css = (ROOT / "assets" / "estilos.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def esc(texto: str) -> str:
    return html.escape(str(texto), quote=False)


def ler_codigo(nome_ficheiro: str) -> str:
    return (ROOT / "implementacoes" / nome_ficheiro).read_text(encoding="utf-8")


def sidebar_brand():
    st.sidebar.markdown(
        """<div class="cl-brand">
        <div class="cl-brand-mark">
          <span class="cl-brand-logo">&lt;/&gt;</span>
          <div>
            <div class="cl-brand-name">CODELAB</div>
            <div class="cl-brand-sub">Qualidade do Código<br>e Refatoração</div>
          </div>
        </div>
        <div class="cl-sidebar-note">
          <strong>Laboratório interactivo</strong><br>
          Python · Streamlit · pytest
        </div>
        </div>""",
        unsafe_allow_html=True,
    )


def hero(kicker: str, titulo: str, subtitulo: str, meta: list[str] | None = None):
    badges = ""
    if meta:
        badges = '<div class="cl-hero-meta">' + "".join(
            f'<span class="cl-badge cl-badge-blue">{esc(m)}</span>' for m in meta
        ) + "</div>"
    st.markdown(
        f"""<div class="cl-hero cl-fade-in">
        <div class="cl-kicker">{esc(kicker)}</div>
        <div class="cl-hero-title">{esc(titulo)}</div>
        <p class="sub">{esc(subtitulo)}</p>
        {badges}
        </div>""",
        unsafe_allow_html=True,
    )


def section_title(titulo: str, subtitulo: str = "", eyebrow: str = ""):
    eyebrow_html = f'<div class="cl-eyebrow">{esc(eyebrow)}</div>' if eyebrow else ""
    sub_html = f"<p>{esc(subtitulo)}</p>" if subtitulo else ""
    st.markdown(
        f'<div class="cl-section-head">{eyebrow_html}<h2>{esc(titulo)}</h2>{sub_html}</div>',
        unsafe_allow_html=True,
    )


def card(titulo: str, texto: str, variante: str = "", icon: str = "", foot: str = ""):
    cls = f"cl-card cl-card-{variante}" if variante else "cl-card"
    icon_cls = variante if variante in {"violet", "green", "amber", "red"} else ""
    icon_html = f'<div class="cl-card-icon {icon_cls}">{esc(icon)}</div>' if icon else ""
    foot_html = f'<div class="cl-card-foot">{esc(foot)}</div>' if foot else ""
    st.markdown(
        f'<div class="{cls}">{icon_html}<h4>{esc(titulo)}</h4>'
        f"<p>{esc(texto)}</p>{foot_html}</div>",
        unsafe_allow_html=True,
    )


def stat(valor: str, label: str, hint: str = "", variante: str = ""):
    cls = f"cl-stat-value {variante}" if variante else "cl-stat-value"
    hint_html = f'<div class="cl-stat-hint">{esc(hint)}</div>' if hint else ""
    st.markdown(
        f'<div class="cl-stat"><div class="{cls}">{esc(valor)}</div>'
        f'<div class="cl-stat-label">{esc(label)}</div>{hint_html}</div>',
        unsafe_allow_html=True,
    )


def badge(texto: str, cor: str = "blue"):
    return f'<span class="cl-badge cl-badge-{cor}">{esc(texto)}</span>'


def flow(steps: list[str], highlight: int = -1):
    parts = []
    for i, s in enumerate(steps):
        hl = ""
        if i == highlight:
            hl = " highlight"
        parts.append(f'<span class="cl-flow-node{hl}">{esc(s)}</span>')
        if i < len(steps) - 1:
            parts.append('<span class="cl-flow-arrow">→</span>')
    st.markdown(f'<div class="cl-flow cl-fade-in">{"".join(parts)}</div>', unsafe_allow_html=True)


def flow_vertical(rows: list[tuple[str, str]], danger_last: bool = False):
    blocks = []
    for i, (titulo, descricao) in enumerate(rows, 1):
        blocks.append(
            f'<div class="cl-flow-v-row"><span class="cl-flow-v-num">{i:02d}</span>'
            f"<div><strong>{esc(titulo)}</strong><span>{esc(descricao)}</span></div></div>"
        )
        if i < len(rows):
            blocks.append('<div class="cl-flow-v-down">↓</div>')
    st.markdown(f'<div class="cl-flow-v">{"".join(blocks)}</div>', unsafe_allow_html=True)


def stepper(items: list[tuple[str, str]], active: int = 1):
    html_parts = []
    for i, (titulo, descricao) in enumerate(items, 1):
        state = "done" if i < active else ("active" if i == active else "")
        label = "✓" if i < active else f"{i:02d}"
        html_parts.append(
            f'<div class="cl-stepper-item {state}"><span class="cl-stepper-num">{label}</span>'
            f'<div class="cl-stepper-body"><strong>{esc(titulo)}</strong>'
            f"<span>{esc(descricao)}</span></div></div>"
        )
    st.markdown(f'<div class="cl-stepper">{"".join(html_parts)}</div>', unsafe_allow_html=True)


def editor_header(filename: str, label: str = ""):
    tag = badge(label, "violet") if label else ""
    st.markdown(
        f'<div class="cl-editor-bar"><span class="file">'
        f'<span class="dots"><span class="dot" style="background:#F87171"></span>'
        f'<span class="dot" style="background:#FBBF24"></span>'
        f'<span class="dot" style="background:#34D399"></span></span>'
        f"<strong>{esc(filename)}</strong></span>{tag}</div>",
        unsafe_allow_html=True,
    )


def code_block(codigo: str, filename: str = "", label: str = "", language: str = "python"):
    if filename:
        editor_header(filename, label)
    st.code(codigo, language=language, line_numbers=True)


def result_panel(titulo: str, valor: str, fatura: str, estado: str = "ok"):
    cor = "green" if estado == "ok" else "red"
    selo = badge("EXECUTADO" if estado == "ok" else "ERRO", cor)
    st.markdown(
        f'<div class="cl-result-panel cl-fade-in">'
        f'<div class="cl-result-head"><span>{esc(titulo)}</span>{selo}</div>'
        f'<div class="cl-result-body"><div class="cl-result-value">{esc(valor)}</div>'
        f'<div class="cl-invoice">{esc(fatura) if fatura else "Sem saída."}</div>'
        f"</div></div>",
        unsafe_allow_html=True,
    )


def console(texto: str):
    st.markdown(f'<div class="cl-console">{esc(texto)}</div>', unsafe_allow_html=True)


def callout(texto: str, variante: str = ""):
    cls = f"cl-callout {variante}" if variante else "cl-callout"
    st.markdown(f'<div class="{cls}">{texto}</div>', unsafe_allow_html=True)


def table(headers: list[str], rows: list[list[str]]):
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows
    )
    st.markdown(
        f'<table class="cl-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>',
        unsafe_allow_html=True,
    )


def attribute_card(sigla: str, titulo: str, descricao: str, foco: str, beneficio: str):
    st.markdown(
        f'<div class="cl-attribute"><div class="cl-attribute-head">'
        f'<span class="cl-attribute-icon">{esc(sigla)}</span><h4>{esc(titulo)}</h4></div>'
        f"<p>{esc(descricao)}</p>"
        f'<div class="cl-attribute-row"><strong>Foco:</strong> {esc(foco)}</div>'
        f'<div class="cl-attribute-row"><strong>Benefício:</strong> {esc(beneficio)}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )


def tool(nome: str, sigla: str, descricao: str):
    st.markdown(
        f'<div class="cl-tool"><span class="cl-tool-badge">{esc(sigla)}</span>'
        f"<div><strong>{esc(nome)}</strong><span>{esc(descricao)}</span></div></div>",
        unsafe_allow_html=True,
    )


def test_row(nome: str, descricao: str, esperado: str, obtido: str, estado: str, duracao: str = ""):
    rotulos = {"passed": "APROVADO", "failed": "FALHADO", "pending": "PENDENTE"}
    rotulo = rotulos.get(estado, estado.upper())
    duracao_html = f"<span><strong>Duração:</strong> {esc(duracao)}</span>" if duracao else ""
    st.markdown(
        f'<div class="cl-test-row {estado}">'
        f'<div><div class="cl-test-name">{esc(nome)}</div>'
        f'<div class="cl-test-desc">{esc(descricao)}</div>'
        f'<div class="cl-test-meta"><span><strong>Esperado:</strong> {esc(esperado)}</span>'
        f"<span><strong>Obtido:</strong> {esc(obtido)}</span>{duracao_html}</div></div>"
        f'<span class="cl-status {estado}">{rotulo}</span></div>',
        unsafe_allow_html=True,
    )


def diff_html(original: str, refatorado: str) -> str:
    orig_lines = original.splitlines(keepends=True)
    ref_lines = refatorado.splitlines(keepends=True)
    diff = difflib.unified_diff(
        orig_lines, ref_lines, fromfile="original", tofile="refatorado", lineterm=""
    )
    rows = []
    ln_o = ln_r = 0
    for line in diff:
        raw = line.rstrip("\n")
        safe = esc(raw)
        if line.startswith("@@"):
            rows.append(
                f'<tr><td class="ln"></td><td class="ln"></td><td class="hunk">{safe}</td></tr>'
            )
            match = re.search(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
            if match:
                ln_o = int(match.group(1)) - 1
                ln_r = int(match.group(2)) - 1
        elif line.startswith("---") or line.startswith("+++"):
            continue
        elif line.startswith("-"):
            ln_o += 1
            rows.append(
                f'<tr class="del"><td class="ln">{ln_o}</td><td class="ln"></td><td>{safe}</td></tr>'
            )
        elif line.startswith("+"):
            ln_r += 1
            rows.append(
                f'<tr class="add"><td class="ln"></td><td class="ln">{ln_r}</td><td>{safe}</td></tr>'
            )
        elif line.startswith(" "):
            ln_o += 1
            ln_r += 1
            rows.append(
                f'<tr class="ctx"><td class="ln">{ln_o}</td><td class="ln">{ln_r}</td>'
                f"<td>{safe}</td></tr>"
            )
    if not rows:
        return '<div class="cl-empty">Sem diferenças entre os dois ficheiros.</div>'
    return f'<div class="cl-diff cl-fade-in"><table>{"".join(rows)}</table></div>'
