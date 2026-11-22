"""Estrutura da página única do CODELAB."""
from __future__ import annotations

from fasthtml.common import (
    A,
    Body,
    Button,
    Div,
    Footer,
    H1,
    Head,
    Header,
    Html,
    Link,
    Main,
    Meta,
    Nav,
    NotStr,
    P,
    Script,
    Section,
    Span,
    Title,
)

from components.comparacao import seccao_comparacao
from components.conceitos import seccao_conceitos
from components.demonstracao import seccao_demonstracao
from components.validacao import seccao_validacao
from services.processamento import (
    TIPO_PREDEFINIDO,
    executar_comparacao,
    exemplo_por_tipo,
    ler_resultados_testes,
)

SCRIPT_TEMA = """
<script>
(function () {
  var chave = 'codelab-tema';
  var guardado = null;
  try { guardado = localStorage.getItem(chave); } catch (erro) {}
  var tema = guardado === 'dark' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', tema);

  function sincronizar() {
    var botao = document.getElementById('alternar-tema');
    var meta = document.getElementById('meta-tema');
    if (!botao) return;
    var escuro = document.documentElement.getAttribute('data-theme') === 'dark';
    botao.setAttribute('aria-pressed', escuro ? 'true' : 'false');
    botao.setAttribute(
      'aria-label',
      escuro ? 'Mudar para tema claro' : 'Mudar para tema escuro'
    );
    botao.setAttribute(
      'title',
      escuro ? 'Mudar para tema claro' : 'Mudar para tema escuro'
    );
    if (meta) meta.setAttribute('content', escuro ? '#121110' : '#F7F5EF');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var botao = document.getElementById('alternar-tema');
    if (!botao) return;
    botao.addEventListener('click', function () {
      var actual = document.documentElement.getAttribute('data-theme');
      var novo = actual === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', novo);
      try { localStorage.setItem(chave, novo); } catch (erro) {}
      sincronizar();
    });
    sincronizar();
  });
})();
</script>
"""

SCRIPT_MENU = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  var botao = document.getElementById('menu-mobile');
  var cabecalho = document.querySelector('.site-header');
  var navegacao = document.getElementById('menu-navegacao');
  if (!botao || !cabecalho || !navegacao) return;

  function definirEtiqueta(texto) {
    botao.setAttribute('aria-label', texto);
    var textoOculto = botao.querySelector('.visually-hidden');
    if (textoOculto) textoOculto.textContent = texto;
  }

  function fechar(devolverFoco) {
    cabecalho.removeAttribute('data-menu');
    botao.setAttribute('aria-expanded', 'false');
    definirEtiqueta('Abrir menu de navegação');
    if (devolverFoco) botao.focus();
  }

  botao.addEventListener('click', function () {
    if (botao.getAttribute('aria-expanded') === 'true') {
      fechar(false);
      return;
    }
    cabecalho.setAttribute('data-menu', 'aberto');
    botao.setAttribute('aria-expanded', 'true');
    definirEtiqueta('Fechar menu de navegação');
    var primeiroLink = navegacao.querySelector('a');
    if (primeiroLink) primeiroLink.focus();
  });

  navegacao.addEventListener('click', function (evento) {
    if (evento.target.closest('a')) fechar(false);
  });

  document.addEventListener('keydown', function (evento) {
    if (evento.key === 'Escape' && botao.getAttribute('aria-expanded') === 'true') {
      fechar(true);
    }
  });

  document.addEventListener('click', function (evento) {
    if (botao.getAttribute('aria-expanded') !== 'true') return;
    if (!cabecalho.contains(evento.target)) fechar(false);
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 760) fechar(false);
  });
});
</script>
"""

ICONE_SOL = (
    '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" '
    'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
    'aria-hidden="true"><circle cx="12" cy="12" r="4"></circle>'
    '<path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41'
    'M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"></path></svg>'
)

ICONE_LUA = (
    '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" '
    'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M20.5 14.5A8.5 8.5 0 0 1 9.5 3.5a8.5 8.5 0 1 0 11 11Z"></path></svg>'
)

ICONE_MENU = (
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" '
    'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
    'aria-hidden="true">'
    '<path class="barra barra-topo" d="M4 7h16"></path>'
    '<path class="barra barra-meio" d="M4 12h16"></path>'
    '<path class="barra barra-base" d="M4 17h16"></path></svg>'
)

MEMBROS_GRUPO = "Victor Pedro · Manuel Mendes · Luís Pedro · Miguel Bengui"


def cabecalho() -> Header:
    return Header(
        Div(
            Div(
                A("CODELAB", href="/", cls="brand-name"),
                Span("Qualidade do Código e Refatoração", cls="brand-desc"),
                cls="brand",
            ),
            Nav(
                A("Demonstração", href="/#demonstracao"),
                A("Comparação", href="/#comparacao"),
                A("Conceitos", href="/#conceitos"),
                id="menu-navegacao",
                cls="nav",
                **{"aria-label": "Navegação principal"},
            ),
            Button(
                Span(NotStr(ICONE_MENU), cls="icon-menu"),
                Span("Abrir menu", cls="visually-hidden"),
                id="menu-mobile",
                cls="menu-toggle",
                type="button",
                **{
                    "aria-controls": "menu-navegacao",
                    "aria-expanded": "false",
                    "aria-label": "Abrir menu de navegação",
                },
            ),
            Button(
                Span(NotStr(ICONE_LUA), cls="icon icon-lua"),
                Span(NotStr(ICONE_SOL), cls="icon icon-sol"),
                Span("Alternar tema", cls="visually-hidden"),
                id="alternar-tema",
                cls="theme-toggle",
                type="button",
                **{"aria-label": "Mudar para tema escuro", "aria-pressed": "false"},
            ),
            cls="header-inner wrap",
        ),
        cls="site-header",
    )


def hero() -> Section:
    passos = (
        (
            "01",
            "Código original",
            "Uma função acumula cálculo, desconto e factura.",
        ),
        (
            "02",
            "Refatoração",
            "Extrair Método separa cada responsabilidade.",
        ),
        (
            "03",
            "Código melhor organizado",
            "Quatro funções com nomes claros e um só coordenador.",
        ),
    )

    fluxo = []
    for indice, (numero, titulo, texto) in enumerate(passos):
        fluxo.append(
            Div(
                Span(numero, cls="flow-num"),
                Div(
                    Span(titulo, cls="flow-title"),
                    Span(texto, cls="flow-note"),
                ),
                cls="flow-step",
            )
        )
        if indice < len(passos) - 1:
            fluxo.append(Div("→", cls="flow-arrow", **{"aria-hidden": "true"}))

    return Section(
        P(
            Span(MEMBROS_GRUPO, cls="eyebrow-strong"),
            cls="eyebrow",
        ),
        H1(
            "O mesmo resultado. ",
            Span("Um código melhor organizado.", cls="h1-muted"),
        ),
        P(
            "Compara duas implementações do mesmo programa e observa como a "
            "refatoração melhora a sua estrutura sem alterar o comportamento.",
            cls="hero-desc",
        ),
        Div(
            *fluxo,
            cls="flow-band",
            **{"aria-label": "Percorrer o processo de refatoração"},
        ),
        cls="hero",
        id="inicio",
    )


def rodape() -> Footer:
    return Footer(
        Div(
            Div(
                Span("CODELAB", cls="footer-brand"),
                Span("Qualidade do Código e Refatoração", cls="footer-desc"),
            ),
            Div(
                Span(
                    "Victor Pedro · Manuel Mendes · Luís Pedro · Miguel Bengui",
                    cls="footer-meta",
                ),
            ),
            cls="footer-inner wrap",
        ),
        cls="site-footer",
    )


def pagina(tipo_selecionado: str = TIPO_PREDEFINIDO, resultado: dict | None = None):
    """Constrói a página principal completa."""
    tipo = (tipo_selecionado or TIPO_PREDEFINIDO).upper()
    if resultado is None:
        resultado = executar_comparacao(exemplo_por_tipo(tipo))

    dados_testes = ler_resultados_testes()

    return Html(
        Head(
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(
                name="description",
                content=(
                    "Trabalho académico que compara duas implementações do "
                    "mesmo programa e demonstra a refatoração sem alterar o "
                    "comportamento."
                ),
            ),
            Meta(name="color-scheme", content="light dark"),
            Meta(id="meta-tema", name="theme-color", content="#F7F5EF"),
            Meta(property="og:title", content="CODELAB — Qualidade do Código e Refatoração"),
            Meta(
                property="og:description",
                content="O mesmo resultado. Um código melhor organizado.",
            ),
            Meta(property="og:type", content="website"),
            Title("CODELAB — Qualidade do Código e Refatoração"),
            Link(rel="icon", href="/favicon.ico", sizes="any"),
            Link(rel="icon", type="image/svg+xml", href="/favicon.svg"),
            Link(rel="preconnect", href="https://fonts.googleapis.com"),
            Link(
                rel="preconnect",
                href="https://fonts.gstatic.com",
                crossorigin="",
            ),
            Link(
                rel="stylesheet",
                href=(
                    "https://fonts.googleapis.com/css2?"
                    "family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600"
                    "&family=IBM+Plex+Mono:wght@400;500;600"
                    "&family=Manrope:wght@500;600;700;800&display=swap"
                ),
            ),
            Link(rel="stylesheet", href="/styles.css"),
            Script(src="/htmx.min.js", defer=True),
            NotStr(SCRIPT_TEMA),
            NotStr(SCRIPT_MENU),
        ),
        Body(
            A("Saltar para o conteúdo", href="#conteudo", cls="skip-link"),
            cabecalho(),
            Main(
                hero(),
                seccao_demonstracao(tipo, resultado),
                seccao_comparacao(),
                seccao_validacao(dados_testes),
                seccao_conceitos(),
                id="conteudo",
                cls="wrap",
            ),
            rodape(),
        ),
        lang="pt-AO",
    )
