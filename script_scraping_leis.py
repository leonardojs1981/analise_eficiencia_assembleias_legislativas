######## Script para baixar leis de Assembléias Legislativas ########
######## Obs: Não há um padrão, assim existe um script para cada AL.#######
######## Em vários casos, uma tabela com as ementas já era disponibilizada diretamente na página da AL. Nesses casos, não há código..#######

# 0. Pacotes
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import math
import ssl



# 1. MT
dict_ementas = {}
for pagina in range(1,15):
    page = urllib.request.urlopen("http://www.al.mt.gov.br/legislacao/?tipo=1&restringeBusca=e&palavraChave=&numeroNorma=&anoNorma=2016&autor=&search=&page=" + str(pagina))
    soup = BeautifulSoup(page)
    lista_ids = []
    for i in soup.find_all("span"):
        try:
            lista_ids.append(i.attrs["id"])
        except:
            pass
    leis = [k for k in lista_ids if 'ementa-prop' in k]
    ementas = [k for k in lista_ids if 'dado-prop' in k]

    for i in range(0,len(leis)):
        dict_ementas[soup.find(id=leis[i]).string.replace("  ","").replace("\n","")] = soup.find(id=ementas[i]).string.replace("  ","").replace("\n","")

ementas_mt = list(dict_ementas.values())

df_ementas_mt = pd.DataFrame(
    {'1_num_lei': list(dict_ementas.keys()),
     '2_ementa': list(dict_ementas.values())})

df_ementas_mt.to_csv("df_ementas_mt.csv")

# 2. PB
# view-source:http://sapl.al.pb.leg.br:8080/sapl/generico/RSS2_normas?incluir=0&lst_tip_norma=2&txt_numero=&txt_ano=2016&dt_norma=&dt_norma2=&dt_public=&dt_public2=&lst_assunto_norma=&txt_assunto=&lst_tip_situacao_norma=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar
page = urllib.request.urlopen("http://sapl.al.pb.leg.br:8080/sapl/generico/RSS2_normas?incluir=0&lst_tip_norma=2&txt_numero=&txt_ano=2016&dt_norma=&dt_norma2=&dt_public=&dt_public2=&lst_assunto_norma=&txt_assunto=&lst_tip_situacao_norma=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar")
soup = BeautifulSoup(page)

lista_leis = []
for i in soup.find_all("title"):
    for string in i.stripped_strings:
        lista_leis.append(string)
    print(i)

del lista_leis[1]

ementas_pb = []
for i in soup.find_all("description"):
    for string in i.stripped_strings:
        ementas_pb.append(string)
    print(i)

dict_leis_PB = {}

for i in range(1,214):
    dict_leis_PB[lista_leis[i]] = ementas_pb[i]
    print(i)

ementas_pb = list(dict_leis_PB.values())


# 3. PI
# http://servleg.al.pi.gov.br:9080/ALEPI/generico/norma_juridica_pesquisar_rss?incluir=0&lst_tip_norma=1&txt_numero=&txt_ano=2016&lst_assunto_norma=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&txt_assunto=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar
page = urllib.request.urlopen("http://servleg.al.pi.gov.br:9080/ALEPI/generico/norma_juridica_pesquisar_rss?incluir=0&lst_tip_norma=1&txt_numero=&txt_ano=2016&lst_assunto_norma=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&txt_assunto=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar")
soup = BeautifulSoup(page)

lista_leis = []
for i in soup.find_all("title"):
    for string in i.stripped_strings:
        lista_leis.append(string)
    print(i)

lista_ementas = []
for i in soup.find_all("description"):
    for string in i.stripped_strings:
        lista_ementas.append(string)
    print(i)

dict_leis_PI = {}

for i in range(1,182):
    dict_leis_PI[lista_leis[i]] = lista_ementas[i]
    print(i)

ementas_pi = list(dict_leis_PI.values())


# 4. AC
# www.al.ac.leg.br/leis/?cat=66&paged=2
lista_links = []
page = urllib.request.urlopen("http://www.al.ac.leg.br/leis/?cat=66")
soup = BeautifulSoup(page)
soup.find_all("a")
lista_tags = []
for i in soup.find_all("a"):
    try:
        lista_tags.append(i.attrs["href"])
    except:
        pass
lista_links = [k for k in lista_tags if '/leis/?p=' in k]


for i in range(2,6):
    page = urllib.request.urlopen("http://www.al.ac.leg.br/leis/?cat=66&paged="+str(i))
    soup = BeautifulSoup(page)
    soup.find_all("a")
    lista_tags = []
    for i in soup.find_all("a"):
        try:
            lista_tags.append(i.attrs["href"])
        except:
            pass
    lista_links += [k for k in lista_tags if '/leis/?p=' in k]

lista_links = set(lista_links)
lista_ids = [k.replace("http://www.al.ac.leg.br/leis/?p=", "") for k in lista_links]


lista_tags_2 = []
for i in lista_links:
    page_lei = urllib.request.urlopen(i)
    for line_number, line in enumerate(page_lei):
        # Because this is 0-index based
        if line_number == 260:
            #linha = line
            lista_tags_2.append(BeautifulSoup(line))
        # Stop reading
        elif line_number > 260:
            break
    print(i)

lista_leis = []
for i in lista_tags_2:
    try:
        lista_leis.append(i.a.string)
    except:
        pass

ementas_ac = []
for i in lista_tags_2:
    try:
        ementas_ac.append(i.p.text)
    except:
        pass

# 5. AM
# http://sapl.al.am.leg.br/generico/norma_juridica_pesquisar_rss?incluir=0&lst_tip_norma=1&txt_numero=&txt_ano=2016&lst_assunto_norma=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&txt_assunto=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
page = urllib.request.urlopen("http://sapl.al.am.leg.br/generico/norma_juridica_pesquisar_rss?incluir=0&lst_tip_norma=1&txt_numero=&txt_ano=2016&lst_assunto_norma=&dt_norma=&dt_norma2=&dt_public=&dt_public2=&txt_assunto=&em_vigencia=&rd_ordenacao=1&btn_norma_pesquisar=Pesquisar", context = gcontext)
soup = BeautifulSoup(page)

lista_leis = []
for i in range(1,len(soup.find_all("title"))):
    lista_leis.append(soup.find_all("title")[i].string.replace("\n","").replace(" ",""))
    print(i)

ementas_am = []
for i in range(1,len(soup.find_all("description"))):
    ementas_am.append(soup.find_all("description")[i].string.replace("&#8220","").replace("&#8221","").replace(";",""))
    print(i)

# 5. RO - LexML
# http://www.lexml.gov.br/busca/search?smode=advanced;f1-tipoDocumento=Legisla%C3%A7%C3%A3o::Lei;f2-autoridade=Estadual;expandGroup=date-2010s;f3-date=2010s::2016;f4-acronimo=RO%C2%A0%E2%80%93%C2%A0Rond%C3%B4nia;startDoc=1
ementas_ro = []
for i in range(1,188):
    start_num = math.floor(i/20.1)*20 + 1
    #print(str(i) + ", " + str(start_num))
    link = "http://www.lexml.gov.br/busca/search?smode=advanced;f1-tipoDocumento=Legisla%C3%A7%C3%A3o::Lei;f2-autoridade=Estadual;expandGroup=date-2010s;f3-date=2010s::2016;f4-acronimo=RO%C2%A0%E2%80%93%C2%A0Rond%C3%B4nia;startDoc="
    page = urllib.request.urlopen(link + str(start_num))
    doc = "id=\"add_" + str(i) + "\""
    for line_number, line in enumerate(page):
        if doc in str(line):
            line_2 = str(line.decode('utf-8')).replace("                           </script>","").replace("<script type=\"text/javascript\">","")
            soup = BeautifulSoup(line_2)
            ementas_ro.append(soup.find_all("td", "col3")[3].text)
    print(i)

# 6. RR
# http://www.tjrr.jus.br/legislacao/index.php/leis-ordinarias/124-leis-ordinarias-2016
soup = BeautifulSoup(open("rr.html"))

lista_links = []
for link in soup.find_all('a'):
    lista_links.append(link.get('href'))

lista_links = [k for k in lista_links if "124-leis" in str(k)]


page = urllib.request.urlopen("http://www.tjrr.jus.br" + "/legislacao/index.php/leis-ordinarias/124-leis-ordinarias-2016/1439-lei-n-1143-de-27-de-dezembro-de-2016")
soup = BeautifulSoup(page)


lista_tags = []
count = 0
for i in lista_links:
    count += 1
    page_lei = urllib.request.urlopen("http://www.tjrr.jus.br" + i)
    for line_number, line in enumerate(page_lei):
        # Because this is 0-index based
        if line_number == 93:
            #linha = line
            lista_tags.append(BeautifulSoup(line))
        # Stop reading
        elif line_number > 93:
            break
    print(count)


# 7. BA
# view-source:http://leisestaduais.com.br/ba?q=2016&page=1&types=&state=ba&date_start=&date_end=

lista_ementas = []
for i in range(1,15):
    page = urllib.request.urlopen("http://leisestaduais.com.br/ba?q=2016&page=" + str(i) + "&types=&state=ba&date_start=&date_end=")
    soup = BeautifulSoup(page)

    for link in soup.find_all("a"):
        lista_ementas.append(link.get("href"))
    print(i)

lista_ementas_ba = [k for k in lista_ementas if "ordinaria" in k]
lista_ementas_ba = [k.replace("q=2016", "").replace("/ba/lei-ordinaria-n-", "").replace("-", " ") for k in lista_ementas_ba if "2016-bahia" in k]


# 8. SC
# view-source:http://leisestaduais.com.br/sc?q=2016&page=1&types=&state=ba&date_start=&date_end=

lista_ementas = []
for i in range(1,52):
    page = urllib.request.urlopen("http://leisestaduais.com.br/sc?q=2016&page=" + str(i) + "&types=&state=sc&date_start=&date_end=")
    soup = BeautifulSoup(page)

    for link in soup.find_all("a"):
        lista_ementas.append(link.get("href"))
    print(i)

lista_ementas_sc = [k for k in lista_ementas if "ordinaria" in k]
lista_ementas_sc = [k.replace("q=2016", "").replace("/sc/lei-ordinaria-n-", "").replace("-", " ") for k in lista_ementas_sc if "2016-santa-catarina" in k]


#9. Ementas copiadas direto direto pro excel
df_ementas = pd.read_csv("ementas.csv")

dict_ementas_geral = {}
for i in list(df_ementas.columns):
    dict_ementas_geral[i] = [k for k in list(df_ementas[i]) if str(k) != 'nan']
    print(i)

# incluindo as que peguei "scrapando"
dict_ementas_geral["MT"] = ementas_mt
dict_ementas_geral["PB"] = ementas_pb
dict_ementas_geral["PI"] = ementas_pi
dict_ementas_geral["AC"] = ementas_ac
dict_ementas_geral["AM"] = ementas_am
dict_ementas_geral["RO"] = ementas_ro
dict_ementas_geral["BA"] = lista_ementas_ba
dict_ementas_geral["SC"] = lista_ementas_sc