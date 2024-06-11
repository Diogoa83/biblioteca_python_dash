import unittest
import pandas as pd
from my_plotly_package.plotly_utils import criar_grafico_barras

class TestPlotlyUtils(unittest.TestCase):
    def test_criar_grafico_barras(self):
        data = {'municipio_paciente': ['Município 1', 'Município 2'],
                'contagem_dose': [100, 200],
                'sexo': ['Masculino', 'Feminino']}
        df = pd.DataFrame(data)
        fig = criar_grafico_barras(df, 'municipio_paciente', 'contagem_dose', 'Teste', 500, 1500, 'sexo', 'contagem_dose', {'Masculino': '#8ac0de', 'Feminino': '#f5c9bf'}, {'Faixa Etaria': 'Faixa Etaria', 'Contagem Doses': 'Contagem Doses'}, 'h')
        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()
