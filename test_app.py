import json
from pathlib import Path
import subprocess
import sys
import unittest

from app import run

ROOT = Path(__file__).resolve().parent


class ProjetoTest(unittest.TestCase):
    def test_exemplo_documentado(self):
        data = json.loads((ROOT / "exemplo.json").read_text(encoding="utf-8"))
        result = run(data)
        self.assertEqual(result['menos_barreiras_registradas'], 'Trecho B')

    def test_cli_com_exemplo(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "app.py"), str(ROOT / "exemplo.json")],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        self.assertEqual(json.loads(result.stdout)['menos_barreiras_registradas'], 'Trecho B')

    def test_rejeita_dados_incompletos(self):
        with self.assertRaises((KeyError, ValueError, TypeError)):
            run({})

    def test_impeditiva_tem_prioridade_sobre_contagem(self):
        bar = dict(local="Natal", tipo="Degrau", impeditiva=False)
        result = run(dict(origem="A", destino="B", percursos=[dict(nome="A", paradas=[], barreiras=[dict(bar, impeditiva=True)]), dict(nome="B", paradas=[], barreiras=[bar, bar, bar])]))
        self.assertEqual(result["menos_barreiras_registradas"], "B")

    def test_rejeita_booleano_textual(self):
        with self.assertRaises(ValueError):
            run(dict(origem="A", destino="B", percursos=[dict(nome="A", paradas=[], barreiras=[dict(local="Natal", tipo="Degrau", impeditiva="false")])]))
