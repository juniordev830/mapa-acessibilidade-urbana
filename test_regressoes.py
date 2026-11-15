import unittest
from app import run

class AccessibilityTests(unittest.TestCase):
    def test_prioritizes_fewer_impassable_barriers(self):
        data={"origem":"Natal","destino":"Centro","percursos":[{"nome":"A","paradas":[],"barreiras":[{"local":"Rua A","tipo":"degrau","impeditiva":True}]},{"nome":"B","paradas":[],"barreiras":[{"local":"Rua B","tipo":"piso","impeditiva":False}]}]}
        result=run(data)
        self.assertEqual(result["menos_barreiras_registradas"],"B")
        self.assertEqual(result["percursos"][0]["impeditivas"],0)

    def test_rejects_non_boolean_barrier(self):
        with self.assertRaises(ValueError):
            run({"origem":"Natal","destino":"Centro","percursos":[{"nome":"A","paradas":[],"barreiras":[{"local":"Rua A","tipo":"degrau","impeditiva":"sim"}]}]})

if __name__=="__main__": unittest.main()
