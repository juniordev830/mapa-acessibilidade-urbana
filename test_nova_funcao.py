import unittest
from app import run
class ResumoBarreiras(unittest.TestCase):
    def test_resumo(self):
        data={"origem":"A","destino":"B","diagnostico":True,"percursos":[{"nome":"A","paradas":[],"barreiras":[{"local":"Rua A","tipo":"Degrau","impeditiva":True},{"local":"Rua B","tipo":"degrau","impeditiva":False}]},{"nome":"B","paradas":[],"barreiras":[]}]}
        result=run(data)
        self.assertEqual(result["barreiras_por_tipo"]["degrau"],{"total":2,"impeditivas":1})
        self.assertEqual(result["percursos_sem_impeditivas_registradas"],["B"])
