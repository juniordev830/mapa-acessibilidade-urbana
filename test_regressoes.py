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

    def test_reject_malformed_route_collection(self):
        base = {"origem": "Natal", "destino": "Centro"}
        for routes in ("text", [None], [1], [{}] * 31):
            with self.subTest(routes=routes), self.assertRaisesRegex(ValueError, "percursos"):
                run({**base, "percursos": routes})

    def test_reject_duplicate_path_names(self):
        base = {"origem": "Natal", "destino": "Centro",
                "percursos": [{"nome": name, "barreiras": [], "paradas": []}
                             for name in ("Centro", " centro ")]}
        with self.assertRaisesRegex(ValueError, "repetido"):
            run(base)

    def test_reject_invalid_barrier_shape_or_excessive_count(self):
        base = {"origem": "Natal", "destino": "Centro"}
        for barriers in ("texto", [None], [{}] * 201):
            with self.subTest(barriers=str(barriers)[:16]), self.assertRaisesRegex(ValueError, "barreiras"):
                run({**base, "percursos": [
                    {"nome": "Norte", "paradas": [], "barreiras": barriers}]})

    def test_empty_path_collection_returns_no_recommendation(self):
        self.assertEqual(run({"origem": "Natal", "destino": "Centro", "percursos": []}),
                         {"percursos": [], "menos_barreiras_registradas": None})


if __name__=="__main__": unittest.main()
