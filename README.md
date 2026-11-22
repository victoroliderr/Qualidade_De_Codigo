# CODELAB — Qualidade do Código e Refatoração

Trabalho académico em **Python + FastHTML** que compara duas implementações do
mesmo programa: o processamento de encomendas de uma loja virtual. As duas versões
são executadas com os mesmos dados e os resultados são apresentados lado a lado.

O objectivo é demonstrar, com execução real, que a refatoração melhora a organização
interna do código sem alterar o comportamento externo.

- Página única, com navegação curta: **Demonstração**, **Comparação** e **Conceitos**.
- Menu de navegação que se abre e fecha em telemóveis, com gestos de toque e teclado.
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
│   ├── htmx.min.js
│   ├── favicon.ico
│   └── favicon.svg
├── requirements.txt
├── .python-version
├── render.yaml                # blueprint do Render (Web Service ASGI)
├── vercel.json                # configuração legada, para quem usar Vercel
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

## Publicação no Render

O projecto está preparado para o runtime Python do Render e para o modelo ASGI.
O ficheiro `render.yaml` descreve um **Web Service** com:

- runtime Python e versão `3.12` (lida de `.python-version`);
- build: `pip install -r requirements.txt`;
- arranque: `uvicorn main:app --host 0.0.0.0 --port $PORT`, ou seja, ligação em
  `0.0.0.0` e porta injectada pelo Render;
- verificação de saúde em `/`;
- `SESSKEY` gerada automaticamente pelo Render (`generateValue: true`) e
  reutilizada em todos os arranques;
- `PYTHONUNBUFFERED=1` para os logs surgirem sem espera.

### Publicar com o blueprint (recomendado)

1. Confirmar que `main.py` expõe a variável `app` no nível superior do módulo.
2. Enviar o projecto para um repositório no GitHub, GitLab ou Bitbucket.
3. No Render, escolher **New → Blueprint** e ligar o repositório.
4. Dar um nome ao projecto e carregar em **Apply**. O Render lê `render.yaml`,
   instala as dependências e publica o serviço.
5. Cada push para o ramo ligado gera uma nova publicação automática.

### Publicar manualmente sem blueprint

Se preferir criar o serviço pelo painel:

1. **New → Web Service** e ligar o repositório.
2. Language: **Python 3**; Build Command: `pip install -r requirements.txt`.
3. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
4. Em **Environment**, adicionar `SESSKEY` com um valor longo e secreto
   (botão **Generate** do painel). Não existe fallback inseguro: com `RENDER=true`,
   a aplicação recusa arrancar se `SESSKEY` estiver ausente.
5. Opcionalmente definir a região (o blueprint usa `frankfurt`) e o plano.

O valor de `SESSKEY` tem de ser o mesmo em todos os arranques, caso contrário
os cookies assinados deixam de ser válidos. Nunca o coloques no Git. A aplicação
não escreve em ficheiros persistentes nem usa SQLite: o resumo apresentado é o
que está confirmado em `data/resultados_testes.json`.

O plano `free` suspende o serviço após 15 minutos sem tráfego. O primeiro pedido
seguinte demora mais a responder; para manter o serviço sempre activo, escolher
um plano pago no painel ou alterar `plan` no `render.yaml`.

### Validar antes de publicar

Podes reproduzir localmente o comando que o Render executa:

```bash
pip install -r requirements.txt
PORT=8000 uvicorn main:app --host 0.0.0.0 --port $PORT
```

Confirmar, na instância local:

- a página inicial abre em `/` e essa rota responde com estado 200;
- os dois temas alternam e a escolha permanece após actualizar;
- a navegação por âncoras funciona;
- a comparação devolve os valores correctos;
- as facturas estão em Kz;
- os painéis de código mostram os ficheiros reais;
- `/styles.css` e `/htmx.min.js` são servidos;
- não existem erros nas rotas.

> Este repositório está preparado para publicação, mas nenhuma publicação de
> produção é afirmada neste documento. A publicação só existe depois de ser feita
> efectivamente no painel do Render.

### Alternativa: Vercel

Os ficheiros `vercel.json` e `.vercelignore` mantêm-se para quem ainda publicar
no Vercel. Nesse caso, definir `SESSKEY` nas variáveis de ambiente do Vercel;
também aí a aplicação recusa arrancar sem a chave.

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
