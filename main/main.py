import pandas as pd
from  flask import Flask, request, Response
from  flask import url_for
import requests
import json
import folium
from datetime import datetime
import plotly.graph_objects as go
import csv

###############################################################################################
#CRIA APIS DO CENSO-BRASIL-WIKI E DA ANNE-FRANK-WIKI
#CRIA API DE MONITORAMENTO (/MONITOR) C/ HTML DO LOG GRAVADO NO MONITOR.CSV

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


def registra_log(origin,endpoint,start_time,end_time,ip,city,country,lat,lon,navegador,status):
    log_file = 'logs/monitor.csv'
    with open(log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([origin,endpoint,start_time,end_time,ip,city,country,lat,lon,navegador,status])



app = Flask(__name__)



#####API 1
@app.route('/consulta-censo-municipio-por-genero', methods=['GET'])
def consulta_genero():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()
    colunas = ['Cod','Municipio','Sigla','Total','TotalHomem','TotalMulher']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""
    if param:
        resultado = df_principal[df_principal['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "1", start_time, end_time, ip,city,country,lat,lon, navegador,response.status_code)
        return response
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "1", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório .")





####API 2
@app.route('/consulta-censo-municipio-por-alfabetizacao', methods=['GET'])
def consulta_alfabetizacao():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()
    colunas = ['Cod','Cep','Sigla','Total_Alfabetizadas','Total_Nao_Alfabetizadas','Total_Alfabetizados_Perct']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""


    #registrar_acesso("/consulta-censo-municipio-por-alfabetizacao")
    if param:
        resultado2 = df_alfabetizacao[df_alfabetizacao['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado2.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "2", start_time, end_time, ip,city,country,lat,lon, navegador,response.status_code)
        return Response(json_result, content_type='application/json; charset=utf-8')
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "2", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")

####API 3 /consulta-censo-municipio-por-area
@app.route('/consulta-censo-municipio-por-area', methods=['GET'])
def consulta_area():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()
    colunas = ['Cod','Cep','UF','Area','Densidade']
    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado3 = df_densidade[df_densidade['UF'] == param.upper()][colunas]
        json_result = json.dumps(resultado3.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "3", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
        return response
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "3", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")

####API 4 /consulta-censo-estado-por-favelas
@app.route('/consulta-censo-estado-por-favelas', methods=['GET'])
def consulta_favelas():
    colunas = ['cep','sigla','Total','Branca','Preta','Parda','Indigena','Amarela','Sd']
    start_time = datetime.now().isoformat()

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    resultado4 = df_favelas[colunas]
    json_result = json.dumps(resultado4.to_dict(orient='records'), ensure_ascii=False)
    response = Response(json_result, content_type='application/json; charset=utf-8')
    end_time = datetime.now().isoformat()
    registra_log("censo-wiki", "4", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
    return response

####API 5 /consulta-censo-municipio-por-quilombola
@app.route('/consulta-censo-municipio-por-quilombola', methods=['GET'])
def consulta_quilombola():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()

    colunas = ['Cod','cep','municipio','nivel','sigla','total','em_territorio_quilombola','fora_territorio_quilombola']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado5 = df_quilombolas[df_quilombolas['sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado5.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "5", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
        return response
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "5", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")


####API 6 /consulta-censo-municipio-por-qtd-favelas
@app.route('/consulta-censo-municipio-por-qtd-favelas', methods=['GET'])
def consulta_qtd_favelas():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()

    colunas = ['UF','Municipio','Qtd_Favelas']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado6 = df_favelas_municipio[df_favelas_municipio['UF'] == param.upper()][colunas]
        json_result = json.dumps(resultado6.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "6", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
        return response
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "6", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")

#####API 7
@app.route('/consulta-domicilios-favelas-por-uf', methods=['GET'])
def consulta_domicilios_favela():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()

    colunas = ['Cod','Favela','Municipio','Sigla','Domicilios']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado7 = df_comunidades_municipio[df_comunidades_municipio['Sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado7.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "7", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
        return response

    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "7", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")


#####API 8
@app.route('/consulta-aldeias-indigenas-por-uf', methods=['GET'])
def consulta_aldeias_indigenas():
    param = request.args.get('UF')
    start_time = datetime.now().isoformat()

    colunas = ['Cod','Aldeia','Municipio','Latitude','Longitude']

    ###dados do usuário requisitante
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado8 = df_aldeias[df_aldeias['sigla'] == param.upper()][colunas]
        json_result = json.dumps(resultado8.to_dict(orient='records'), ensure_ascii=False)
        response = Response(json_result, content_type='application/json; charset=utf-8')
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "8", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
        return response
    else:
        end_time = datetime.now().isoformat()
        registra_log("censo-wiki", "8", start_time, end_time, ip,city,country,lat,lon, navegador,"500")
        return ("Favor informar a sigla de uma Unidade Federativa. O campo UF é obrigatório.")


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

    ###dados do usuário requisitante
    start_time = datetime.now().isoformat()
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""


    param = request.args.get('city')
    colunas = ['city','latitude','longitude','place','event','summary','date','date_start','date_end','content','image']
    if param:
        resultado9 = df_events[df_events['city'] == param.lower().strip()][colunas]
    else:
        resultado9 = df_events[colunas]
    json_result = json.dumps(resultado9.to_dict(orient='records'), ensure_ascii=False)
    response = Response(json_result, content_type='application/json; charset=utf-8')
    end_time = datetime.now().isoformat()
    registra_log("anne-frank-wiki", "9", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
    return response


####API 10 /anne-frank-locations
@app.route('/anne-frank-locations', methods=['GET'])
def locations():
    colunas = ['latitude','longitude','title','content','image','image_desc']
    df_locations.loc[df_locations['image_desc'] == 'Unknown Photo', 'image'] = 'Not Available'

    ###dados do usuário requisitante
    start_time = datetime.now().isoformat()
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    resultado10 = df_locations[colunas]
    json_result = json.dumps(resultado10.to_dict(orient='records'), ensure_ascii=False)
    response = Response(json_result, content_type='application/json; charset=utf-8')
    end_time = datetime.now().isoformat()
    registra_log("anne-frank-wiki", "10", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
    return response

####API 11 /anne-frank-characters
@app.route('/anne-frank-characters', methods=['GET'])
def characters():
    param = request.args.get('name')
    colunas = ['image_description','image','title','first_name','last_name','birth_date','death_date','gender','birth_place','death_place','birth_country','summary','content','death_country']
    df_characters.loc[df_characters['image_description'] == 'Unknown Photo', 'image'] = 'Not Available'

    ###dados do usuário requisitante
    start_time = datetime.now().isoformat()
    ip = request.headers.get("X-Real-IP")
    navegador = request.headers.get("User-Agent")

    ###coordenadas
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
        response_coordenada = requests.get(url, timeout=3)
        data = response_coordenada.json()
        if data.get("status") == "success":
            city = data.get("city", "")
            country = data.get("country", "")
            lat = data.get("lat", "")
            lon = data.get("lon", "")
        else:
            city = ""
            country = ""
            lat = ""
            lon = ""
    except Exception as e:
        city = ""
        country = ""
        lat = ""
        lon = ""

    if param:
        resultado11 = df_characters[df_characters['title'].str.lower().str.contains(param.lower().strip(), na=False)][colunas]
    else:
        resultado11 = df_characters[colunas]
    json_result = json.dumps(resultado11.to_dict(orient='records'), ensure_ascii=False)
    response = Response(json_result, content_type='application/json; charset=utf-8')
    end_time = datetime.now().isoformat()
    registra_log("anne-frank-wiki", "11", start_time, end_time, ip,city,country,lat,lon, navegador, response.status_code)
    return response


#######################################     MONITOR     #################################################
@app.route('/monitor', methods=['GET'])
def monitor():
    ##css para a página html
    css_url = url_for('static', filename='main.css')

    # cria o dataframe do monitor a ser usado no app para os gráficos
    local_path = 'logs/monitor.csv'
    colunas = ['origin', 'endpoint', 'start_time', 'end_time', 'ip', 'navegador', 'status']
    df_monitor = pd.read_csv(
        local_path,
        names=colunas,
        header=None
    )
    ###CENSO BRASIL
    df_censo = df_monitor[df_monitor['origin']=='censo-wiki']

    ###ANNE-FRANK
    df_frank = df_monitor[df_monitor['origin']=='anne-frank-wiki']

    ###INDICADORES
    total = len(df_monitor['origin'])

    ###TEMÁTICA
    total_censo = len(df_censo['origin'])
    total_anne_frank = len(df_frank['origin'])
    censo_prct = round((total_censo/total)*100,2)
    anne_frank_prct = round((total_anne_frank / total) * 100,2)

    ####ENDPOINTS
    total_endpoint = len(df_monitor['endpoint'].unique())

    def calcula_acesso_edpoint(endpoint):
        return str(len(df_monitor[df_monitor['endpoint']==endpoint]))

    ####STATUS RESPONSE
    response_ok = len(df_monitor[df_monitor['status']==200])
    response_ok = round((response_ok/total)*100, 2)
    response_nok = len(df_monitor[df_monitor['status']==500])
    response_nok = round((response_nok/total)*100, 2)

    ##status por endpoint
    def calcula_status_endpoint(endpoint):
        df_monitor_endpoint = df_monitor[df_monitor['endpoint']==endpoint]
        if len(df_monitor_endpoint['endpoint'])==0:
            return 0
        else:
            response_ok_endpoint = len(df_monitor_endpoint[df_monitor_endpoint['status'] == 200])
            response_ok_endpoint = round(( response_ok_endpoint / len(df_monitor_endpoint))*100,2)
            return response_ok_endpoint


    ###TEMPO DE RESPOSTA
    ##converte campos de timestamp em datetime
    df_monitor["start_time"] = pd.to_datetime(df_monitor["start_time"])
    df_monitor["end_time"] = pd.to_datetime(df_monitor["end_time"])

    ##nova coluna de tempo de resposta
    df_monitor["response_time_ms"] = (df_monitor["end_time"] - df_monitor["start_time"]).dt.total_seconds() * 1000

    ##média
    response_time_ms = df_monitor["response_time_ms"].mean()

    ##CALCULA TEMPO MÉDIO POR ENDPOINT
    def calcula_tempo_endpoint(endpoint):
        df_monitor_endpoint = df_monitor[df_monitor['endpoint']==endpoint]
        if len(df_monitor_endpoint['endpoint'])==0:
            return 0
        else:
            start = pd.to_datetime(df_monitor_endpoint["start_time"])
            end = pd.to_datetime(df_monitor_endpoint["end_time"])
            response_time_ms_endpoint = round(((end - start).dt.total_seconds() * 1000).mean(), 2)
            return response_time_ms_endpoint

    ####MAPA COM LOCALIDADES DOS ACESSOS
    cont = 0
    coordenadas_iniciais = [20, 0] ##coordenada geral
    mapa = folium.Map(location=coordenadas_iniciais, zoom_start=2)


    while cont < len(df_monitor['lat']):
        lat = df_monitor['lat'].iloc[cont]
        lon = df_monitor['lon'].iloc[cont]
        city = df_monitor['city'].iloc[cont]
        country = df_monitor['country'].iloc[cont]
        acessos_ip = str(len(df_monitor[df_monitor['ip'] == df_monitor['ip'].iloc[cont]]))
        folium.Marker(
            location=[lat, lon],
            tooltip=city + ',' + country + ',' + acessos_ip + ' acesso(s)',
            icon=folium.Icon(color='lightred')
        ).add_to(mapa)
        mapa.save('static/mapa.html')

        cont = cont + 1


    ###NAVEGADORES
    edge = df_monitor['navegador'].str.contains('Edg/', na=False).sum()
    edge = round((edge/total)*100,2)
    firefox = df_monitor['navegador'].str.contains('Firefox/', na=False).sum()
    firefox = round((firefox / total) * 100, 2)
    opera = (
            df_monitor['navegador'].str.contains('OPR/', na=False)
            | df_monitor['navegador'].str.contains('Opera/', na=False)
    ).sum()
    opera = round((opera / total) * 100, 2)

    ###na linha do chrome, aparecem tbm edge, opera (compatibilidade)
    chrome = (
            df_monitor['navegador'].str.contains('Chrome/', na=False)
            & ~df_monitor['navegador'].str.contains('Edg/', na=False)
            & ~df_monitor['navegador'].str.contains('OPR/', na=False)
            & ~df_monitor['navegador'].str.contains('Opera/', na=False)
    ).sum()
    chrome = round((chrome / total) * 100, 2)
    safari = (
            df_monitor['navegador'].str.contains('Safari/', na=False)
            & ~df_monitor['navegador'].str.contains('Chrome/', na=False)
            & ~df_monitor['navegador'].str.contains('Edg/', na=False)
    ).sum()
    safari = round((safari / total) * 100, 2)

    outros = round(100 - (safari + opera + edge + chrome + firefox),2)

    categorias = ['Edge','Firefox','Safari','Opera','Chrome', 'Outros']
    valores = [edge, firefox, safari , opera , chrome, outros]

    fig = go.Figure(data=[go.Pie(
        labels=categorias,
        values=valores,
        hole=0.8,  # Define o tamanho do buraco (0.4 significa 40% do tamanho total)
        marker=dict(
            colors=['#f56a6a', '#940606', '#7b3535', '#f89797', '#ffc0cb','#f7dcdc'],# Cores personalizadas: verde acra alfabetizados e vermelho acra não alfabetizados
            line=dict(color='white', width=1)  # Cor e espessura da linha de contorno
        ),
        textinfo='none',
        hoverinfo='label+percent',
        hoverlabel=dict(
            font_size=12,  # Tamanho da fonte do tooltip
            font_family="Segoe UI",  # Fonte do tooltip
            font_color="white",  # Cor da letra do tooltip
            bgcolor='#f56a6a'
        )
    )])

    # Atualizar o layout acra adicionar título e definir o tamanho da fonte
    fig.update_layout(
        annotations=[dict(text='%', x=0.5, y=0.5, font_size=52, font_color='#f56a6a', showarrow=False)],
        plot_bgcolor='white',  # Cor de fundo do gráfico (dentro da área de plotagem)
        paper_bgcolor='white',  # Cor de fundo do esacço da página
        legend=dict(
            orientation="v",  # Orientação vertical (legenda ao lado)
            yanchor="middle",  # Ancoragem da legenda
            y=0.5,  # Posição vertical da legenda
            xanchor="left",  # Ancoragem horizontal
            x=1.1,  # Posição horizontal da legenda (1.1 coloca a legenda à direita do gráfico)
            font=dict(
                size=12,  # Tamanho da fonte da legenda
                color="#f56a6a"  # Cor da fonte da legenda
            ),
        ),
        margin=dict(t=30, b=30, l=30, r=100)
    )
    # Salvar o gráfico como HTML
    fig.write_html('static/navegadores.html', include_plotlyjs='cdn')


    return f"""
        <html>
        <head>
        <link href="{css_url}" rel="stylesheet">
        <link rel="icon" href="static/logo.png" type="image/x-icon">
        </head>
        <body>
        <div id="wrapper" style="margin-top:2em; margin-left:5em;">
    	<div id="main">
    	<div class="content" width="40%" >
    	    <header class="major">
            <h2 style="color:#f56a6a; font-size:32px;">Visão Geral</h2>
            </header>
        </div>
    	<div id="banner" width="100%" style="margin-top:-9em;">
        <header class="major">
            <div class="content" style="width:200px;">
                <h2 style="font-size: 32px; color:#f56a6a;" align="left">{"{:,}".format(total)}</h2>
                <p><strong>Total</strong> acessos</p>
            </div>
        </header>
        <div style="width: 1px; padding-left:2em;"></div>
        <header class="major">
            <div class="content"  style="width:200px; ">
                <h2 style="font-size: 32px; color:#f56a6a;" align="left">{"{:,}".format(total_censo)}</h2>
                <p>Censo do Brasil <strong>{censo_prct} %</strong> </p>
            </div>
        </header>
        <div style="width: 1px; padding-left:2em;"></div>
        <header class="major">
            <div class="content"  style="width:250px;">
                <h2 style="font-size: 32px; color:#f56a6a;" align="left">{"{:,}".format(total_anne_frank)}</h2>
                <p>Anne Frank Wiki <strong>{anne_frank_prct} % </strong> </p>
            </div>
        </header>
        <div style="width: 10em; "></div>
        <div style="width: 1px; height: 100px; background-color:#dde1e3;"></div>
        <div style="width: 10em;"></div>
        <header>
            <div class="content"  style="width:200px;" >
                <h2 style="font-size: 48px; color:#f56a6a; margin-left:0.25em;" align="left">{"{:,}".format(total_endpoint)}</h2>
                <h3 align="left">Endpoints</h3>
            </div>
        </header>
        </div>
        </div>
        </div>
        <div class="content" align="center" style="margin-top:-25em;">
                <iframe src="static/mapa.html" height="400px" width="90%"></iframe>
        </div>
        <div class="content" style="margin-top:2em; margin-left:5em; margin-right:5em;">
            <div id="banner" style="margin-top:-5em;">
                <div class="content" width="40%" >
                    <header class="major">
                    <h2 style="color:#f56a6a; font-size:32px;">Responses</h2>
                    </header>
                </div>
                <div class="content" width="60%" style="margin-left:5em;">
                    <header class="major">
                    <h2 style="color:#f56a6a; font-size:32px;">Navegadores</h2>
                    </header>
                </div>
            </div>
            <div style="display:flex; gap:3em; align-items:flex-start; margin-top:-5em;">
                <div class="content">
                    <header class="major">
                    <h2 style="font-size: 24px; color:#f56a6a;" align="left">{"{:,}".format(response_ok)} %</h2>
                    <p>Status <strong> "200" </strong> </p>
                    </header>
                </div>
                <div class="content">
                    <header class="major">
                    <h2 style="font-size: 24px; color:#f56a6a;" align="left">{"{:,}".format(response_nok)} %</h2>
                    <p>Status <strong> "500" </strong> </p>
                    </header>
                </div>
                <div style="width: 1px; height: 80px; background-color:#dde1e3;"></div>
                <div class="content" style="margin-left:1em;">
                    <header class="major">
                    <h2 style="font-size: 24px; color:#f56a6a;" align="left">{"{:,.2f}".format(response_time_ms)} ms</h2>
                    <p>Tempo <strong> médio </strong> </p>
                    </header>
                </div>
                <iframe src="static/navegadores.html" height="200px" width="450px" align="right"></iframe>
            </div>
            <br>
                <div class="content" width="40%" >
                    <header class="major">
                    <h2 style="color:#f56a6a; font-size:32px;">Endpoints</h2>
                    </header>
                </div>
            <table align="center">
            <thead>
			<tr>
				<th></th>
				<th>Temática</th>
				<th>Endpoint</th>
				<th>Acesso(s)</th>
				<th>Tempo médio (ms)</th>
				<th>Tx. Sucesso (%)</th>
			</tr>
			</thead>
            <tr>
                <th><h3>1</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-municipio-por-genero</h3></th>
                <th><h3>{calcula_acesso_edpoint(1)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(1)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(1)} %</h3></th>
            </tr>
            <tr>
                <th><h3>2</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-municipio-por-alfabetizacao</h3></th>
                <th><h3>{calcula_acesso_edpoint(2)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(2)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(2)} %</h3></th>
            </tr>
            <tr>
                <th><h3>3</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-municipio-por-area</h3></th>
                <th><h3>{calcula_acesso_edpoint(3)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(3)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(3)} %</h3></th>
            </tr>
            <tr>
                <th><h3>4</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-estado-por-favelas</h3></th>
                <th><h3>{calcula_acesso_edpoint(4)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(4)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(4)} %</h3></th>
            </tr>
            <tr>
                <th><h3>5</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-municipio-por-quilombola</h3></th>
                <th><h3>{calcula_acesso_edpoint(5)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(5)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(5)} %</h3></th>
            </tr>
            <tr>
                <th><h3>6</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-censo-municipio-por-qtd-favelas</h3></th>
                <th><h3>{calcula_acesso_edpoint(6)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(6)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(6)} %</h3></th>
            </tr>
            <tr>
                <th><h3>7</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-domicilios-favelas-por-uf</h3></th>
                <th><h3>{calcula_acesso_edpoint(7)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(7)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(7)} %</h3></th>
            </tr>
            <tr>
                <th><h3>8</h3></th>
                <th>censo-brasil-wiki</th>
                <th><h3>/consulta-aldeias-indigenas-por-uf</th>
                <th><h3>{calcula_acesso_edpoint(8)}</th>
                <th><h3>{calcula_tempo_endpoint(8)} ms</th>
                <th><h3>{calcula_status_endpoint(8)} %</th>
            </tr>
            <tr>
                <th><h3>9</h3></th>
                <th>anne-frank-wiki</th>
                <th><h3>/anne-frank-events</h3></th>
                <th><h3>{calcula_acesso_edpoint(9)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(9)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(9)} %</h3></th>
            </tr>
            <tr>
                <th><h3>10</h3></th>
                <th>anne-frank-wiki</th>
                <th><h3>/anne-frank-locations</h3></th>
                <th><h3>{calcula_acesso_edpoint(10)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(10)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(10)} %</h3></th>
            </tr>            
            <tr>
                <th><h3>11</h3></th>
                <th>anne-frank-wiki</th>
                <th><h3>/anne-frank-characters</h3></th>
                <th><h3>{calcula_acesso_edpoint(11)}</h3></th>
                <th><h3>{calcula_tempo_endpoint(11)} ms</h3></th>
                <th><h3>{calcula_status_endpoint(11)} %</h3></th>
            </tr>  
            </table>
            <p align="right">Atualizado em {datetime.now().replace(microsecond=0)}</p>
        </div>
        </body>
        </html>
    """



if __name__ == "__main__":
    app.run(debug=True)