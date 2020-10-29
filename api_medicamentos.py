import streamlit as st
import pandas as pd
import numpy as np
import scipy
from scipy import stats
import pydeck as pdk


import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', 999)


data = pd.read_csv('./TA_PRECO_MEDICAMENTO.csv', sep = ';', encoding  = 'LATIN-1')


# Logo
from PIL import Image
img = Image.open("logo.jpg")
st.image(img,width=600)


st.sidebar.info('Essa API tem como objetivo orientar o consumidor sobre os preços dos medicamentos vendidos no Brasil com base na Lei nº 10.742/2003 onde a atribuição da CMED de autorizar preços de entrada, acompanhar o mercado e autorizar reajustes de preços dos medicamentos, nos limites permitidos pela Lei, a regulação do setor farmacêutico seria pautada no modelo de teto de preços')

add_selectbox = st.sidebar.selectbox(
    "Você sabia que os peços de medicamentos são pautadas no modelo de teto de preços por lei ?",("", "Sim", "Não"))

if add_selectbox == "Não":
	st.sidebar.info('As farmácias e drogarias, assim como laboratórios, distribuidores e importadores, não podem cobrar pelos medicamentos preço acima do permitido pela CMED. A lista de preços máximos permitidos para a venda de medicamentos é disponibilizada para consulta dos consumidores e é atualizada mensalmente.')

st.sidebar.success('https://www.gov.br/anvisa/pt-br')
    
img_2 = Image.open("anvisa.jpg")
st.sidebar.image(img_2,width=300)

st.sidebar.success('Última atualização dos dados: 13/10/2020, informações obtidas da ANVISA')


# Header/Subheader - como em HTML
st.header("API para consulta de preços de medicamentos")


# MultiSelect produto

produto = data['PRODUTO'].unique()
produto = sorted(produto)
medicamento = st.selectbox("Selecione o medicamento:", produto)

# MultiSelect tipo de produto

filtro = ['PRODUTO', 'APRESENTAÇÃO', 'LABORATÓRIO', 'TIPO DE PRODUTO (STATUS DO PRODUTO)', 'PMC 20%', 'PMC 18%', 'PMC 17,5%', 'PMC 17%', 'PMC 12%', 'PMC 0%']
produto_2 = data.filter(items = filtro)


ajuste = produto_2.loc[produto_2['PRODUTO'] == medicamento]
apresentacao = ajuste['APRESENTAÇÃO'].unique()
apresentacao = sorted(apresentacao)

tipo = st.selectbox("Selecione o item:", apresentacao)


# checkbox se o medicamento é generico

if st.checkbox('Generico'):
	generico = 'yes'
else:
	generico = 'no'


# MultiSelect tipo de laboratório

ajuste_2 = produto_2.loc[produto_2['PRODUTO'] == medicamento]
laboratorio = ajuste_2['LABORATÓRIO'].unique()
laboratorio = sorted(laboratorio)


tipo_2 = st.selectbox("Selecione o laboratório:", laboratorio)


# MultiSelect tipo de estados


estados = st.selectbox("Selecione o estado:", ('', 'ACRE', 'ALAGROAS', 'AMAPÁ', 'AMAZONAS', 'BAHIA', 'CEARÁ',
	                                                           'DISTRITO FEDEREAL', 'ESPÍRITO SANTO', 'GOIÁS', 'MARANHÃO',
	                                                           'MATO GROSSO', 'MATO GROSSO DO SUL', 'MINAS GERAIS', 'PARÁ',
	                                                           'PARAÍBA', 'PARANÁ', 'PERNABUNCO', 'PIAUÍ', 'RIO DE JANEIRO',
	                                                           'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDÔNIA', 
	                                                           'RORAIMA', 'SANTA CATARINA', 'SÃO PAULO', 'SERGIPE', 'TOCANTINS'))


# Variáveis dos preços dos medicamento por estados


icms_20 = ('RIO DE JANEIRO')
icms_18 = pd.DataFrame([['AMAZONAS, AMAPÁ, BAHIA, CEARÁ, MARANHÃO, MINAS GERAIS, PARAÍBA, PERNABUNCO, PIAUÍ, PARANÁ, RIO GRANDE DO NORTE, RIO GRANDE DO SUL, SERGIPE, SÃO PAULO, TOCANTINS']], columns = ['review'])
icms_17meio = ('RONDÔNIA')
icms_17 = pd.DataFrame([['ACRE, ALAGROAS, DISTRITO FEDEREAL, ESPÍRITO SANTO, GOIÁS, MATO GROSSO, MATO GROSSO DO SUL, PARÁ, RORAIMA, SANTA CATARINA']], columns = ['review'])
icms_12 = pd.DataFrame([['SÃO PAULO, MINAS GERAIS']], columns = ['review'])


ajuste_3 = ajuste.loc[ajuste['APRESENTAÇÃO'] == tipo]

 
# Funções

if st.button("Consultar"):

	def word_count(review, word):
		cont = 0
		review = review.upper()

		if word in review.upper():
			return review.count(word)
		else:
			return 0
		
	confirmacao_1 = icms_18['review'].apply(lambda x: word_count(x, estados))
	confirmacao_2 = icms_17['review'].apply(lambda x: word_count(x, estados))
	confirmacao_3 = icms_12['review'].apply(lambda x: word_count(x, estados))

	w = 0 
	for w in confirmacao_1:
		str(w)

	if w == 1:
		consulta_2 = ajuste_3['PMC 18%'].unique()
		for x in consulta_2:
			final_2 = 'R$' + x

		if generico == 'no':

			st.success('{} É o preço máximo que pode ser praticado pelo comércio varejista de medicamentos, ou seja, farmácias e drogarias, tendo em vista que este contempla tanto a margem de lucro como os impostos inerentes a esses tipos de comércio para o estado selecionado.'.format(final_2))
			st.success('A alíquota de ICMS 18% se refere aos estado de {}.'.format(estados))



	y = 0 
	for y in confirmacao_2:
		str(y)

	if y == 1:
		consulta_3 = ajuste_3['PMC 17%'].unique()
		for x in consulta_3:
			final_3 = 'R$' + x

		if generico == 'yes' or generico == 'no':

			st.success('{} É o preço máximo que pode ser praticado pelo comércio varejista de medicamentos, ou seja, farmácias e drogarias, tendo em vista que este contempla tanto a margem de lucro como os impostos inerentes a esses tipos de comércio para o estado selecionado.'.format(final_3))
			st.success('A alíquota de ICMS 17% se refere aos estado de {}.'.format(estados))


	z = 0
	for z in confirmacao_3:
		str(z)

		if z == 1 and generico == 'yes':
			consulta_4 = ajuste_3['PMC 12%'].unique()
			for x in consulta_4:
				final_4 = 'R$' + x

			if generico == 'yes':

				st.success('{} É o preço máximo que pode ser praticado pelo comércio varejista de medicamentos, a alíquota de ICMS 12% está relacionada com os medicamentos genéricos dos estados de SP e MG, ou seja, farmácias e drogarias, tendo em vista que este contempla tanto a margem de lucro como os impostos inerentes a esses tipos de comércio para o estado selecionado.'.format(final_4))
				

	if estados == icms_20:
		consulta = ajuste_3['PMC 20%'].unique()
		for x in consulta:
			final = 'R$' + x

		if generico == 'yes' or generico == 'no':

			st.success('{} É o preço máximo que pode ser praticado pelo comércio varejista de medicamentos, ou seja, farmácias e drogarias, tendo em vista que este contempla tanto a margem de lucro como os impostos inerentes a esses tipos de comércio para o estado selecionado.'.format(final))
			st.success('A alíquota de ICMS 20% se refere aos estado de {}.'.format(estados))



	if estados == icms_17meio:
		consulta_5 = ajuste_3['PMC 17,5%'].unique()
		for x in consulta_5:
			final_5 = 'R$' + x

		if generico == 'yes' or generico == 'no':

			st.success('{} É o preço máximo que pode ser praticado pelo comércio varejista de medicamentos, ou seja, farmácias e drogarias, tendo em vista que este contempla tanto a margem de lucro como os impostos inerentes a esses tipos de comércio para o estado selecionado.'.format(final_5))
			st.success('A alíquota de ICMS 17,5% se refere aos estado de {}.'.format(estados))


# mapa 

brasil = pd.DataFrame([[-15.83, -47.86]], columns = ['lat', 'lon'])
ac = pd.DataFrame([[-8.77, -70.55]], columns = ['lat', 'lon'])
al = pd.DataFrame([[-9.62, -36.82]], columns = ['lat', 'lon'])
am = pd.DataFrame([[-3.47, -65.10]], columns = ['lat', 'lon'])
ap = pd.DataFrame([[1.41, -51.77]], columns = ['lat', 'lon'])
ba = pd.DataFrame([[-13.29, -41.71]], columns = ['lat', 'lon'])
ce = pd.DataFrame([[-5.20, -39.53]], columns = ['lat', 'lon'])
df = pd.DataFrame([[-15.83, -47.86]], columns = ['lat', 'lon'])
es = pd.DataFrame([[-19.19, -40.34]], columns = ['lat', 'lon'])
go = pd.DataFrame([[-15.98, -49.86]], columns = ['lat', 'lon'])
ma = pd.DataFrame([[-5.42, -45.44]], columns = ['lat', 'lon'])
mt = pd.DataFrame([[-12.64, -55.42]], columns = ['lat', 'lon'])
ms = pd.DataFrame([[-20.51, -54.54]], columns = ['lat', 'lon'])
mg = pd.DataFrame([[-18.10, -44.38]], columns = ['lat', 'lon'])
pa = pd.DataFrame([[-3.79, -52.48]], columns = ['lat', 'lon'])
pb = pd.DataFrame([[-7.28, -36.72]], columns = ['lat', 'lon'])
pr = pd.DataFrame([[-24.89, -51.55]], columns = ['lat', 'lon'])
pe = pd.DataFrame([[-8.38, -37.86]], columns = ['lat', 'lon'])
pi = pd.DataFrame([[-6.60, -42.28]], columns = ['lat', 'lon'])
rj = pd.DataFrame([[-22.84, -43.15]], columns = ['lat', 'lon'])
rn = pd.DataFrame([[-5.81, -36.59]], columns = ['lat', 'lon'])
ro = pd.DataFrame([[-10.83, -63.34]], columns = ['lat', 'lon'])
rs = pd.DataFrame([[-30.17, -53.50]], columns = ['lat', 'lon'])
rr = pd.DataFrame([[1.99, -61.33]], columns = ['lat', 'lon'])
sc = pd.DataFrame([[-27.45, -50.95]], columns = ['lat', 'lon'])
se = pd.DataFrame([[-10.57, -37.45]], columns = ['lat', 'lon'])
sp = pd.DataFrame([[-23.55, -46.64]], columns = ['lat', 'lon'])
to = pd.DataFrame([[-9.46, -48.26]], columns = ['lat', 'lon'])


if estados == '':
	st.map(data=brasil, zoom=3)

if estados == 'ACRE':
	st.map(data=ac, zoom=6)

if estados == 'ALAGROAS':
	st.map(data=al, zoom=6)

if estados == 'AMAPÁ':
	st.map(data=ap, zoom=6)

if estados == 'AMAZONAS':
	st.map(data=am, zoom=6)

if estados == 'BAHIA':
	st.map(data=ba, zoom=6)

if estados == 'CEARÁ':
	st.map(data=ce, zoom=6)

if estados == 'DISTRITO FEDEREAL':
	st.map(data=df, zoom=6)

if estados == 'ESPÍRITO SANTO':
	st.map(data=es, zoom=6)

if estados == 'GOIÁS':
	st.map(data=go, zoom=6)

if estados == 'MARANHÃO':
	st.map(data=ma, zoom=6)

if estados == 'MATO GROSSO':
	st.map(data=mt, zoom=6)

if estados == 'MATO GROSSO DO SUL':
	st.map(data=ms, zoom=6)

if estados == 'MINAS GERAIS':
	st.map(data=mg, zoom=6)

if estados == 'PARÁ':
	st.map(data=pa, zoom=6)

if estados == 'PARAÍBA':
	st.map(data=pb, zoom=6)

if estados == 'PARANÁ':
	st.map(data=pr, zoom=6)

if estados == 'PERNABUNCO':
	st.map(data=pe, zoom=6)

if estados == 'PIAUÍ':
	st.map(data=pi, zoom=6)

if estados == 'RIO DE JANEIRO':
	st.map(data=rj, zoom=6)

if estados == 'RIO GRANDE DO NORTE':
	st.map(data=rn, zoom=6)

if estados == 'RIO GRANDE DO SUL':
	st.map(data=rs, zoom=6)

if estados == 'RONDÔNIA':
	st.map(data=ro, zoom=6)

if estados == 'RORAIMA':
	st.map(data=rr, zoom=6)

if estados == 'SANTA CATARINA':
	st.map(data=sc, zoom=6)

if estados == 'SÃO PAULO':
	st.map(data=sp, zoom=6)

if estados == 'SERGIPE':
	st.map(data=se, zoom=6)

if estados == 'TOCANTINS':
	st.map(data=to, zoom=6)




# Texto Area

message = st.text_area("Nos dê um feedback se as farmácias e drogarias do seu estado estão respeitando esses valores. ","Digite aqui..")
name = st.text_input('Deixe seu nome:')
email = st.text_input('Deixe seu Email:')

if st.button("Enviar"):
	st.success('Obrigado mensagem enviada com sucesso.')




