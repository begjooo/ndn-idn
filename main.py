import streamlit as st
import pandas as pd
import folium
import plotly.express as px
import math

from streamlit_folium import st_folium
from PIL import Image as img

KOOR_KOTA = 'dataset/koor_kota.csv'
FLOW_DTS = 'dataset/flow-dts.csv'
CONTENT_DTS = 'dataset/content-dts.csv'
LINK_DST = 'dataset/link-dts.csv'
PRO_DTS = 'dataset/pro-dts.csv'
CLI_DTS = 'dataset/cli-dts.csv'

st.set_page_config(layout = "wide")

st.write("""<h1 style="text-align:center">
	IDENTIFIKASI POPULARITAS KONTEN DAN KINERJA <i>NODES</i> NDN PADA JARINGAN IDN</h1>
	""", unsafe_allow_html = True)

def judul_sidebar():
	st.sidebar.write('''
		<p style="font-size:40px; color:grey"><b><i>Navigasi</i></b></p>
		''', unsafe_allow_html = True)

	# nyumputin hamburger menu (pojok kanan atas)
	#hide_menu_style = """
        #<style>
        	##MainMenu {visibility: hidden;}
        #</style>
        #"""
	#st.markdown(hide_menu_style, unsafe_allow_html=True)

# milih kota pake dropdownbox
def pilih_kota(df):
	st.sidebar.write('''
		# [Informasi Umum](#informasi-umum)
		''', unsafe_allow_html = True)

	df = df.set_index('kota', drop = False)
	daftar_kota = list(df['kota'])
	daftar_kota.sort()
	opsi = st.sidebar.selectbox('Pilih Kota', daftar_kota)
	kode = df['kode'][opsi]
	return kode

# ambil info kota
def info_kota(df, kode):
	kota = df['kota'][kode]
	kode = df['kode'][kode]
	lat = df['lat'][kode]
	lon = df['lon'][kode]

	st.header('Informasi Umum')

	col1, col2= st.columns(2)
	with col1:
		st.metric('Kota', '{}'.format(kota))
	with col2:
		st.metric('Lat, Lng', '{}, {}'.format(lat, lon))

# ambil data koor kota csv
def data_koor():
	df = pd.read_csv(KOOR_KOTA, delimiter = ';')
	kode = pilih_kota(df)
	df = df.set_index('kode', drop = False)
	info_kota(df, kode)
	peta(df, kode)

# atur link antar nodes
def	set_link(df, test_peta):
	bikin_link(df, test_peta, 'BNA', 'MDN')
	bikin_link(df, test_peta, 'BNA', 'MBO')
	bikin_link(df, test_peta, 'MBO', 'MDN')
	bikin_link(df, test_peta, 'SBG', 'MDN')
	bikin_link(df, test_peta, 'SBG', 'PAD')
	bikin_link(df, test_peta, 'MDN', 'PBR')
	bikin_link(df, test_peta, 'PAD', 'PBR')
	bikin_link(df, test_peta, 'PAD', 'LMP')
	bikin_link(df, test_peta, 'PBR', 'BTM')
	bikin_link(df, test_peta, 'PBR', 'PLG')
	bikin_link(df, test_peta, 'BTM', 'PGP')
	bikin_link(df, test_peta, 'PLG', 'LMP')
	bikin_link(df, test_peta, 'PLG', 'PGP')
	bikin_link(df, test_peta, 'LMP', 'JKT')
	bikin_link(df, test_peta, 'PGP', 'BTU')
	bikin_link(df, test_peta, 'PGP', 'JKT')
	bikin_link(df, test_peta, 'BTU', 'PTK')
	bikin_link(df, test_peta, 'BTU', 'JKT')
	bikin_link(df, test_peta, 'JKT', 'CBN')
	bikin_link(df, test_peta, 'JKT', 'BDG')
	bikin_link(df, test_peta, 'BDG', 'CBN')
	bikin_link(df, test_peta, 'BDG', 'YYK')
	bikin_link(df, test_peta, 'CBN', 'SMG')
	bikin_link(df, test_peta, 'YYK', 'SMG')
	bikin_link(df, test_peta, 'YYK', 'SBY')
	bikin_link(df, test_peta, 'SMG', 'SBY')
	bikin_link(df, test_peta, 'SBY', 'BJM')
	bikin_link(df, test_peta, 'SBY', 'MKS')
	bikin_link(df, test_peta, 'SBY', 'DPR')
	bikin_link(df, test_peta, 'SBY', 'MLG')
	bikin_link(df, test_peta, 'MLG', 'DPR')
	bikin_link(df, test_peta, 'PTK', 'BJM')
	bikin_link(df, test_peta, 'BJM', 'BPP')
	bikin_link(df, test_peta, 'BJM', 'MKS')
	bikin_link(df, test_peta, 'PAL', 'MND')
	bikin_link(df, test_peta, 'PAL', 'MKS')
	bikin_link(df, test_peta, 'PAL', 'BPP')
	bikin_link(df, test_peta, 'MKS', 'AMB')
	bikin_link(df, test_peta, 'MND', 'AMB')

# nambahin link
def bikin_link(df, test_peta, awal, akhir):
	lat_awal = df['lat'][awal]
	lon_awal = df['lon'][awal]
	lat_akhir = df['lat'][akhir]
	lon_akhir = df['lon'][akhir]

	tooltip = df['kode'][awal] + " - " + df['kode'][akhir]
	folium.PolyLine(
		[[lat_awal, lon_awal],
		[lat_akhir, lon_akhir]],
		tooltip = 'Link {} = {} ms'.format(tooltip, 15),
	).add_to(test_peta)

# ambil setengah data
def setengah_data_ke_atas(df, kolom):
	panjang = len(df)/2
	median = df[kolom].median()

	ambil_setengah = 0
	if panjang % 2 == 0:
		ambil_setengah = panjang - 1
	else:
		ambil_setengah = panjang - 1
		ambil_setengah = math.ceil(ambil_setengah)

	df_setengah = df.loc[(df[kolom] >= median)]
	df_setengah = df_setengah.truncate(before = 0, after = ambil_setengah)

	return df_setengah

# bikin pie chart di informasi umum > peta()
def g_pie_bagian_peta(kode, df, event, judul):
	list_paket = df.loc[(df.node == kode) &
		(df.event == event)]

	# filter interestin yg di-request user '/konten/'
	filter_list = list_paket[list_paket.prefix.str.contains('/konten/')]
	jml_paket_per_event = len(filter_list)

	# bikin konten jadi unique()
	paket_usr = list(filter_list.prefix.unique())

	jml_paket_per_konten = []
	for i in range(len(paket_usr)):
		jumlah = len(filter_list.loc[filter_list.prefix == paket_usr[i]])
		jml_paket_per_konten.append(jumlah)

	df_jml_paket = pd.DataFrame(zip(paket_usr, jml_paket_per_konten), columns = ['prefix', 'jumlah'])

	st.write(f"""<h4 style="text-align: center">{judul}</h4>""", unsafe_allow_html = True)
	
	signaling_true = st.checkbox('Paket Signaling', key = event)
	if signaling_true:
		# filter interestin utk signaling
		signaling = list_paket[~list_paket.prefix.str.contains('/konten/')]
		jml_sig_per_event = len(signaling)

		df_jml_paket = df_jml_paket.append(
			{'prefix':'signaling', 'jumlah':jml_sig_per_event},
			ignore_index = True)
	
	fig = px.pie(df_jml_paket, values = 'jumlah', names = 'prefix')
	fig.update_layout(legend_x = -0.3, legend_y = 0)
	st.plotly_chart(fig)

	if signaling_true:
		st.write("""
			<p>
			Total <i>'{}'</i> dari <i>User</i> : {}<br>
			Total Paket <i>Signaling</i> : {}
			</p>
			""".format(judul, jml_paket_per_event, jml_sig_per_event),
			unsafe_allow_html = True)
	else:
		st.write("""
			<p>
			Total <i>'{}'</i> dari <i>User</i> : {}<br>
			</p>
			""".format(judul, jml_paket_per_event),
			unsafe_allow_html = True)

# bikin kuartil 3
def kuartil3(kode, df, event, judul):
	list_paket = df.loc[(df.node == kode) &
		(df.event == event)]

	# filter interestin yg di-request user '/konten/'
	filter_list = list_paket[list_paket.prefix.str.contains('/konten/')]
	jml_paket_per_event = len(filter_list)

	# bikin konten jadi unique()
	paket_usr = list(filter_list.prefix.unique())

	jml_paket_per_konten = []
	for i in range(len(paket_usr)):
		jumlah = len(filter_list.loc[filter_list.prefix == paket_usr[i]])
		jml_paket_per_konten.append(jumlah)

	df_jml_paket = pd.DataFrame(zip(paket_usr, jml_paket_per_konten), columns = ['prefix', 'jumlah'])

	# sorting berdasarkan kolom
	konpop = df_jml_paket.sort_values(by = ['jumlah'], ascending=False)
	# reset index nya biar ngurut
	konpop = konpop.reset_index(drop = True)

	# kuartil 2
	konpop_q2 = setengah_data_ke_atas(konpop, 'jumlah')
	# kuartil 3
	konpop_q3 = setengah_data_ke_atas(konpop_q2, 'jumlah')
	
	st.write("""
		<br>
		""", unsafe_allow_html = True)
	st.write("""
		#### Konten Terpopuler @ {} :
		""".format(kode),
		unsafe_allow_html = True)
	for i in range(len(konpop_q3)):
		st.write('''
			<li> <a style="font-family:courier new">{}</a> @ {} <i>Request</i></li>
			'''.format(konpop_q3['prefix'][i], konpop_q3['jumlah'][i]),
			unsafe_allow_html = True)

# nampilin peta pake folium
def peta(df, kode):
	test_peta = folium.Map(location = [ -0.4834, 109.7878], zoom_start = 10,
		tiles = 'CartoDB dark_matter', zoom_control = False)

	# nambahin marker
	for i in range(0, len(df)):
		p_kota = df.iloc[i]['kota']
		p_latlon = str(df.iloc[i]['lat']) + ', ' + str(df.iloc[i]['lon'])
		folium.Marker(
			#radius = 20000,
			location = [df.iloc[i]['lat'], df.iloc[i]['lon']],
			#popup = p_kota + '\n' + p_latlon,
			tooltip = '[{}-site] {}'.format(df.iloc[i]['kode'], p_kota),
			fill = True,
			icon = folium.DivIcon(html = f"""
					<div style="
						widht: 50%;
						height: 100%;
						border: 1px solid white;
						border-radius: 100%;
						background: #e07d1b
					"></div>
					<div style="font-family:courier new; color: white"><b>{df.iloc[i]['kode']}</b></div>
				""")
		).add_to(test_peta)
	
	set_link(df, test_peta)
	
	# klik di peta nampilin lat lon
	#test_peta.add_child(folium.LatLngPopup())

	test_peta.fit_bounds([[-3.654703, 128.190643], [5.548290, 95.323753]],
		[5.548290, 95.323753],
		[-8.650000, 115.216667],
		max_zoom = 10)

	df_flow = pd.read_csv(FLOW_DTS, delimiter = ";")
	df_flow = df_flow.drop(columns = ['acc','cr','face','module','timestamp'])
	df_flow['node'] = df_flow['node'].str.upper()

	int_in = df_flow.loc[(df_flow.event == 'InterestIn') & (df_flow.node == kode)]
	int_out = df_flow.loc[(df_flow.event == 'InterestOut') & (df_flow.node == kode)]
	data_in = df_flow.loc[(df_flow.event == 'DataIn') & (df_flow.node == kode)]
	data_out = df_flow.loc[(df_flow.event == 'DataOut') & (df_flow.node == kode)]

	n_int_in = len(int_in)
	n_int_out = len(int_out)
	n_data_in = len(data_in)
	n_data_out = len(data_out)
	
	cola, colb = st.columns(2)
	with cola:
		st_map = st_folium(test_peta, height = 400)
	with colb:
		st.write('### <i>Nodes {}-site</i>'.format(kode), unsafe_allow_html = True)
		st.metric('Total Interest Masuk', '{}'.format(n_int_in))
		st.metric('Total Interest Keluar', '{}'.format(n_int_out))
		st.metric('Total Data Masuk', '{}'.format(n_data_in))
		st.metric('Total Data Keluar', '{}'.format(n_data_out))

	col1, col2 = st.columns(2)
	with col1:
		g_pie_bagian_peta(kode, df_flow, 'InterestIn', 'Interest Masuk')
		g_pie_bagian_peta(kode, df_flow, 'DataIn', 'Data Masuk')
	with col2:
		g_pie_bagian_peta(kode, df_flow, 'InterestOut', 'Interest Keluar')
		g_pie_bagian_peta(kode, df_flow, 'DataOut', 'Data Keluar')

	kuartil3(kode, df_flow, 'InterestIn', 'Interest Masuk')

# bikin kolom dan grafik line untuk bagian chr
def kolom_bagian_chr(df, teks):
	col_chr_1, col_chr_2 = st.columns(2)
	with col_chr_1:
		st.line_chart(df, height = 400)

	with col_chr_2:
		st.markdown("""
			<b><i>{}</i> Tertinggi per <i>Nodes</i></b>
			""".format(teks), unsafe_allow_html = True)
		max_val = df.max()
		df_max = pd.DataFrame(zip(max_val.index, df.idxmax(), max_val),
			columns = ['kota', 'konten', 'chr'])
		for i in range(len(df_max)):
			st.markdown("""<a1 style="font-size:14px">
				# <i>Nodes</i> {}
				: <a2 style="font-family:courier new">{}</a2>
				@ {:.3f}
				</a1>""".format(
					df_max['kota'][i],
					df_max['konten'][i],
					df_max['chr'][i])
				, unsafe_allow_html = True)

		st.markdown('<hr>', unsafe_allow_html = True)

		st.markdown("""
			<b><i>{}</i> Terendah per <i>Nodes</i></b>
			""".format(teks), unsafe_allow_html = True)
		min_val = df.min()
		df_min = pd.DataFrame(zip(min_val.index, df.idxmin(), min_val),
			columns = ['kota', 'konten', 'chr'])
		for i in range(len(df_max)):
			st.markdown("""<a1 style="font-size:14px">
				# <i>Nodes</i> {}
				: <a2 style="font-family:courier new">{}</a2>
				@ {:.3f}
				</a1>""".format(
					df_min['kota'][i],
					df_min['konten'][i],
					df_min['chr'][i])
				, unsafe_allow_html = True)

# bagian chr
def g_bagian_chr(df):
	nodes = df['kota'].unique()
	opsi = st.sidebar.multiselect('Pilih Nodes', nodes)
	konten = list(df.loc[opsi,'prefix'])

	# bikin 2d list untuk chr berdasarkan opsi
	list_chr = []
	for i in range(len(opsi)):
		list_chr.append(df.loc[opsi[i],'chr'].to_list())
	
	list_nhit = []
	for i in range(len(opsi)):
		list_nhit.append(df.loc[opsi[i],'nhit'].to_list())
	
	list_nmiss = []
	for i in range(len(opsi)):
		list_nmiss.append(df.loc[opsi[i],'nmiss'].to_list())

	# bikin dataset baru scr dinamis
	df_chr = pd.DataFrame()
	df_nhit = pd.DataFrame()
	df_nmiss = pd.DataFrame()

	for i in range(len(list_chr)):
		df_chr.insert(0, opsi[i], list_chr[i])
	for i in range(len(list_nhit)):
		df_nhit.insert(0, opsi[i], list_nhit[i])
	for i in range(len(list_nmiss)):
		df_nmiss.insert(0, opsi[i], list_nmiss[i])
	#st.write(df_chr)
	
	if len(opsi) == 0:
		st.markdown("""
			<h2>Tidak ada <i>input</i> ...</h2>
			Silahkan pilih <i>nodes</i> :
			""", unsafe_allow_html = True)
		st.code('Navigasi > Cache Hit Ratio (CHR) > Pilih Nodes')
	else:
		st.markdown("""
				<h3 style="text-align:center"><i>Cache Hit Ratio</i> (CHR)</h3>
			""", unsafe_allow_html = True)
		df_chr = df_chr.set_index(df['prefix'].unique())
		kolom_bagian_chr(df_chr, "Cache Hit Ratio")

		with st.expander("'nHits' dan 'nMisses'"):
			st.markdown("""<br>
					<h3 style="text-align:center"><i>Cache Hits</i> (<i>nHits</i>)</h3>
				""", unsafe_allow_html = True)
			df_nhit = df_nhit.set_index(df['prefix'].unique())
			kolom_bagian_chr(df_nhit, "nHits")

			st.markdown("""<br>
					<h3 style="text-align:center"><i>Cache Misses</i> (<i>nMisses</i>)</h3>
				""", unsafe_allow_html = True)
			df_nmiss = df_nmiss.set_index(df['prefix'].unique())
			kolom_bagian_chr(df_nmiss, "nMisses")

# grafik rata-rata chr
def grafik_rata_rata_chr(df, opsi_metrik):
	df_total = df.loc[:,['kota', opsi_metrik]]
	list_cli = df_total.index.unique()

	df_nilai = pd.DataFrame()
	for i in list_cli:
		df_tmp = df_total.loc[df_total.index == i]
		list_pilih = list(df_tmp[opsi_metrik][i])
		df_nilai.insert(0, i, list_pilih)

	rata_rata_metrik = []
	for i in range(len(df_nilai.columns)):
		rata_rata_metrik.append(df_nilai[df_nilai.columns[i]].mean())

	df_grafik = pd.DataFrame(zip(list(df_nilai.columns), rata_rata_metrik),
		columns = ['Nodes', 'Rata-Rata CHR'])
	df_grafik = df_grafik.set_index('Nodes')

	st.write("""<h3 style="text-align:center">Rata-Rata <i>{}</i> per <i>Nodes</i></h3>
		""".format('CHR'),
		unsafe_allow_html = True)

	col1, col2 = st.columns(2)
	with col1:
		# bikin grafiknya
		

		figbar = px.bar(df_grafik, x = df_grafik.index, y = 'Rata-Rata CHR')
		figbar.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
			xaxis_title = 'Nodes',
			yaxis_title = 'Rata-Rata',
			width = 500,
			#height = 430,
			margin = dict(l=40, r=0, t=20, b=50))
		st.plotly_chart(figbar)
	
	with col2:
		# nyari kuartil
		df_q = df_grafik.reset_index()
		df_q = df_q.sort_values(by = ['Rata-Rata CHR'],
			ascending = False).reset_index(drop = True)

		# Q2
		quartil_2 = df_q['Rata-Rata CHR'].median()
		
		# Q3
		stgh_atas = df_q.loc[df_q['Rata-Rata CHR'] >= quartil_2]
		quartil_3 = stgh_atas['Rata-Rata CHR'].median()

		# Q1
		stgh_bawah = df_q.loc[df_q['Rata-Rata CHR'] < quartil_2]
		quartil_1 = stgh_bawah['Rata-Rata CHR'].median()
		
		st.write('''Kuartil :
			<a style="font-family:courier new">
			Q1 = {:.4f} | Q2 = {:.4f} | Q3 = {:.4f}
			</a>'''.format(quartil_1, quartil_2, quartil_3),
			unsafe_allow_html = True)

		nodes_q4 = df_q.loc[(df_q['Rata-Rata CHR'] >= quartil_3)].reset_index(drop = True)
		nodes_q3 = df_q.loc[(df_q['Rata-Rata CHR'] >= quartil_2) & (df_q['Rata-Rata CHR'] < quartil_3)].reset_index(drop = True)
		nodes_q2 = df_q.loc[(df_q['Rata-Rata CHR'] >= quartil_1) & (df_q['Rata-Rata CHR'] < quartil_2)].reset_index(drop = True)
		nodes_q1 = df_q.loc[(df_q['Rata-Rata CHR'] < quartil_1)].reset_index(drop = True)

		st.write("""<a>
			<i>Nodes</i> dengan Kinerja <b>Terbaik</b> :
			</a>""", unsafe_allow_html = True)
		for i in range(len(nodes_q4)):
			st.write("""<a style="font-family:courier new">
				{}. {} @ {:.4f}
			</a>""".format(i + 1, nodes_q4.loc[i, 'Nodes'], nodes_q4.loc[i, 'Rata-Rata CHR']),
			unsafe_allow_html = True)

		st.write("<br>", unsafe_allow_html = True)

		nodes_q1_dcd = nodes_q1.sort_values(by = ['Rata-Rata CHR']).reset_index(drop = True)
		st.write("""<a>
			<i>Nodes</i> dengan Kinerja <b>Terburuk</b> :
			</a>""", unsafe_allow_html = True)
		for i in range(len(nodes_q1_dcd)):
			st.write("""<a style="font-family:courier new">
				{}. {} @ {:.4f}
			</a>""".format(i + 1, nodes_q1_dcd.loc[i, 'Nodes'], nodes_q1_dcd.loc[i, 'Rata-Rata CHR']),
		unsafe_allow_html = True)

# hitung chr per nodes
def cache_hit_ratio():
	# ambil data trafik
	st.sidebar.write('''
		# [<i>Cache Hit Ratio</i> (CHR)](#cache-hit-ratio-chr)
		''', unsafe_allow_html = True)
	df_cont = pd.read_csv(CONTENT_DTS, delimiter = ';')
	df_cont['kota'] = df_cont['kota'].str.upper()
	df_cont = df_cont.set_index(['kota', 'prefix'])
	cache_hit = []
	for i, j in df_cont.iterrows():
		nhits = df_cont['nhit'][i]
		nmiss = df_cont['nmiss'][i]
		itung = nhits/(nhits + nmiss)
		cache_hit.append(itung)

	df_cont['chr'] = cache_hit
	df_cont = df_cont.reset_index()
	df_cont = df_cont.set_index('kota', drop = False)

	st.markdown("<hr>", unsafe_allow_html = True)

	st.markdown("""
		## <i>Cache Hit Ratio</i> (CHR)
		<p>
			<i><b>Cache Hit Ratio</b></i> <b>(CHR)</b> merupakan perbandingan antara
			<b style="font-family: courier new">nHits</b> dengan
			<b style="font-family: courier new">total interest masuk</b>.
			<br>Semakin tinggi nilai CHR, maka semakin baik kinerja dari <i>nodes</i> NDN.
		</p>
		""", unsafe_allow_html = True)
	st.image(img.open('gambar/chr.png'), width = 300)
	st.markdown("""
		<ul>dimana:
		<li><b style="font-family: courier new">nHits</b> : Kejadian saat konten yang diminta <b>tersedia</b> di dalam <i>cache</i></li>
		<li><b style="font-family: courier new">nMisses</b> : Kejadian saat konten yang diminta <b>tidak tersedia</b> di dalam <i>cache</i></li>
		</ul>
		""", unsafe_allow_html = True)

	g_bagian_chr(df_cont)
	grafik_rata_rata_chr(df_cont, 'chr')

# bikin kolom dan grafik line untuk bagian client
def kolom_bagian_cli(df, metrik):
	col_chr_1, col_chr_2 = st.columns(2)
	with col_chr_1:
		st.line_chart(df, height = 400)

	with col_chr_2:
		st.markdown("""
			<b><i>{}</i> Tertinggi per <i>Nodes</i></b>
			""".format(metrik), unsafe_allow_html = True)
		max_val = df.max()
		df_max = pd.DataFrame(zip(max_val.index, df.idxmax(), max_val),
			columns = ['client', 'konten', metrik])
		for i in range(len(df_max)):
			st.markdown("""<a1 style="font-size:14px">
				# <i>Nodes</i> {}
				: <a2 style="font-family:courier new">{}</a2>
				@ {:.3f}
				</a1>""".format(
					df_max['client'][i],
					df_max['konten'][i],
					df_max[metrik][i])
				, unsafe_allow_html = True)

		st.markdown('<hr>', unsafe_allow_html = True)

		st.markdown("""
			<b><i>{}</i> Terendah per <i>Nodes</i></b>
			""".format(metrik), unsafe_allow_html = True)
		min_val = df.min()
		df_min = pd.DataFrame(zip(min_val.index, df.idxmin(), min_val),
			columns = ['client', 'konten', metrik])
		for i in range(len(df_max)):
			st.markdown("""<a1 style="font-size:14px">
				# <i>Nodes</i> {}
				: <a2 style="font-family:courier new">{}</a2>
				@ {:.3f}
				</a1>""".format(
					df_min['client'][i],
					df_min['konten'][i],
					df_min[metrik][i])
				, unsafe_allow_html = True)

# grafik rata-rata di client
def grafik_rata_rata_cli(df, opsi_metrik):
	df_total = df.loc[:,['konten', opsi_metrik]]
	list_cli = df_total.index.unique()

	df_nilai = pd.DataFrame()
	for i in list_cli:
		df_tmp = df_total.loc[df_total.index == i]
		list_pilih = list(df_tmp[opsi_metrik][i])
		df_nilai.insert(0, i, list_pilih)

	rata_rata_metrik = []
	for i in range(len(df_nilai.columns)):
		rata_rata_metrik.append(df_nilai[df_nilai.columns[i]].mean())
	
	df_grafik = pd.DataFrame(zip(list(df_nilai.columns), rata_rata_metrik),
		columns = ['Client', 'Rata-Rata ' + opsi_metrik])
	df_grafik = df_grafik.set_index('Client')

	# bikin grafiknya
	st.write("""<h5 style="text-align:center">Rata-Rata <i>{}</i> per <i>Client</i></h5>
		""".format(opsi_metrik),
		unsafe_allow_html = True)

	figbar = px.bar(df_grafik, x = df_grafik.index, y = 'Rata-Rata ' + opsi_metrik)
	figbar.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
		xaxis_title = 'Client',
		yaxis_title = 'Rata-Rata',
		width = 500,
		margin = dict(l=40, r=0, t=20, b=50))
	st.plotly_chart(figbar)

# data client
def data_cli():
	st.sidebar.write('# [Informasi <i>Client</i>](#informasi-client)'
		, unsafe_allow_html = True)
	st.markdown("""<hr>""", unsafe_allow_html = True)
	st.markdown("""
		<h2 style="text-align:center">Informasi <i>Client</i></h2>
		""", unsafe_allow_html = True)

	df = pd.read_csv(CLI_DTS, delimiter = ';')
	df['client'] = df['client'].str.upper()

	list_cli = list(df['client'].unique())

	df = df.set_index('client')

	df.rename(columns = {
		'sent':'Interest Sent',
		'nack':'Interest Nack',
		'loss':'Interest Loss',
		'avg_rtt':'Interest Average RTT (ms)'}, inplace = True)

	col1, col2 = st.columns(2)
	with col1:
		opsi_cli = st.multiselect('Pilih Client', list_cli)
		df_filter = df.loc[opsi_cli]
		konten = list(df_filter.loc[opsi_cli,'konten'])

	with col2:
		list_kolom = list(df_filter.columns)
		list_kolom.pop(0)
		opsi_metrik = st.selectbox('Pilih Metrik', list_kolom)

	# bikin 2d list untuk chr berdasarkan opsi
	list_metrik = []
	for i in range(len(opsi_cli)):
		list_metrik.append(df_filter.loc[opsi_cli[i], opsi_metrik].to_list())

	df_terpilih = pd.DataFrame()
	for i in range(len(list_metrik)):
		df_terpilih.insert(0, opsi_cli[i], list_metrik[i])

	if len(opsi_cli) == 0:
		st.markdown("""
			<h2>Tidak ada <i>input</i> ...</h2>
			Silahkan pilih <b><i>Node Client</i></b>
			""", unsafe_allow_html = True)
		st.markdown('<br>', unsafe_allow_html = True)
	else:
		df_terpilih = df_terpilih.set_index(df['konten'].unique())
		kolom_bagian_cli(df_terpilih, opsi_metrik)
	
	with st.expander("Rata-Rata 'Loss' dan 'Average RTT'"):
		col3, col4 = st.columns(2)
		with col3:
			grafik_rata_rata_cli(df,'Interest Loss')
		with col4:
			grafik_rata_rata_cli(df,'Interest Average RTT (ms)')

# data producer
def data_pro():
	st.sidebar.write('# [Informasi <i>Producer</i>](#informasi-producer)'
		, unsafe_allow_html = True)
	# ambil data pro-dts.csv
	df_pro = pd.read_csv(PRO_DTS, delimiter = ';')
	df_pro['producer'] = df_pro['producer'].str.upper()
	df_pro = df_pro.set_index('producer', drop = False)
	
	# list producernya -> bikin jadi unique() biar kebacanya 1
	list_producer = list(df_pro['producer'].unique())
	
	# hitung total interest yang diterima di tiap producer
	total_interest = []
	for i in list_producer:
		list_konten = list(df_pro.loc[i,'ninterestin'])
		test = 0
		for j in list_konten:
			test = test + j
		#st.write('Total Interest yang diterima oleh Producer ', i, 'sebanyak', test)
		total_interest.append(test)

	st.markdown("""<hr>""", unsafe_allow_html = True)

	st.markdown("""
				<h2 style="text-align:center">Informasi <i>Producer</i></h2><br>
			""", unsafe_allow_html = True)

	col1, col2 = st.columns(2)
	with col1:
		# bikin grafiknya
		st.write("""<h5 style="text-align: center">Total <i>Interest</i> Masuk per <i>Producer</i></h5>""",
			unsafe_allow_html = True)
		df_grafik = pd.DataFrame(zip(list_producer, total_interest),
		columns = ['producer','jml_interest'])
		fig = px.bar(df_grafik, x = 'producer', y = 'jml_interest')
		fig.update_layout(plot_bgcolor = 'rgba(0,0,0,0)',
			xaxis_title = '',
			yaxis_title = '',
			width = 500,
			margin = dict(l=40, r=0, t=0, b=50))
		st.plotly_chart(fig)
	with col2:
		st.write("""<h5 style="text-align: center">Jumlah <i>Interest</i> Masuk per Konten</h5>""",
			unsafe_allow_html = True)
		for i in list_producer:
			st.write('<h6># <i>Producer</i> {}</h6>'.format(i),
				unsafe_allow_html = True)
			df_konten = df_pro.loc[i,:]
			avg_konten = df_konten.ninterestin.mean()
			for j in range(len(df_konten)):
				pre = df_konten.iloc[j]['prefix']
				n_int = df_konten.iloc[j]['ninterestin']

				st.markdown("""<a1 style="font-size:14px">
					<a2 style="font-family:courier new">{}</a2>
					@ {} <i>Interest</i>
					</a1>"""
					.format(pre, n_int), unsafe_allow_html = True)
			st.write("""<a style="font-size:14px">
				Rata-Rata <i>Interest</i> per <i>Producer</i> @ <b>{} <i>Interest</i></b>
				</a>""".format(avg_konten), unsafe_allow_html = True)
			st.write("")

judul_sidebar()
data_koor()
cache_hit_ratio()
data_cli()
data_pro()
