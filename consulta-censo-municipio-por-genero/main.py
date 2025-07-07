import pandas as pd
from  flask import Flask, request, Response
import json


file_path = 'sources/Faixa Etaria por Municipio.csv'
df = pd.read_csv(file_path, encoding='utf-8')

df = df[df['Nivel'] == 'MU']

df = pd.DataFrame(df).sort_values(by=['Cod'],ascending=True)

app = Flask(__name__)

@app.route('/consulta-censo-municipio-por-genero', methods=['GET'])
def consulta_events():
    param = request.args.get('UF')
    colunas = ['Cod','Municipio','Sigla','Total','TotalHomem','TotalMulher']
    if param:
        resultado = df[df['Sigla'] == param][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório .")

