import pandas as pd
from  flask import Flask, request, Response
import json
import os
from datetime import datetime
import csv


#############################################################################################################
#################################  CENSO BRASIL #############################################################
#############################################################################################################
#####API 1 /consulta-censo-municipio-por-genero
file_path = 'sources/censo/Faixa Etaria por Municipio.csv'
df_principal = pd.read_csv(file_path, encoding='utf-8')
df_principal = df_principal[df_principal['Nivel'] == 'MU']
df_principal = pd.DataFrame(df_principal).sort_values(by=['Cod'],ascending=True)

#####API 2 /consulta-censo-municipio-por-alfabetizacao
file_path = 'sources/censo/Alfabetizacao.csv'
df_alfabetizacao = pd.read_csv(file_path, encoding='utf-8')
df_alfabetizacao = df_alfabetizacao[df_alfabetizacao['Nivel'] == 'MU']
df_alfabetizacao = pd.DataFrame(df_alfabetizacao).sort_values(by=['Cod'],ascending=True)


####API 3 /consulta-censo-municipio-por-area
file_path = 'sources/censo/Densidade.csv'
df_densidade = pd.read_csv(file_path, encoding='utf-8')
df_densidade = df_densidade[df_densidade['Nivel'] == 'MU']
df_densidade = pd.DataFrame(df_densidade).sort_values(by=['Cod'],ascending=True)


####API 4 /consulta-censo-estado-por-favelas
file_path = 'sources/censo/favelas.csv'
df_favelas = pd.read_csv(file_path, encoding='utf-8')
df_favelas = df_favelas[df_favelas['nivel'] == 'UF']
df_favelas = pd.DataFrame(df_favelas).sort_values(by=['sigla'],ascending=True)


####API 5 /consulta-censo-municipio-por-quilombola
file_path = 'sources/censo/Quilombolas.csv'
df_quilombolas = pd.read_csv(file_path, encoding='utf-8')
df_quilombolas = df_quilombolas[df_quilombolas['nivel'] == 'MU']
df_quilombolas = pd.DataFrame(df_quilombolas).sort_values(by=['sigla'],ascending=True)


####API 6 /consulta-censo-municipio-por-quilombola
file_path = 'sources/censo/n_favelas_municipios.csv'
df_favelas_municipio = pd.read_csv(file_path, encoding='utf-8')
df_favelas_municipio = pd.DataFrame(df_favelas_municipio).sort_values(by=['UF'],ascending=True)


####API 7 /consulta-domicilios-favelas-por-uf
file_path = 'sources/censo/relacao_favelas.csv'
df_comunidades_municipio = pd.read_csv(file_path, encoding='utf-8')
df_comunidades_municipio = pd.DataFrame(df_comunidades_municipio).sort_values(by=['Sigla'],ascending=True)


####API 8 /consulta-aldeias-indigenas-por-uf
file_path = 'sources/censo/aldeias_pontos.csv'
df_aldeias = pd.read_csv(file_path, encoding='utf-8')
df_aldeias = pd.DataFrame(df_aldeias).sort_values(by=['Cod'],ascending=True)


app = Flask(__name__)


#####API 1
@app.route('/consulta-censo-municipio-por-genero', methods=['GET'])
def consulta_genero():
    param = request.args.get('UF')
    colunas = ['Cod','Municipio','Sigla','Total','TotalHomem','TotalMulher']
    #registrar_acesso("/consulta-censo-municipio-por-genero")
    if param:
        resultado = df_principal[df_principal['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório .")



####API 2
@app.route('/consulta-censo-municipio-por-alfabetizacao', methods=['GET'])
def consulta_alfabetizacao():
    param = request.args.get('UF')
    colunas = ['Cod','Cep','Sigla','Total_Alfabetizadas','Total_Nao_Alfabetizadas','Total_Alfabetizados_Perct']
    #registrar_acesso("/consulta-censo-municipio-por-alfabetizacao")
    if param:
        resultado2 = df_alfabetizacao[df_alfabetizacao['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado2.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")

####API 3 /consulta-censo-municipio-por-area
@app.route('/consulta-censo-municipio-por-area', methods=['GET'])
def consulta_area():
    param = request.args.get('UF')
    colunas = ['Cod','Cep','UF','Area','Densidade']
    #registrar_acesso("/consulta-censo-municipio-por-area")
    if param:
        resultado3 = df_densidade[df_densidade['UF'] == param.upper()][colunas]
        json_result = json.dumps(resultado3.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")

####API 4 /consulta-censo-estado-por-favelas
@app.route('/consulta-censo-estado-por-favelas', methods=['GET'])
def consulta_favelas():
    colunas = ['cep','sigla','Total','Branca','Preta','Parda','Indigena','Amarela','Sd']
    #registrar_acesso("/consulta-censo-estado-por-favelas")
    resultado4 = df_favelas[colunas]
    json_result = json.dumps(resultado4.to_dict(orient='records'), ensure_ascii=False)
    return Response(json_result, content_type='application/json; charset=utf-8')

####API 5 /consulta-censo-municipio-por-quilombola
@app.route('/consulta-censo-municipio-por-quilombola', methods=['GET'])
def consulta_quilombola():
    param = request.args.get('UF')
    colunas = ['Cod','cep','municipio','nivel','sigla','total','em_territorio_quilombola','fora_territorio_quilombola']
    #registrar_acesso("/consulta-censo-municipio-por-quilombola")
    if param:
        resultado5 = df_quilombolas[df_quilombolas['sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado5.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")


####API 6 /consulta-censo-municipio-por-qtd-favelas
@app.route('/consulta-censo-municipio-por-qtd-favelas', methods=['GET'])
def consulta_qtd_favelas():
    param = request.args.get('UF')
    colunas = ['UF','Municipio','Qtd_Favelas']
    #registrar_acesso("/consulta-censo-municipio-por-qtd-favelas")
    if param:
        resultado6 = df_favelas_municipio[df_favelas_municipio['UF'] == param.upper()][colunas]
        json_result = json.dumps(resultado6.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório.")

#####API 7
@app.route('/consulta-domicilios-favelas-por-uf', methods=['GET'])
def consulta_domicilios_favela():
    param = request.args.get('UF')
    colunas = ['Cod','Favela','Municipio','Sigla','Domicilios']
    #registrar_acesso("/consulta-censo-municipio-por-genero")
    if param:
        resultado7 = df_comunidades_municipio[df_comunidades_municipio['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado7.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório .")


#####API 8
@app.route('/consulta-aldeias-indigenas-por-uf', methods=['GET'])
def consulta_aldeias_indigenas():
    param = request.args.get('UF')
    colunas = ['Cod','Aldeia','Municipio','Latitude','Longitude']
    #registrar_acesso("/consulta-aldeias_indigenas-por-uf")
    if param:
        resultado8 = df_aldeias[df_aldeias['sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado8.to_dict(orient='records'), ensure_ascii=False)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF obrigatório .")


#############################################################################################################
#################################  ANNE FRANK  ##############################################################
#############################################################################################################

####API 9 /anne-frank-events
file_path = 'sources/anne_frank/events.csv'
df_events = pd.read_csv(file_path, encoding='utf-8')
df_events['city'] = df_events['city'].str.lower().str.strip()

####API 10 /anne-frank-locations
file_path = 'sources/anne_frank/locations.csv'
df_locations = pd.read_csv(file_path, encoding='utf-8')

####API 11 /anne-frank-characters
file_path = 'sources/anne_frank/persons.csv'
df_characters = pd.read_csv(file_path, encoding='utf-8')

####API 9 /anne-frank-events
@app.route('/anne-frank-events', methods=['GET'])
def events():
    file_path = 'sources/anne_frank/events.csv'
    df_events = pd.read_csv(file_path, encoding='utf-8')
    df_events['city'] = df_events['city'].str.lower().str.strip()
    #registrar_acesso("/anne-frank-events")

    param = request.args.get('city')
    colunas = ['city','latitude','longitude','place','event','summary','date','date_start','date_end','content','image']
    if param:
        resultado9 = df_events[df_events['city'] == param.lower().strip()][colunas]
    else:
        resultado9 = df_events[colunas]
    json_result = json.dumps(resultado9.to_dict(orient='records'), ensure_ascii=False)
    return Response(json_result, content_type='application/json; charset=utf-8')


####API 10 /anne-frank-locations
@app.route('/anne-frank-locations', methods=['GET'])
def locations():
    colunas = ['latitude','longitude','title','content','image','image_desc']
    df_locations.loc[df_locations['image_desc'] == 'Unknown Photo', 'image'] = 'Not Available'
    #registrar_acesso("/anne-frank-locations")

    resultado10 = df_locations[colunas]
    json_result = json.dumps(resultado10.to_dict(orient='records'), ensure_ascii=False)
    return Response(json_result, content_type='application/json; charset=utf-8')

####API 11 /anne-frank-characters
@app.route('/anne-frank-characters', methods=['GET'])
def characters():
    param = request.args.get('name')
    colunas = ['image_description','image','title','first_name','last_name','birth_date','death_date','gender','birth_place','death_place','birth_country','summary','content','death_country']
    df_characters.loc[df_characters['image_description'] == 'Unknown Photo', 'image'] = 'Not Available'
    #registrar_acesso("/anne-frank-characters")

    if param:
        resultado11 = df_characters[df_characters['title'].str.lower().str.contains(param.lower().strip(), na=False)][colunas]
    else:
        resultado11 = df_characters[colunas]
    json_result = json.dumps(resultado11.to_dict(orient='records'), ensure_ascii=False)
    return Response(json_result, content_type='application/json; charset=utf-8')

if __name__ == "__main__":
    app.run(debug=True)