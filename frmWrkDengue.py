## IMPORTAÇÃO DAS DEPENDENCIAS ##

import os 
import xlrd
import fpdf
import math
import time
import folium
import datetime
import requests
import gspread
import urllib.parse
import numpy      as np
import pandas     as pd
import seaborn    as sns
import geopandas  as gpd
import matplotlib as mpl
import contextily as ctx
import adjustText as aT
import matplotlib.pyplot as plt

from sklearn.cluster       import DBSCAN
from sklearn.cluster       import KMeans
from folium                import plugins
from folium.plugins        import HeatMap
from folium.plugins        import HeatMapWithTime
from fpdf                  import FPDF
from requests              import get
from simpledbf             import Dbf5
from pygal.style           import Style
from scipy.spatial         import ConvexHull
from matplotlib            import rcParams
from sklearn.cluster       import KMeans
from matplotlib.lines      import Line2D
from pandas_ods_reader     import read_ods
from shapely.geometry      import Point
from sklearn.preprocessing import scale
from IPython.display       import SVG, display
from urllib.request        import Request, urlopen
from sklearn               import preprocessing, cluster

import warnings
warnings.filterwarnings('ignore')
    
## FUNÇÃO PARA CRIAÇÃO DO PROJETO ##
####################################
def criarProjeto(prjNome):

	parent_dir = prjNome + "/"

	if os.path.isdir(parent_dir):
		pass
	else:
		os.mkdir(parent_dir) 
	 
	path = os.path.join(parent_dir, "dbf/")

	if os.path.isdir(path):
		pass
	else: 	
		os.mkdir(path) 

	path = os.path.join(parent_dir, "graficos/")   

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path) 
	
	path = os.path.join(parent_dir, "mapas/") 

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path) 

	path = os.path.join(parent_dir, "relatorio/") 

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path) 

	path = os.path.join(parent_dir, "imagens/") 

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path)

	path = os.path.join(parent_dir, "shapeFile/") 

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path)

	path = os.path.join(parent_dir, "geocode/") 

	if os.path.isdir(path):
		pass
	else: 
		os.mkdir(path) 


	print("Projeto '% s' criado!" % parent_dir) 
####################################

## CLASSE PARA CRIAÇÃO Da GEOCODIFICACAO ##
###########################################
class GeoCodificacao():

	def preProcessamento(self):

		self.casosSCS[['Lat', 'Lon']] = self.casosSCS['COORD'].str.split(',', 1, expand=True)
		self.casosVA[['Lat', 'Lon']]  = self.casosVA['COORD'].str.split(',', 1, expand=True)

		self.casosSCS = self.casosSCS[self.casosSCS['Lat'].isnull() == False ]
		self.casosVA  = self.casosVA[self.casosVA['Lat'].isnull()   == False ]

		self.casosSCS['DT_NOTIFIC'] = self.casosSCS['DT_NOTIFIC'].apply(lambda x: x.strftime('%Y-%m-%d'))
		self.casosSCS['DT_SIN_PRI'] = self.casosSCS['DT_SIN_PRI'].apply(lambda x: x.strftime('%Y-%m-%d'))

		self.casosVA['DT_NOTIFIC'] = self.casosVA['DT_NOTIFIC'].apply(lambda x: x.strftime('%Y-%m-%d'))
		self.casosVA['DT_SIN_PRI'] = self.casosVA['DT_SIN_PRI'].apply(lambda x: x.strftime('%Y-%m-%d'))

	def __init__(self, diretorio):

		self.diretorio = diretorio

		self.casosSCS = pd.read_excel(self.diretorio + "geo_ref_SCS.xlsx")
		self.casosVA  = pd.read_excel(self.diretorio + "geo_ref_VA.xlsx") 

		self.preProcessamento()		

	def geoCodePlot(self, municipio):

		geometrySCS = [Point(xy) for xy in zip((self.casosSCS['Lon']).astype(float),(self.casosSCS['Lat']).astype(float))]
		geometryVA  = [Point(xy) for xy in zip((self.casosVA['Lon']).astype(float),(self.casosVA['Lat']).astype(float))]

		geo_dfSCS = gpd.GeoDataFrame(self.casosSCS,crs="EPSG:4326",geometry=geometrySCS)
		geo_dfVA  = gpd.GeoDataFrame(self.casosVA,crs="EPSG:4326",geometry=geometryVA)

		mapaSCS = folium.Map(location=[-29.71621641965267, -52.426850474074136], zoom_start=14)
		mapaVA  = folium.Map(location=[-29.613714319245297, -52.19315455544646], zoom_start=14)

		coordinatesSCS =[]
		coordinatesVA  =[]

		suspeitos_dengue_scs     = folium.FeatureGroup(name = 'Casos Notificados')
		confirmados_dengue_scs   = folium.FeatureGroup(name = 'Dengue Confirmados')
		n_confirmados_dengue_scs = folium.FeatureGroup(name = 'Casos Fechados não Cofirmados')
		casos_obito_scs          = folium.FeatureGroup(name = 'Casos Óbito')
		cura_scs                 = folium.FeatureGroup(name = 'Cura')

		suspeitos_dengue_va     = folium.FeatureGroup(name = 'Casos Notificados')
		confirmados_dengue_va   = folium.FeatureGroup(name = 'Dengue Confirmados')
		n_confirmados_dengue_va = folium.FeatureGroup(name = 'Casos Fechados não Cofirmados')
		casos_obito_va          = folium.FeatureGroup(name = 'Casos Óbito')
		cura_va                 = folium.FeatureGroup(name = 'Cura')

		raio = 300
		for la,lo in zip((self.casosSCS['Lat']).astype(float),(self.casosSCS['Lon']).astype(float)):
		      caso = self.casosSCS[(self.casosSCS['Lat'].astype(float) == la) & (self.casosSCS['Lon'].astype(float) == lo)] 
		      texto = str(caso['NM_LOGRADO'].values[0]) + ' n° ' + str(caso['NU_NUMERO'].values[0]) + ' <br> Semana Notificação (' + str(caso['SEM_NOT'].values[0]) + ')' + ' <br> Data Pri Sintomas (' + str(caso['DT_SIN_PRI'].values[0]) + ') <br> Data Notificação (' + str(caso['DT_NOTIFIC'].values[0]) + ')'
		      
		      if len(caso[caso['CLASSI_FIN'] == 10.0]) > 0 :
		          folium.Circle([la, lo],
		                    radius=raio
		                   ).add_to(confirmados_dengue_scs)
		          folium.Marker(
		              location=[la,lo],
		              icon=folium.Icon(color='red', icon='info-sign'),
		              popup=folium.Popup(texto,
		                                 max_width=200)
		          ).add_to(confirmados_dengue_scs)		         
		      elif len(caso[caso['CLASSI_FIN'] == 11.0]) > 0:
		          folium.Circle([la, lo],
		                    radius=raio
		                   ).add_to(casos_obito_scs)
		          folium.Marker(
		              location=[la,lo],
		              icon=folium.Icon(color='black', icon='info-sign'),
		              popup=folium.Popup(texto,
		                                 max_width=200)
		          ).add_to(casos_obito_scs)
		      else :
		          if caso['DT_ENCERRA'].isnull().values.any() :
		              folium.Circle([la, lo],
		                        radius=raio
		                       ).add_to(suspeitos_dengue_scs)
		              folium.Marker(
		                  location=[la,lo],
		                  icon=folium.Icon(color='blue', icon='info-sign'),
		                  popup=folium.Popup(texto,
		                                    max_width=200)
		              ).add_to(suspeitos_dengue_scs)
		          else:
		              folium.Circle([la, lo],
		                        radius=raio
		                       ).add_to(n_confirmados_dengue_scs)
		              folium.Marker(
		                  location=[la,lo],
		                  icon=folium.Icon(color='green', icon='info-sign'),
		                  popup=folium.Popup(texto,
		                                    max_width=200)
		              ).add_to(n_confirmados_dengue_scs)


		for la,lo in zip((self.casosVA['Lat']).astype(float),(self.casosVA['Lon']).astype(float)):
		      caso = self.casosVA[(self.casosVA['Lat'].astype(float) == la) & (self.casosVA['Lon'].astype(float) == lo)] 
		      texto = str(caso['NM_LOGRADO'].values[0]) + ' n° ' + str(caso['NU_NUMERO'].values[0]) + ' <br> Semana Notificação (' + str(caso['SEM_NOT'].values[0]) + ')' + ' <br> Data Pri Sintomas (' + str(caso['DT_SIN_PRI'].values[0]) + ') <br> Data Notificação (' + str(caso['DT_NOTIFIC'].values[0]) + ')'
		      
		      if len(caso[caso['CLASSI_FIN'] == 10.0]) > 0 :
		          folium.Circle([la, lo],
		                    radius=raio
		                   ).add_to(confirmados_dengue_va)
		          folium.Marker(
		              location=[la,lo],
		              icon=folium.Icon(color='red', icon='info-sign'),
		              popup=folium.Popup(texto,
		                                 max_width=200)
		          ).add_to(confirmados_dengue_va)
		      elif len(caso[caso['CLASSI_FIN'] == 11.0]) > 0:
		          folium.Circle([la, lo],
		                    radius=raio
		                   ).add_to(casos_obito_va)
		          folium.Marker(
		              location=[la,lo],
		              icon=folium.Icon(color='black', icon='info-sign'),
		              popup=folium.Popup(texto,
		                                 max_width=200)
		          ).add_to(casos_obito_va)
		      else :
		          if caso['DT_ENCERRA'].isnull().values.any() :
		              folium.Circle([la, lo],
		                        radius=raio
		                       ).add_to(suspeitos_dengue_va)
		              folium.Marker(
		                  location=[la,lo],
		                  icon=folium.Icon(color='blue', icon='info-sign'),
		                  popup=folium.Popup(texto,
		                                    max_width=200)
		              ).add_to(suspeitos_dengue_va)
		          else:
		              folium.Circle([la, lo],
		                        radius=raio
		                       ).add_to(n_confirmados_dengue_va)
		              folium.Marker(
		                  location=[la,lo],
		                  icon=folium.Icon(color='green', icon='info-sign'),
		                  popup=folium.Popup(texto,
		                                    max_width=200)
		              ).add_to(n_confirmados_dengue_va)

		suspeitos_dengue_scs.add_to(mapaSCS)
		confirmados_dengue_scs.add_to(mapaSCS)
		n_confirmados_dengue_scs.add_to(mapaSCS)
		casos_obito_scs.add_to(mapaSCS)
		cura_scs.add_to(mapaSCS)

		folium.LayerControl(collapsed = False).add_to(mapaSCS)

		suspeitos_dengue_va.add_to(mapaVA)
		confirmados_dengue_va.add_to(mapaVA)
		n_confirmados_dengue_va.add_to(mapaVA)
		casos_obito_va.add_to(mapaVA)
		cura_va.add_to(mapaVA)

		folium.LayerControl(collapsed = False).add_to(mapaVA)

		
		if municipio == 'SCS':
			mapaSCS.save(outfile = self.diretorio + "geocode_pontosSCS.html")
			return mapaSCS
		else:
			mapaVA.save(outfile  = self.diretorio + "geocode_pontosVA.html")
			return mapaVA
		
		

	def geoCodeHeatMap(self, municipio):

		coordinatesSCS =[]
		coordinatesVA  =[]

		for la,lo in zip((self.casosSCS['Lat']).astype(float),(self.casosSCS['Lon']).astype(float)):
			coordinatesSCS.append([la,lo])

		for la,lo in zip((self.casosVA['Lat']).astype(float),(self.casosVA['Lon']).astype(float)):
			coordinatesVA.append([la,lo])

		mPSCS = folium.Map([-29.71621641965267, -52.426850474074136], zoom_start=14, max_zoom=14)
		mPVA  = folium.Map([-29.613714319245297, -52.19315455544646], zoom_start=14)

		HeatMap(coordinatesSCS).add_to(mPSCS)
		HeatMap(coordinatesVA).add_to(mPVA)		

		mPSCS.save(outfile= self.diretorio + "geocodeSCSHM.html")	
		mPVA.save(outfile= self.diretorio + "geocodeVAHM.html")

		if municipio == 'SCS':
			return mPSCS
		else:
			return mPVA

	def geoCluster(self, municipio):

		k = 12
		cores = ['#000000','#483D8B','#00FFFF','#00FF7F','#B8860B','#DEB887','#FF00FF','#FF0000','#FF8C00','#FFD700','#FFE4E1','#FF1493']
		model = cluster.KMeans(n_clusters=k, init='k-means++')
		X = self.casosSCS[['Lat','Lon']]
		## clustering
		dtf_X = X.copy()
		dtf_X["cluster"] = model.fit_predict(X)
		## find real centroids
		df = pd.DataFrame(model.cluster_centers_, columns = ['Lat', 'Lon'])
		df['Id'] = list(range(len(df)))

		mapaSCS = folium.Map(location=[-29.71621641965267, -52.426850474074136], zoom_start=13, zoom_control=False, max_zoom=13)

		for la,lo,clus in zip((dtf_X['Lat']).astype(float),(dtf_X['Lon']).astype(float), dtf_X['cluster']):
			folium.CircleMarker(location=[la,lo],
				radius=6,
				color= cores[clus],
				weight=5
				).add_to(mapaSCS)   

		for la,lo,id in zip((df['Lat']).astype(float),(df['Lon']).astype(float),df['Id']):
			folium.Marker(
				location=[la,lo],
				icon=folium.plugins.BeautifyIcon(border_color='#FF8C00', background_color='#FF8C00',
				text_color='black',
				number=id,
				icon_shape='marker'),
				).add_to(mapaSCS)  

		
		if municipio == 'SCS':
			mapaSCS.save(outfile= self.diretorio + "geocodeSCSCluster.html")
			return mapaSCS	

	def geoClusterArea(self, municipio):

		k = 12
		cores = ['#000000','#483D8B','#00FFFF','#00FF7F','#B8860B','#DEB887','#FF00FF','#FF0000','#FF8C00','#FFD700','#FFE4E1','#FF1493']
		model = cluster.KMeans(n_clusters=k, init='k-means++')
		X = self.casosSCS[['Lat','Lon']]
		## clustering
		dtf_X = X.copy()
		dtf_X["cluster"] = model.fit_predict(X)
		## find real centroids
		df = pd.DataFrame(model.cluster_centers_, columns = ['Lat', 'Lon'])
		df['Id'] = list(range(len(df)))

		mapaSCS = folium.Map(location=[-29.71621641965267, -52.426850474074136], zoom_start=13, zoom_control=False, max_zoom=13)

		for la,lo,clus in zip((dtf_X['Lat']).astype(float),(dtf_X['Lon']).astype(float), dtf_X['cluster']):
			folium.CircleMarker(location=[la,lo],
				radius=6,
				color= cores[clus],
				weight=5
				).add_to(mapaSCS)   

		for la,lo,id in zip((df['Lat']).astype(float),(df['Lon']).astype(float),df['Id']):
			folium.Marker(
				location=[la,lo],
				icon=folium.plugins.BeautifyIcon(border_color='#FF8C00', background_color='#FF8C00',
				text_color='black',
				number=id,
				icon_shape='marker'),
				).add_to(mapaSCS)  

		for i in range(k):

			tmp_coord_cluster = []
			sub_set = dtf_X[dtf_X['cluster'] == i]

			for la,lo in zip((sub_set['Lat']).astype(float),(sub_set['Lon']).astype(float)):

				tmp_coord_cluster.append([la,lo])

			if (len(tmp_coord_cluster) > 2):

				b = [tmp_coord_cluster[i] for i in ConvexHull(tmp_coord_cluster).vertices]
				b.append(b[0])
				folium.PolyLine(b, color='red').add_to(mapaSCS)

		
		if municipio == 'SCS':
			mapaSCS.save(outfile= self.diretorio + "geocodeSCSClusterArea.html")
			return mapaSCS


###########################################

## CLASSE PARA CRIAÇÃO DOS MAPAS ##
###################################
class Mapas():

	def dadosMapa(self):

		map_df = gpd.read_file(self.shapeFile + 'RS_Municipios_2019.shp')

		return map_df

	def __init__(self, mapas, shapeFile, csv, anotacao=' '):

		self.mapas =  mapas
		self.shapeFile = shapeFile
		self.csv = csv	
		self.mapa_df = self.dadosMapa()
		self.str_semana = anotacao

	def mapaRs(self, dados):

		ax = dados.plot(figsize=(20, 10))
		ax.axis('off')

	def gisDengue(self):

		df = pd.read_csv(self.csv) 
		df['Ibge'] = df['Ibge'].astype(str)

		merged = self.mapa_df.set_index('CD_MUN').join(df.set_index('Ibge'))
		merged = merged.to_crs(epsg=3857)

		return merged

	def gisCasosSuspeitos(self, merged):

		merged_crs = merged[merged.Suspeito.notnull()]
		merged_crs["rep"] = merged_crs["geometry"].representative_point()
		merged_points = merged_crs.copy()
		merged_points.set_geometry("rep", inplace = True)

		vmin, vmax = 0, 300
		fig, ax = plt.subplots(1, figsize=(10, 10))
		ax.axis('off')
		
		ax.set_title('Casos Suspeitos', fontdict={'fontsize': '25', 'fontweight' : '4'})

		merged.plot(column='Suspeito', cmap='Reds', ax=ax, linewidth=0.8, figsize=(20, 6), edgecolor='black', alpha=0.5)
		ax.annotate(self.str_semana,xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

		texts = []

		for x, y, label in zip(merged_points.geometry.x, merged_points.geometry.y, merged_points["Suspeito"].astype(int)):

			texts.append(plt.text(x, y, label, color='black', fontsize = 12))

		aT.adjust_text(texts, force_points=0.3, force_text=0.8, expand_points=(1,1), expand_text=(1,1), 
                  arrowprops=dict(arrowstyle="-", color='grey', lw=0.5))

		ctx.add_basemap(ax)

		fig.savefig(self.mapas + 'suspeito_crs.jpeg', dpi=300)

	def municipiosInfestados(self, merged):

		merged_crs = merged[merged.Suspeito.notnull()]
		merged_crs["rep"] = merged_crs["geometry"].representative_point()
		merged_points = merged_crs.copy()
		merged_points.set_geometry("rep", inplace = True)

		vmin, vmax = 0, 300
		fig, ax = plt.subplots(1, figsize=(10, 10))

		ax.axis('off')
		str_semana = ' '
		ax.set_title('Municípios Infestados', fontdict={'fontsize': '25', 'fontweight' : '4'})

		merged.plot(column='Infestado', cmap='Reds', ax=ax, legend=True, categorical=True, linewidth=0.8, figsize=(20, 6), edgecolor='black', alpha=0.5)
		ax.annotate(self.str_semana,xy=(0.1, .08),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

		LegendElement = [
                    Line2D([0],[0],color='beige',lw=4,label='Não Infestado'),
                    Line2D([0],[0],color='brown',lw=4,label='Infestado'),
                    ]

		ax.legend(handles=LegendElement,loc='upper right')

		texts = []

		for x, y, label in zip(merged_points.geometry.x, merged_points.geometry.y, merged_points["Infestado"].astype(int)):

			texts.append(plt.text(x, y, "", fontsize = 8))

		aT.adjust_text(texts, force_points=0.3, force_text=0.8, expand_points=(1,1), expand_text=(1,1), 
                  arrowprops=dict(arrowstyle="-", color='grey', lw=0.5))

		ctx.add_basemap(ax)

		fig.savefig(self.mapas + 'infestado_crs.jpeg', dpi=300)

	def gisDistribuicaoCasos(self, merged):

		ax = merged.plot(column='Dengue', cmap='Blues', figsize=(20, 10), linewidth=0.2, edgecolor='black', scheme='User_Defined', k=6, classification_kwds={'bins':[5, 10, 40, 70, 100, 4000]}, legend=True)

		ax.axis('off')
		ax.get_legend().set_bbox_to_anchor((0., 0., 0.2, 0.2))

		leg = ax.get_legend()
		leg.get_texts()[0].set_text('até 5 casos')
		leg.get_texts()[1].set_text('5   - 10 casos')
		leg.get_texts()[2].set_text('11  - 40 casos')
		leg.get_texts()[3].set_text('41  - 70 casos')
		leg.get_texts()[4].set_text('70  - 100 casos')
		leg.get_texts()[5].set_text('101 - 4000 casos')
		leg.set_title('Casos confirmados dengue ')
###################################

## CLASSE PARA CRIAÇÃO DO RELATORIO ##
######################################
class Relatorio():

	def __init__(self, diretorioRelatorio):
		self.pdf = FPDF()		
		self.diretorioRelatorio = diretorioRelatorio	

	def cabecalho(self):
		self.pdf.image(self.diretorioRelatorio + "Aedes-Aegypti-1.png", 0, 0, 50, 30)
    
	def rodape(self):
		self.pdf.set_y(-15)
		self.pdf.set_font('Helvetica', 'I', 8)
		self.pdf.set_text_color(128)
		self.pdf.cell(0, 10, 'Page ' + str(self.pdf.page_no()), 0, 0, 'C')
    
	def titulo(self, title):
		self.pdf.set_font('Helvetica', 'b', 20)
		self.pdf.ln(0)
		self.pdf.write(5, 30*' ' + title)
		self.pdf.ln(10)

		self.pdf.set_font('Helvetica', '', 9)
		self.pdf.set_text_color(r=128,g=128,b=128)
		today = time.strftime("%d/%m/%Y")
		self.pdf.write(4, 67*' ' + 'Semana Epidemiológica ' + f'{today}')

		self.pdf.ln(10)

	def escrita(self, texto, distancia = 4):
		self.pdf.set_text_color(r=0,g=0,b=0)
		self.pdf.set_font('Helvetica', '', 12)

		self.pdf.write(distancia, texto)

	def salva(self, caminho, nome):
		self.pdf.output(caminho + nome + ".pdf", 'F')    

	def adicionaPagina(self):
		self.pdf.add_page()

	def inserirImagem(self, diretorio, tipo):

		if tipo == 'simplificado':

			self.pdf.ln(3)
			self.escrita("Circulação Viral___________________________________________________________________")
			self.pdf.ln(5)

			self.pdf.image(diretorio  + "casosNotificacoes.png", 7, 40, 200, 70)
			self.pdf.ln(5)

			self.pdf.image(diretorio  + "casosAbertos.png", 7, 115, 100, 70)
			self.pdf.ln(5)

			self.pdf.image(diretorio  + "casosSuspeitos.png", 114, 115, 100, 70)
			self.pdf.ln(5)

			self.pdf.ln(140)
			self.escrita("Presença Vetorial_________________________________________________________________")

			self.pdf.image(diretorio  + "Larvas.png", 20, 200, 170, 75)
			self.pdf.ln(5)			
######################################

## CLASSE PARA CRIAÇÃO DOS GRÁFICOS ##
######################################
class Grafico():

## TRATAMENTO DOS DADOS DA BASE .DBF ##

	def tratamentoDadosDbf(self):

		municipio = ["Candelaria","Gramado Xavier","Herveiras","Mato Leitao","Pantano Grande","Passo do Sobrado","Rio Pardo","Santa Cruz do Sul","Sinimbu","Vale do Sol","Vale Verde","Venancio Aires","Vera Cruz"]
		municipioID = ["430420","430915","430957","431215","431395","431407","431570","431680","432067","432253","432252","432260","432270"]

		for i in range(0,13):

			self.df['ID_MUNICIP']= np.where(((self.df['ID_MUNICIP']==municipioID[i])),municipio[i], self.df['ID_MUNICIP']) 
			self.df['ID_MN_RESI']= np.where(((self.df['ID_MN_RESI']==municipioID[i])),municipio[i], self.df['ID_MN_RESI'])

		self.df['TPAUTOCTO']= np.where(((self.df['TPAUTOCTO']=='1')),'Autoctone', self.df['TPAUTOCTO'])         
		self.df['TPAUTOCTO']= np.where(((self.df['TPAUTOCTO']=='2')),'Importado', self.df['TPAUTOCTO']) 

		self.df['EVOLUCAO']= np.where(((self.df['EVOLUCAO']=='1')),'Cura', self.df['EVOLUCAO'])         
		self.df['EVOLUCAO']= np.where(((self.df['EVOLUCAO']=='2')),'Obito pelo agravo', self.df['EVOLUCAO'])  
		self.df['EVOLUCAO']= np.where(((self.df['EVOLUCAO']=='3')),'Obito por outras causas', self.df['EVOLUCAO'])         
		self.df['EVOLUCAO']= np.where(((self.df['EVOLUCAO']=='4')),'Obito em investigacao', self.df['EVOLUCAO'])  
		self.df['EVOLUCAO']= np.where(((self.df['EVOLUCAO']=='9')),'Ignorado', self.df['EVOLUCAO'])    

		self.df['NM_BAIRRO'] = self.df['NM_BAIRRO'].str.replace(" ","\n")
		self.df['NM_LOGRADO'] = self.df['NM_LOGRADO'].str.replace(" ","\n")

		self.df['SEM_NOT'] = self.df['SEM_NOT'].str[4:]
		self.df['SEM_PRI'] = self.df['SEM_PRI'].str[4:]
		self.df['NU_IDADE_N']= np.where(((self.df['NU_IDADE_N'].astype(int) - 4000) < 0), self.df['NU_IDADE_N'], self.df['NU_IDADE_N'].astype(int) - 4000) 
		self.df['NU_IDADE_N']= np.where(((self.df['NU_IDADE_N'].astype(int) - 3000) < 0), self.df['NU_IDADE_N'], self.df['NU_IDADE_N'].astype(int) - 3000) 
		self.df['NU_IDADE_N']= np.where(((self.df['NU_IDADE_N'].astype(int) - 2000) < 0), self.df['NU_IDADE_N'], self.df['NU_IDADE_N'].astype(int) - 2000) 
		self.df['NU_IDADE_N']= np.where(((self.df['NU_IDADE_N'].astype(int) - 1000) < 0), self.df['NU_IDADE_N'], self.df['NU_IDADE_N'].astype(int) - 1000) 				  

## CONVERSÃO PARA O FORMATO DE DATA DO EXCEL ##
## FAZ PARTE DO TRATAMENTO DE DADOS DA BASE .XSLX ##

	def xldate_to_datetime(self, xldatetime):

		tempDate = datetime.datetime(1899, 12, 31)
		(days, portion) = math.modf(xldatetime)

		deltaDays = datetime.timedelta(days=days)
		secs = int(24 * 60 * 60 * portion)
		detlaSeconds = datetime.timedelta(seconds=secs)
		TheTime = (tempDate + deltaDays + detlaSeconds)

		return TheTime.strftime("%d-%m-%Y")

## CONVERTE LITERAL PARA INTEIRO ##
## FAZ PARTE DO TRATAMENTO DE DADOS DA BASE .XSLX ##

	def convertLiteralToInt(self, value):
		try:
			number = int(value)
		except ValueError:
			number = 0
		return number	

## TRATAMENTO DE DADOS DA BASE .XSLX ##
## LEITURA DO .XSLX PARA DATAFRAME ##

	def tratamentoDadosXslx(self):
			lista_dados = []

			workbook = xlrd.open_workbook(self.dbfVetor)
			worksheet = workbook.sheet_by_name('RELATORIODENGUE')
			num_rows = worksheet.nrows - 1
			curr_row = 0

			while curr_row < num_rows:
			      if isinstance(worksheet.cell(curr_row, 0).value,float):         
			          
			          lista_dados.append([self.xldate_to_datetime(worksheet.cell(curr_row, 0).value),
			                         worksheet.cell(curr_row, 1).value,
			                         worksheet.cell(curr_row, 2).value,
			                         worksheet.cell(curr_row, 3).value,
			                         self.xldate_to_datetime(worksheet.cell(curr_row, 4).value),
			                         worksheet.cell(curr_row, 5).value,
			                         self.xldate_to_datetime(worksheet.cell(curr_row, 6).value),
			                         worksheet.cell(curr_row, 7).value,
			                         worksheet.cell(curr_row, 8).value,
			                         worksheet.cell(curr_row, 9).value,
			                         self.convertLiteralToInt(worksheet.cell(curr_row, 10).value),
			                         worksheet.cell(curr_row, 11).value,
			                         worksheet.cell(curr_row, 12).value,
			                         worksheet.cell(curr_row, 13).value,
			                         worksheet.cell(curr_row, 14).value,
			                         worksheet.cell(curr_row, 15).value,
			                         worksheet.cell(curr_row, 16).value,
			                         worksheet.cell(curr_row, 17).value,
			                         worksheet.cell(curr_row, 18).value,
			                         worksheet.cell(curr_row, 19).value,
			                         worksheet.cell(curr_row, 20).value,
			                         worksheet.cell(curr_row, 21).value,
			                         worksheet.cell(curr_row, 22).value,
			                         worksheet.cell(curr_row, 23).value,
			                         worksheet.cell(curr_row, 24).value, 
			                         worksheet.cell(curr_row, 25).value, 
			                         worksheet.cell(curr_row, 26).value, 
			                         worksheet.cell(curr_row, 27).value, 
			                         worksheet.cell(curr_row, 28).value, 
			                         worksheet.cell(curr_row, 29).value, 
			                         worksheet.cell(curr_row, 30).value, 
			                         worksheet.cell(curr_row, 31).value, 
			                         worksheet.cell(curr_row, 32).value, 
			                         worksheet.cell(curr_row, 33).value, 
			                         worksheet.cell(curr_row, 34).value, 
			                         worksheet.cell(curr_row, 35).value, 
			                         worksheet.cell(curr_row, 36).value, 
			                         worksheet.cell(curr_row, 37).value, 
			                         worksheet.cell(curr_row, 38).value, 
			                         worksheet.cell(curr_row, 39).value,                     
			                         ])
			      curr_row += 1


			dfSCS=pd.DataFrame(lista_dados,columns=['DATA',                        
			                                     'CRS',
			                                     'MUNICIPIO',
			                                     'LOCALIDADE',
			                                     'DCOLETA',
			                                     'SE',
			                                     'DENTRADA',
			                                     'FIA',
			                                     'NAMOSTRAS',
			                                     'IMOVEISAEAELARVAS',
			                                     'NUMEROAEAELARVAS',
			                                     'IMOVEISAEAEPUPAS',
			                                     'NUMEROAEAEPUPAS',
			                                     'IMOVEISAEAEADULTOS',
			                                     'NUMEROAEAEADULTOS',
			                                     'IMOVEISAEALLARVAS',
			                                     'NUMEROAEALLARVAS',
			                                     'IMOVEISAEALPUPAS',
			                                     'NUMEROAEALPUPAS',
			                                     'IMOVEISAEALADULTOS',
			                                     'NUMEROAEALADULTOS',
			                                     'IMOVEISOULARVAS',
			                                     'NUMEROOULARVAS',
			                                     'IMOVEISOUPUPAS',
			                                     'NUMEROOUPUPAS',
			                                     'IMOVEISOUADULTOS',
			                                     'NUMEROOUADULTOS',
			                                     'IMOVEISANLARVAS',
			                                     'NUMEROANLARVAS',
			                                     'IMOVEISANPUPAS',
			                                     'NUMEROANPUPAS',
			                                     'IMOVEISANADULTOS',
			                                     'NUMEROANADULTOS',
			                                     'IMOVEISNCULILARVAS',
			                                     'NUMERONCULILARVAS',
			                                     'IMOVEISNCULIPUPAS',
			                                     'NUMERONCULIPUPAS',
			                                     'IMOVEISNCULIADULTOS',
			                                     'NUMERONCULIADULTOS',
			                                     'MII'])
			return dfSCS

## INICILIZA A CLASSE GRAFICO ##
## INICILIZA A PERSISITENCIA DO CAMINHO DO DIRETORIO E DA LEITURA DAS BASES DE DADOS ##

	def __init__(self, nomeDiretorio):		

		dbf = Dbf5(os.getcwd() + '/' + nomeDiretorio + '/dbf/Dengue.dbf', codec='cp1250')

		self.dbfVetor = os.getcwd() + '/' + nomeDiretorio + '/dbf/relatoriodengue.xls'
		self.diretorio = os.getcwd() + '/' + nomeDiretorio + '/graficos/'
		self.diretorioRelatorio = os.getcwd() + '/' + nomeDiretorio + '/relatorio/'
		self.diretorioMapas = os.getcwd() + '/' + nomeDiretorio + '/mapas/'
		self.diretorioShapeFile = os.getcwd() + '/' + nomeDiretorio + '/shapeFile/'
		self.diretorioCsv = os.getcwd() + '/' + nomeDiretorio + '/dbf/gis_dengue.csv'
		self.diretorioGeoCode = os.getcwd() + '/' + nomeDiretorio + '/geocode/'
		
		self.df = dbf.to_dataframe() 
		self.dfSCS = self.tratamentoDadosXslx()
		self.tratamentoDadosDbf()

		print("Dataframe criado e dados tratados prontos para uso.")
		print("Caso deseje utilizar outro caminho para a base de dados utilize a função [criaConjuntoDados('caminho')].")
		print("O atributo caminho refere-se ao caminho a partir da pasta atual.")

## RETORNA O DATAFRAME REFENRETE AOS DADOS DA BASE .DBF ##

	def getDados():

		return self.df

## CRIA O DATAFRAME A PARTIR DE OUTRO CAMINHO PARA A BASE DE DADOS .DBF QUE NÃO O CAMINHO PADRÃO ##

	def criaConjuntoDados(caminhoDados):

		dbf = Dbf5(caminhoDados + '/Dengue.dbf', codec='cp1250')

		self.df = dbf.to_dataframe() 

## GERA O GRAFICO DOS CASOS SUSPEITOS DE DENGUE. CORRESPONDE AS INVESTIGAÇÕES ABERTAS ##

	def casosSuspeitos(self, xLabel,yLabel,cor='#4169E1', pAlpha=0.5):

		plt.figure(figsize=(9,5))
		sns.set(style="darkgrid")

		try:
			ax = sns.countplot(self.df["ID_MN_RESI"], order = self.df["ID_MN_RESI"].value_counts().index, palette=[cor], alpha = pAlpha)
			i=0

			for p in ax.patches:
				height = p.get_height()
				ax.text(p.get_x()+p.get_width()/2., height + 0.2,
				s = '{:.0f}'.format(height),ha="center", color = cor)
				i += 1

			plt.title('Casos Suspeitos', fontweight="bold")
			plt.xticks(rotation=45) 
			plt.xlabel(xLabel)
			plt.ylabel(yLabel)			
			plt.savefig(self.diretorio + 'casosSuspeitos.png')  

		except:
			return "Não foi possível plotar gráfico [casosSuspeitos]"

## GERA O GRAFICO DOS CASOS CONFIRMADOS DE DENGUE. CORRESPONDE AS INVESTIGAÇÕES FECHADAS ##

	def casosConfirmados(self, xLabel,yLabel,cor='#4169E1', pAlpha=0.5):

		confirmados = self.df["ID_MN_RESI"]

		plt.figure(figsize=(9,5))
		sns.set(style="darkgrid")

		try:

			ax = sns.countplot(confirmados, order = confirmados.value_counts().index, palette=[cor], alpha = pAlpha)
			i=0

			for p in ax.patches:
				height = p.get_height()
				ax.text(p.get_x()+p.get_width()/2., height + 0.2,
				s = '{:.0f}'.format(height),ha="center", color = cor)
				i += 1

			plt.title('Casos Confirmados', fontweight="bold")
			plt.xticks(rotation=45) 
			plt.xlabel(xLabel)
			plt.ylabel(yLabel)			
			plt.savefig(self.diretorio + 'casosConfirmados.png')  

		except:

			return "Não foi possível plotar gráfico [casosConfirmados]"

## GERA O GRAFICO DOS CASOS ABERTOS DE DENGUE. INFORMA SOBRE OS CASOS PENDENTES, SEM DEFINIÇÃO E NÃO ENCERRADOS ##

	def casosAbertos(self, xLabel,yLabel,cor='#4169E1', pAlpha=0.5):

		notificacao = self.df[self.df['DT_ENCERRA'].isna()]

		if(len(notificacao) != 0):

			plt.figure(figsize=(9,5))
			sns.set(style="darkgrid")

			try:
				ax = sns.countplot(notificacao["ID_MN_RESI"], order = notificacao["ID_MN_RESI"].value_counts().index, palette=[cor], alpha = pAlpha)
				i=0

				for p in ax.patches:
					height = p.get_height()
					ax.text(p.get_x()+p.get_width()/2., height + 0.2,
					s = '{:.0f}'.format(height),ha="center", color = cor)
					i += 1

				plt.title('Casos Abertos', fontweight="bold")
				plt.xticks(rotation=45) 
				plt.xlabel(xLabel)
				plt.ylabel(yLabel)			
				plt.savefig(self.diretorio + 'casosAbertos.png')  

			except:
				return "Não foi possível plotar gráfico [casosAbertos]"

## GERA O GRAFICO DOS CASOS CONFIRMADOS DE DENGUE POR SEMANA EPIDEMIOLÓGICA. RETRATA A EVOLUÇAO DOS CASOS ##

	def casosConfirmadosSE(self, xLabel,yLabel, cor='#4169E1'):

		confirmadosSE = self.df[self.df['CLASSI_FIN'] == '10']

		dengue = confirmadosSE.sort_values(by='SEM_NOT')

		plt.figure(figsize=(15,5))
		sns.set(style="darkgrid")

		try:      
			ax = sns.histplot(data=dengue, x=dengue['SEM_NOT'], kde=True)
			i=0

			for p in ax.patches:
				height = p.get_height()
				ax.text(p.get_x()+p.get_width()/2., height + 0.2,
				s = '{:.0f}'.format(height),ha="center", color = cor)
				i += 1

			plt.title('Casos Confirmados SE', fontweight="bold")			
			plt.xlabel(xLabel)
			plt.ylabel(yLabel)			
			plt.savefig(self.diretorio + 'casosConfirmadosSE.png')  

		except:
			return "Não foi possível plotar gráfico [casosConfirmadosSE]"

## GERA O GRAFICO DOS CASOS NOTIFICADOS DE DENGUE. RETRATA AS INVESTIGACOES ABERTAS ##

	def casosNotificacoes(self, xLabel,yLabel, cor='#4169E1', pAlpha=0.5):

		notificacao = self.df.sort_values(by='SEM_NOT')

		plt.figure(figsize=(15,5))
		sns.set(style="darkgrid")

		try:
			ax = sns.histplot(x=notificacao['SEM_NOT'], data=notificacao, palette=[cor], alpha = pAlpha, kde=True)
			i=0

			for p in ax.patches:
				height = p.get_height()
				ax.text(p.get_x()+p.get_width()/2., height + 0.2,
				s = '{:.0f}'.format(height),ha="center", color = cor)
				i += 1

			plt.title('Casos Notificações', fontweight="bold")			
			plt.xlabel(xLabel)
			plt.ylabel(yLabel)			
			plt.savefig(self.diretorio + 'casosNotificacoes.png')  

		except:
			return "Não foi possível plotar gráfico [casosNotificacoes]"

## GERA O GRAFICO DOS CASOS ABERTOS POR SEMANA EPIDEMIOLOGICA. RETRATA A EVOLUCAO DOS CASOS AINDA NAO ENCERRADOS ##

	def casosAbertosSE(self, xLabel, yLabel, cor='#4169E1', pAlpha=0.5):

		abertosSE = self.df[self.df['DT_ENCERRA'].isna()]

		dengue = abertosSE.sort_values(by='SEM_NOT')

		if (len(dengue) != 0):

			plt.figure(figsize=(15,5))
			sns.set(style="darkgrid")

			try:
				ax = sns.histplot(data=dengue, x=dengue['SEM_NOT'], alpha = pAlpha, kde=True)
				i=0

				for p in ax.patches:
					height = p.get_height()
					ax.text(p.get_x()+p.get_width()/2., height + 0.2,
					s = '{:.0f}'.format(height),ha="center", color = cor)
					i += 1

				plt.title('Casos Abertos SE', fontweight="bold")				
				plt.xlabel(xLabel)
				plt.ylabel(yLabel)			
				plt.savefig(self.diretorio + 'casosAbertosSE.png')  


			except:
				return "Não foi possível plotar gráfico [casosAbertosSE]"

	def Relatorio():
		pass

## RETORNA A LISTAGEM DE LARVAS DO VETOR POR MUNICIPIO. ##

	def listagemMunicipio(self):
		larvas = []

		for municipios in self.dfSCS['MUNICIPIO'].unique().tolist():

			municipio = self.dfSCS[self.dfSCS['MUNICIPIO'] == municipios]

			for ses in municipio['SE'].unique().tolist():

				se = municipio[municipio['SE'] == ses]

				larvas.append([municipios,ses,int(se['NUMEROAEAELARVAS'].sum())])

				dflarvas=pd.DataFrame(larvas,columns=['MUNICIPIO','SE','LARVAS'])

		return dflarvas

## GERA O GRAFICO DA EVOLUCAO DE LARVAS COLETADAS DAS ATIVIDADES DE CAMPO PARA MUNICIPIOS DETERMINADOS. ##

	def larvasMunicipio(self, municipio):

	    dflarvas = self.listagemMunicipio()
	    dfSCS_SCS = dflarvas[dflarvas['MUNICIPIO'] == municipio]

	    fig = plt.figure(figsize=(10,5))
	    sns.set(style="darkgrid")
	    ax = fig.add_axes([0,0,1,1])

	    plt.title('Santa Cruz do Sul', fontweight="bold")
	    plt.ylabel('Qtd Larvas Aedes Aegypti Coletadas')
	    plt.xlabel('Semana Epidemiológica')

	    ax.bar(dfSCS_SCS['SE'],dfSCS_SCS['LARVAS'], alpha=0.5)

	    plt.savefig(self.diretorio + 'Larvas.png', bbox_inches='tight')

## RETORNA A LISTAGEM DAS LARVAS DO VETOR COLETADAS POR MUNICIPIO. ##

	def listagemBairrosMunicipios(self):

	    larvas = []

	    for municipios in self.dfSCS['MUNICIPIO'].unique().tolist():

	      municipio = self.dfSCS[self.dfSCS['MUNICIPIO'] == municipios]

	      for bairros in municipio['LOCALIDADE'].unique().tolist():
	        
	        bairro = municipio[municipio['LOCALIDADE'] == bairros]

	        for ses in bairro['SE'].unique().tolist():

	          se = bairro[bairro['SE'] == ses]

	          larvas.append([municipios, bairros, ses, int(se['NUMEROAEAELARVAS'].sum())])
	          dflarvas=pd.DataFrame(larvas,columns=['MUNICIPIO','BAIRRO','SE','LARVAS'])

	    return dflarvas

## GERA O GRAFICO DA EVOLUCAO DAS LARVAS DO VETOR COLETAS POR BAIRRO PARA MUNCICIPIOS ESPECIFICOS. ##

	def larvasBairros(self, municipio):

	    dflarvas = self.listagemBairrosMunicipios()
	    dfSCS_SCS = dflarvas[dflarvas['MUNICIPIO'] == municipio]

	    for bairro in dfSCS_SCS['BAIRRO'].unique().tolist(): 
	      dfSCS_SCS_BAIRRO = dfSCS_SCS[dfSCS_SCS['BAIRRO'] == bairro]
	      
	      fig = plt.figure(figsize=(10,5))
	      ax = fig.add_axes([0,0,1,1])
	      ax.bar(dfSCS_SCS_BAIRRO['SE'],dfSCS_SCS_BAIRRO['LARVAS'], alpha=0.5)
	      plt.title(bairro + ' :: Santa Cruz do Sul', fontweight="bold")
	      plt.ylabel('Qtd Larvas Aedes Aegypti Coletadas')
	      plt.xlabel('Semana Epidemiológica')
	      plt.savefig(self.diretorio + municipio + '_' + bairro + '_Larvas.png', bbox_inches='tight')

	def relatorio(self, tipo='simplificado', titulo='BOLETIM SIMPLIFICADO'):

		relatorio = Relatorio(self.diretorioRelatorio) 

		relatorio.adicionaPagina()
		relatorio.cabecalho()
		relatorio.titulo(titulo)
		relatorio.inserirImagem(self.diretorio, tipo)
		relatorio.rodape()
		relatorio.salva(self.diretorioRelatorio, titulo)	

	def acompanhamentoMapas(self):

		return Mapas(self.diretorioMapas, self.diretorioShapeFile, self.diretorioCsv)

	def geoCodificacao(self):

		return GeoCodificacao(self.diretorioGeoCode)
####################################      
