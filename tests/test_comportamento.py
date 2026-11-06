import io
import unittest
from contextlib import redirect_stdout

from implementacoes import (
    exemplo_original,
    exemplo_refatorado,
    extensao_original,
    extensao_refatorada,
)


def capturar_saida(funcao, usuario):
    saida = io.StringIO()
    with redirect_stdout(saida):
        funcao(usuario)
    return saida.getvalue()


class TestComportamentoRefatoracao(unittest.TestCase):
    def verificar_saida(self, funcao, usuario, esperado, descricao):
        obtido = capturar_saida(funcao, usuario)
        self.resultado_esperado = esperado or "Nenhuma notificação foi emitida."
        self.resultado_obtido = obtido or "Nenhuma notificação foi emitida."
        self.descricao = descricao
        self.assertEqual(obtido, esperado)

    def verificar_equivalencia(self, original, refatorada, usuario, descricao):
        saida_original = capturar_saida(original, usuario)
        saida_refatorada = capturar_saida(refatorada, usuario)
        self.resultado_esperado = "As duas versões devem produzir a mesma saída."
        self.resultado_obtido = (
            "Saídas iguais: " + (saida_original.strip() or "nenhuma notificação")
            if saida_original == saida_refatorada
            else "Saídas diferentes."
        )
        self.descricao = descricao
        self.assertEqual(saida_original, saida_refatorada)

    def test_administrador_processado_na_versao_original(self):
        self.verificar_saida(
            exemplo_original.processar_usuario,
            {"nome": "Ana", "admin": True},
            "Notificando admin: Ana\n",
            "Administrador no exemplo principal — versão original",
        )

    def test_administrador_processado_na_versao_refatorada(self):
        self.verificar_saida(
            exemplo_refatorado.processar_usuario,
            {"nome": "Ana", "admin": True},
            "Notificando admin: Ana\n",
            "Administrador no exemplo principal — versão refatorada",
        )

    def test_utilizador_comum_no_exemplo_original(self):
        self.verificar_saida(
            exemplo_original.processar_usuario,
            {"nome": "João", "admin": False},
            "",
            "Utilizador comum no exemplo principal — versão original",
        )

    def test_utilizador_comum_no_exemplo_refatorado(self):
        self.verificar_saida(
            exemplo_refatorado.processar_usuario,
            {"nome": "João", "admin": False},
            "",
            "Utilizador comum no exemplo principal — versão refatorada",
        )

    def test_administrador_processa_relatorio_original(self):
        self.verificar_saida(
            extensao_original.processar_relatorio,
            {"nome": "Ana", "admin": True},
            "Notificando admin: Ana\n",
            "Administrador ao processar relatório — versão original",
        )

    def test_administrador_processa_relatorio_refatorado(self):
        self.verificar_saida(
            extensao_refatorada.processar_relatorio,
            {"nome": "Ana", "admin": True},
            "Notificando admin: Ana\n",
            "Administrador ao processar relatório — versão refatorada",
        )

    def test_utilizador_comum_processa_relatorio_original(self):
        self.verificar_saida(
            extensao_original.processar_relatorio,
            {"nome": "João", "admin": False},
            "",
            "Utilizador comum ao processar relatório — versão original",
        )

    def test_utilizador_comum_processa_relatorio_refatorado(self):
        self.verificar_saida(
            extensao_refatorada.processar_relatorio,
            {"nome": "João", "admin": False},
            "",
            "Utilizador comum ao processar relatório — versão refatorada",
        )

    def test_saidas_iguais_para_administrador_no_exemplo_principal(self):
        self.verificar_equivalencia(
            exemplo_original.processar_usuario,
            exemplo_refatorado.processar_usuario,
            {"nome": "Ana", "admin": True},
            "Equivalência para administrador no exemplo principal",
        )

    def test_saidas_iguais_para_utilizador_comum_no_exemplo_principal(self):
        self.verificar_equivalencia(
            exemplo_original.processar_usuario,
            exemplo_refatorado.processar_usuario,
            {"nome": "João", "admin": False},
            "Equivalência para utilizador comum no exemplo principal",
        )

    def test_saidas_iguais_para_administrador_no_relatorio(self):
        self.verificar_equivalencia(
            extensao_original.processar_relatorio,
            extensao_refatorada.processar_relatorio,
            {"nome": "Ana", "admin": True},
            "Equivalência para administrador na extensão de relatório",
        )

    def test_saidas_iguais_para_utilizador_comum_no_relatorio(self):
        self.verificar_equivalencia(
            extensao_original.processar_relatorio,
            extensao_refatorada.processar_relatorio,
            {"nome": "João", "admin": False},
            "Equivalência para utilizador comum na extensão de relatório",
        )
