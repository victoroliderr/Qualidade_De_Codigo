# CODELAB — Qualidade do Código e Refatoração

Laboratório académico em **Python + FastHTML** que compara duas implementações do
mesmo programa: o processamento de encomendas de uma loja virtual. As duas versões
são executadas com os mesmos dados e os resultados são apresentados lado a lado.

O objectivo é demonstrar, com execução real, que a refatoração melhora a organização
interna do código sem alterar o comportamento externo.

- Página única, com navegação curta: **Demonstração**, **Comparação** e **Conceitos**.
- Tema claro e tema escuro, com a escolha guardada no navegador.
- Interface integralmente em **português de Angola** (`lang="pt-AO"`).
- Valores exclusivamente em **Kwanza angolano (Kz)**.
- Resultados, facturas e testes reais. Não existem valores simulados.

## Como funciona a demonstração

O utilizador escolhe um tipo de cliente — **COMUM**, **VIP** ou **PREMIUM** — e
carrega em **COMPARAR AS DUAS VERSÕES**. A aplicação:

1. executa `implementacoes/pedido_original.py`;
2. executa `implementacoes/pedido_refatorado.py`;
3. usa exactamente os mesmos dados nas duas versões;
4. compara os valores devolvidos e as facturas emitidas;
5. apresenta os painéis **ANTES — Código Original** e **DEPOIS — Código Refatorado**.

Quando o valor e a factura coincidem, a interface confirma
**COMPORTAMENTO PRESERVADO**.

| Cliente | Desconto | Exemplo   | Total          |
| ------- | -------: | --------- | -------------- |
| COMUM   |       0% | 100.000 Kz | 100.000,00 Kz |
| VIP     |      10% | 100.000 Kz | 90.000,00 Kz  |
| PREMIUM |      15% | 200.000 Kz | 170.000,00 Kz |

Os valores são ilustrativos e não representam preços de mercado.

## Tecnologias

- Python 3.12
- FastHTML (ASGI, componentes em Python)
- HTMX para a actualização do painel de resultados
- Pygments para o realce de sintaxe Python
- pytest para os testes
- CSS próprio, sem frameworks de interface

Não existem React, Next.js, Vue ou TypeScript no projecto.

## Estrutura

```text
codelab/
├── main.py                     # aplicação ASGI e rotas
├── implementacoes/
│   ├── pedido_original.py      # uma função com várias responsabilidades
│   └── pedido_refatorado.py    # quatro funções especializadas
├── services/
│   ├── moeda.py                # formatar_kwanzas()
│   └── processamento.py        # execução, exemplos e relatório de testes
├── components/
│   ├── layout.py               # estrutura da página, cabeçalho e temas
│   ├── demonstracao.py         # selector de cliente e painel de resultados
│   ├── comparacao.py           # comparação dos ficheiros reais
│   ├── validacao.py            # resumo da última execução do pytest
│   ├── conceitos.py            # atributos de qualidade e técnica aplicada
│   └── base.py                 # cabeçalho comum das secções
├── tests/
│   ├── test_processamento_pedidos.py
│   ├── test_interface.py
│   └── conftest.py             # exporta os resultados reais do pytest
├── data/
│   └── resultados_testes.json  # último relatório real, lido pela interface
├── public/
│   ├── styles.css
│   └── htmx.min.js
├── requirements.txt
├── .python-version
├── vercel.json
├── .env.example
└── README.md
```

## Instalação local

Na pasta do projecto:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

No Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Executar a aplicação

```bash
uvicorn main:app --reload
```

Abrir `http://127.0.0.1:8000`. A página inicial já apresenta o exemplo VIP, por isso
a demonstração está visível sem qualquer clique.

## Executar os testes

```bash
pytest -q
```

Para actualizar o resumo apresentado na interface com uma execução real:

```bash
CODELAB_RESULTS_PATH=data/resultados_testes.json pytest -q
```

O ficheiro `data/resultados_testes.json` é lido pela aplicação. O servidor **não
executa pytest**: em produção, o resumo corresponde à última execução feita no
terminal ou na CI. Depois de actualizar o relatório, confirma o ficheiro no Git
para que a versão publicada apresente os novos resultados.

Os testes cobrem:

- cliente COMUM, sem desconto;
- cliente VIP, com 10% de desconto;
- cliente PREMIUM, com 15% de desconto;
- encomendas com vários produtos e quantidades;
- igualdade de valor e de factura entre as duas implementações;
- formatação monetária em Kwanzas;
- rotas, ficheiros estáticos, temas e localização.

## Publicação no Vercel

O projecto está preparado para o runtime Python do Vercel e para o modelo ASGI.

1. Confirmar que `main.py` expõe a variável `app` no nível superior do módulo.
2. Confirmar que o repositório contém `requirements.txt` com versões fixadas,
   `.python-version` com `3.12` e `vercel.json` com a configuração mínima.
3. Enviar o projecto para um repositório no GitHub.
4. No Vercel, escolher **Add New → Project** e importar o repositório.
5. Em **Settings → Environment Variables**, criar `SESSKEY` com uma chave estável
   e secreta. Nunca colocar essa chave no Git. Sem esta variável, a aplicação
   recusa arrancar no Vercel.
6. Publicar. O Vercel detecta `main.py` como ponto de entrada ASGI.

O valor de `SESSKEY` tem de ser o mesmo em todos os arranques. A aplicação não
escreve em ficheiros persistentes nem usa SQLite local em produção.

Para validar localmente antes de publicar, pode usar a CLI do Vercel:

```bash
npm install -g vercel
vercel dev
```

Confirmar, na instância local:

- a página inicial abre;
- os dois temas alternam e a escolha permanece após actualizar;
- a navegação por âncoras funciona;
- a comparação devolve os valores correctos;
- as facturas estão em Kz;
- os painéis de código mostram os ficheiros reais;
- `/styles.css` e `/htmx.min.js` são servidos;
- não existem erros nas rotas.

> Este repositório está preparado para publicação, mas nenhuma publicação de
> produção é afirmada neste documento. A publicação só existe depois de ser feita
> efectivamente no painel do Vercel.

## Roteiro de demonstração (3 a 5 minutos)

1. **Introdução** — mostrar a página inicial e explicar que serão comparadas duas
   implementações do mesmo programa.
2. **Demonstração** — seleccionar o cliente **VIP** e carregar em
   **COMPARAR AS DUAS VERSÕES**.
3. **Resultado** — mostrar que as duas implementações produzem
   **90.000,00 Kz** e que a interface confirma **COMPORTAMENTO PRESERVADO**.
4. **Código** — descer até **O QUE MUDOU NO CÓDIGO?** e explicar que a função
   original acumulava cálculo, desconto e factura, enquanto a versão refatorada
   separou:
   - `calcular_valor_base()`
   - `aplicar_desconto_cliente()`
   - `emitir_fatura_impressa()`
   - `processar_pedido()`
5. **Validação** — apresentar o resumo real dos testes automatizados.
6. **Conclusão** — a refatoração melhorou a legibilidade, a manutenibilidade e a
   reutilização sem alterar o comportamento esperado.

## Regras de localização e moeda

- Idioma do documento: `pt-AO`.
- Terminologia preferida: **utilizador**, **ecrã**, **registo**, **ficheiro**,
  **telemóvel**, **partilhar ficheiro**, **entrega**, **encomenda**.
- Moeda única: **Kz (Kwanza angolano)**.
- Formatação central em `services/moeda.py`:

```python
formatar_kwanzas(valor)  # 100000.0 -> "100.000,00 Kz"
```


## Licença e contexto

Projecto académico de Engenharia de Software, na área de Qualidade do Código e
Refatoração. O documento escrito do grupo (`qualidade_de_codigo.docx`) complementa
esta demonstração prática.
