import pandas as pd
from  flask import Flask, request, Response
import json


file_path = 'sources/Faixa Etaria por Municipio.csv'
df = pd.read_csv(file_path, encoding='utf-8')

df = df[df['Nivel'] == 'MU']

df = pd.DataFrame(df).sort_values(by=['Cod'],ascending=True)

file_path = 'sources/Alfabetizacao.csv'
df2 = pd.read_csv(file_path, encoding='utf-8')
df2 = df2[df2['Nivel'] == 'MU']
df2 = pd.DataFrame(df2).sort_values(by=['Cod'],ascending=True)

file_path = 'sources/Densidade.csv'
df3 = pd.read_csv(file_path, encoding='utf-8')
df3 = df3[df3['Nivel'] == 'MU']
df3 = pd.DataFrame(df3).sort_values(by=['Cod'],ascending=True)

app = Flask(__name__)

@app.route('/consulta-censo-municipio-por-genero', methods=['GET'])
def consulta_genero():
    param = request.args.get('UF')
    colunas = ['Cod','Municipio','Sigla','Total','TotalHomem','TotalMulher']
    if param:
        resultado = df[df['Sigla'] == param][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório .")

@app.route('/consulta-censo-municipio-por-alfabetizacao', methods=['GET'])
def consulta_alfabetizacao():
    param = request.args.get('UF')
    colunas = ['Cod','Municipio','Sigla','Total_Alfabetizadas','Total_Nao_Alfabetizadas','Total_Alfabetizados_Perct']
    if param:
        resultado = df2[df2['Sigla'] == param][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")

@app.route('/consulta-censo-municipio-por-area', methods=['GET'])
def consulta_area():
    param = request.args.get('UF')
    colunas = ['Cod','Cep','UF','Area','Densidade']
    if param:
        resultado = df3[df3['Sigla'] == param][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")

