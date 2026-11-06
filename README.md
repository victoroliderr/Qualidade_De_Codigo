# CODELAB — Qualidade do Código e Refatoração

Laboratório interactivo em **Python + Streamlit** que demonstra, com execução real, a
refatoração do processamento de pedidos de uma loja virtual. A aplicação compara a
implementação original com uma versão refatorada, mostra os dois códigos reais, calcula
o diff, executa as duas versões com os mesmos dados e corre uma suíte de testes com
**pytest**.

O cenário principal é o processamento de pedidos (clientes **COMUM**, **VIP** e
**PREMIUM**).

## Tecnologias

- Python 3.10+
- Streamlit
- pytest
- HTML/CSS para a camada visual

## Instalação

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
streamlit run app.py
```

O Streamlit abre a aplicação no navegador. Se não abrir automaticamente, acede a
`http://localhost:8501`.

## Executar os testes

```bash
python -m pytest tests/test_processamento_pedidos.py -v
```

A página **Testes Automatizados** também executa o pytest num subprocesso real e
apresenta o estado, a duração, o esperado, o obtido e a consola de execução. Para isso,
o pytest tem de estar instalado no mesmo ambiente Python que corre o Streamlit.

## Estrutura

```text
.
├── app.py
├── pages/
│   ├── 01_Visao_Geral.py
│   ├── 02_Laboratorio.py
│   ├── 03_Comparacao.py
│   ├── 04_Testes.py
│   ├── 05_Qualidade.py
│   ├── 06_Code_Smells.py
│   ├── 07_Refatoracao.py
│   ├── 08_Ferramentas.py
│   └── 09_Referencias.py
├── implementacoes/
│   ├── pedido_original.py
│   └── pedido_refatorado.py
├── tests/
│   ├── conftest.py
│   └── test_processamento_pedidos.py
├── components/
│   └── componentes_visuais.py
├── assets/
│   └── estilos.css
├── requirements.txt
└── README.md
```

A interface não contém uma segunda implementação escondida: a página do laboratório
importa `implementacoes/pedido_original.py` e `implementacoes/pedido_refatorado.py`.
As faturas são capturadas com `io.StringIO` e `contextlib.redirect_stdout`, e cada
versão recebe uma cópia profunda e independente do pedido.

## Regras do exemplo

| Tipo de cliente | Desconto |
|---|---:|
| COMUM | 0% |
| VIP | 10% |
| PREMIUM | 15% |

Casos oficiais do relatório:

| Exemplo | Pedido | Resultado |
|---|---|---:|
| João Silva (COMUM) | 50,00 × 2 | R$ 100,00 |
| Maria Santos (VIP) | 100,00 × 1 | R$ 90,00 |
| Empresa XYZ (PREMIUM) | 200,00 × 1 | R$ 170,00 |

## Roteiro de demonstração para a defesa

1. **Apresentação** — abrir a **Visão Geral** e explicar o propósito do laboratório:
   melhorar a estrutura interna sem alterar o comportamento externo.
2. **Cenário original** — abrir **Comparação de Código**, painel *Before*, e mostrar que
   `processar_pedido` concentra cálculo, desconto e fatura.
3. **Executar o pedido** — abrir **Laboratório Prático**, escolher o exemplo **VIP**
   (`Maria Santos`) e clicar em **EXECUTAR COMPARAÇÃO**.
4. **Mostrar o resultado** — confirmar que as duas versões produzem a mesma fatura e
   R$ 90,00; destacar a mensagem **COMPORTAMENTO PRESERVADO**.
5. **Comparar o código** — voltar a **Comparação de Código** e alternar entre
   *Lado a lado*, *Original*, *Refatorado* e *Diferenças*.
6. **Explicar as técnicas** — identificar **Extrair Método** nas quatro funções e
   explicar o dicionário `taxas_desconto` como organização extensível das regras.
7. **Executar os testes** — abrir **Testes Automatizados**, clicar em
   **EXECUTAR TESTES AUTOMATIZADOS** e percorrer os seis resultados e a consola.
8. **Concluir** — relacionar as alterações com legibilidade, manutenibilidade,
   reutilização, eficiência e confiabilidade; referir que não são inventadas métricas.

## Notas de rigor

- As páginas **Ferramentas e Métricas** e **Qualidade do Código** explicam métricas
  (complexidade ciclomática, cobertura e acoplamento) sem apresentar valores que não
  foram medidos.
- A análise estática não é executada pela aplicação; Pylint, SonarQube e ESLint são
  apresentados com as respectivas linguagens e limitações.
- Os resultados dos testes apresentados na interface vêm de um relatório JSON gerado
  pelo pytest durante a execução, não de valores estáticos.
