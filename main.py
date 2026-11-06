from fasthtml.common import *
from pathlib import Path
import json, subprocess, os

ROOT = Path(__file__).resolve().parent
css = (ROOT / "public" / "styles.css").read_text(encoding="utf-8")

SESSION_SECRET = os.getenv("SESSION_SECRET", "codelab-dev-secret-change-me")
_app, rt = fast_app(secret_key=SESSION_SECRET)
app = _app
application = app

THEME_SCRIPT = """
<script>
(function(){
  const key='codelab-theme';
  function apply(t){ document.documentElement.setAttribute('data-theme',t); }
  const saved=localStorage.getItem(key)||'light';
  apply(saved);
  window.toggleTheme=function(){ const cur=document.documentElement.getAttribute('data-theme'); const n=cur==='dark'?'light':'dark'; localStorage.setItem(key,n); apply(n); };
})();
</script>
"""

@rt("/")
def get():
    from services.processamento import EXEMPLOS, executar_comparacao, formatar_kwanzas
    import implementacoes.pedido_original as po
    import implementacoes.pedido_refatorado as pr

    original_code = (ROOT / "implementacoes" / "pedido_original.py").read_text(encoding="utf-8")
    refatorado_code = (ROOT / "implementacoes" / "pedido_refatorado.py").read_text(encoding="utf-8")

    # run tests summary if exists
    resumo = "Sem resultados. Execute pytest com CODELAB_RESULTS_PATH."
    results_path = ROOT / "test_results.json"
    if results_path.exists():
        data = json.loads(results_path.read_text(encoding="utf-8"))
        resumo = f"{data.get('aprovados',0)}/{data.get('total',0)} testes aprovados"

    return Html(
        Head(
            Title("CODELAB — Qualidade do Código e Refatoração"),
            Meta(charset="utf-8"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Meta(name="language", content="pt-AO"),
            Style(css),
            NotStr(THEME_SCRIPT),
        ),
        Body(
            Div(
                Header(
                    Div("CODELAB", cls="brand"),
                    Nav(
                        A("Demonstração", href="#demo"),
                        A("Comparação", href="#comp"),
                        A("Conceitos", href="#conc"),
                        Button("Tema", onclick="toggleTheme()", cls="theme-btn"),
                    ),
                    cls="topbar",
                ),
                Main(
                    Section(
                        H1("CODELAB"),
                        P("Qualidade do Código e Refatoração", cls="sub"),
                        H2("O mesmo resultado. Um código melhor organizado."),
                        P("Compara duas implementações do mesmo programa e observa como a refatoração melhora a sua estrutura sem alterar o comportamento."),
                        Div("CÓDIGO ORIGINAL → REFATORAÇÃO → CÓDIGO MELHOR ORGANIZADO", cls="flow"),
                        id="hero",
                    ),
                    Section(
                        H2("Demonstração"),
                        Form(
                            Select(
                                Option("COMUM", value="COMUM"),
                                Option("VIP", value="VIP", selected=True),
                                Option("PREMIUM", value="PREMIUM"),
                                name="tipo",
                            ),
                            Button("COMPARAR AS DUAS VERSÕES", type="submit", cls="primary"),
                            method="post", action="/comparar", id="demo",
                        ),
                        id="demo",
                    ),
                    Section(
                        H2("O que mudou no código?"),
                        Div(
                            Pre(Code(original_code), cls="code"),
                            Pre(Code(refatorado_code), cls="code"),
                            cls="codecols",
                        ),
                        P("Antes, uma única função executava várias responsabilidades. Depois, cada operação passou a ter uma função própria."),
                        id="comp",
                    ),
                    Section(
                        H2("Conceitos"),
                        Ul(Li("Legibilidade"), Li("Manutenibilidade"), Li("Reutilização"), Li("Eficiência"), Li("Confiabilidade")),
                        P("Refatoração: melhorar a estrutura interna do código sem alterar o comportamento externo."),
                        P("Técnica: Extrair Método."),
                        id="conc",
                    ),
                    Section(
                        H2("Testes automatizados"),
                        P(resumo),
                    ),
                ),
                cls="app",
            )
        )
    )

@rt("/comparar", methods=["POST"])
def post(tipo: str):
    from services.processamento import EXEMPLOS, executar_comparacao, formatar_kwanzas
    pedido = EXEMPLOS.get(tipo, EXEMPLOS["VIP"])
    r = executar_comparacao(pedido)
    cor = "green" if r["preservado"] else "red"
    msg = "COMPORTAMENTO PRESERVADO" if r["preservado"] else "DIFERENÇA DETECTADA"
    return Html(
        Head(Title("Resultado"), Style(css)),
        Body(
            Main(
                H2("Resultado"),
                Div(
                    Div(H3("ANTES — Código Original"), P(formatar_kwanzas(r["valor_original"])), Pre(r["fatura_original"])),
                    Div(H3("DEPOIS — Código Refatorado"), P(formatar_kwanzas(r["valor_refatorado"])), Pre(r["fatura_refatorada"])),
                    cls="resultcols",
                ),
                P(msg, cls=cor),
                A("Voltar", href="/"),
            )
        )
    )

if __name__ == "__main__":
    serve()
