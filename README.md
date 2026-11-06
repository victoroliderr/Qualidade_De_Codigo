# Laboratório de Qualidade do Código

Aplicação local em Python e Streamlit para demonstrar refatoração sem alteração
do comportamento. O exemplo principal aplica **Extrair Método** à notificação
de administradores. Uma extensão separada demonstra reutilização e remoção de
duplicação ao processar utilizadores e relatórios.

## Requisitos

- Python 3.10 ou superior
- pip

## Instalação e execução

Na pasta do projecto, crie e active um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows PowerShell, active-o com:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Instale a dependência e inicie a aplicação:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abre a aplicação no navegador. Se não abrir automaticamente,
acesse `http://localhost:8501`.

## Testes automatizados

Execute a suite com a biblioteca padrão `unittest`:

```bash
python -m unittest discover -s tests -v
```

Na aplicação, a área **Testes** também executa a mesma suite e apresenta o
estado, a saída esperada e a saída realmente obtida em cada caso.

## Utilização

Na área **Simulador**, seleccione Ana (administradora) ou João (utilizador
comum), escolha processar utilizador ou relatório e clique em **Executar
comparação**. O mesmo dicionário de dados é passado às implementações original
e refatorada; as saídas são recolhidas com `StringIO` e `redirect_stdout`.
As áreas **Comparação do código**, **Testes**, **Qualidade** e **Conceitos**
explicam e exibem os módulos reais executados.

## Estrutura do projecto

```text
.
├── app.py
├── implementacoes/
│   ├── exemplo_original.py
│   ├── exemplo_refatorado.py
│   ├── extensao_original.py
│   └── extensao_refatorada.py
├── tests/
│   └── test_comportamento.py
├── requirements.txt
└── README.md
```

## Roteiro de Demonstração

1. Apresente o laboratório e o objectivo de preservar o comportamento.
2. No **Simulador**, seleccione Ana, que é administradora.
3. Escolha **Processar utilizador** e execute a comparação.
4. Mostre que ambas as versões produzem a mesma notificação.
5. Seleccione João, utilizador comum, e execute novamente para mostrar que
   nenhuma versão emite uma notificação.
6. Abra **Comparação do código** e mostre os dois módulos do exemplo principal.
7. Explique **Extrair Método**: `notificar_admin` concentra a ação, enquanto
   `processar_usuario` mantém a decisão.
8. No simulador, escolha **Processar relatório** e execute a comparação. Depois,
   em **Comparação do código**, abra o separador **Extensão · Reutilização** e
   mostre como a versão refatorada reutiliza a função e elimina duplicação.
   Esta extensão é um exemplo adicional, separado do código do trabalho.
9. Execute os testes automatizados e percorra os resultados apresentados.
10. Termine explicando legibilidade, manutenibilidade, reutilização,
    eficiência e confiabilidade sem atribuir métricas artificiais.
