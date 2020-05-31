import csv
from datetime import datetime

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

filename = 'data.csv'
with open(filename) as f:
	reader = csv.reader(f)
	header_row = next(reader)
	dates, countries, lons, lats = [], [], [], []
	cases, cures, deaths = [], [], []
	hover_texts = []
	for row in reader:
		current_date = datetime.strptime(row[0], '%Y-%m-%d').date()
		country = row[1]
		try:
			lon = float(row[5])
			lat = float(row[6])
			case = int(row[2])
			cure = int(row[3])
			death = int(row[4])
		except ValueError:
			print(f'Missing data for {current_date}')
		else:
			hover_text = f'{country} had {case} cases this day. '
			hover_text += f'{cure} covered, {death} dead.'
			if case > 0 and cure >= 0 and death >= 0:
				dates.append(current_date)
				countries.append(country)
				lons.append(lon)
				lats.append(lat)
				cases.append(case)
				cures.append(cure)
				deaths.append(death)
				hover_texts.append(hover_text)

a = 0
date2, countries2, lon2, lat2 = [], [], [], []
case2, cure2, death2 = [], [], []
hover_text2 = []
trends = {}
for i in range(len(dates)):
	c = countries[i]
	if c in trends:
		trends[c][0].append(dates[i])
		trends[c][1].append(cases[i])
		trends[c][2].append(cures[i])
		trends[c][3].append(deaths[i])		
	else:
		trends[c] = [[],[],[],[]]
		trends[c][0].append(dates[i])
		trends[c][1].append(cases[i])
		trends[c][2].append(cures[i])
		trends[c][3].append(deaths[i])

	if i < len(dates)-1:
		if dates[i] != dates[i+1]:
			date2.append(dates[a:i+1])
			countries2.append(countries[a:i+1])
			lon2.append(lons[a:i+1])
			lat2.append(lats[a:i+1])
			case2.append(cases[a:i+1])
			cure2.append(cures[a:i+1])
			death2.append(deaths[a:i+1])
			hover_text2.append(hover_texts[a:i+1])
			a = i+1
	else:
		date2.append(dates[a:])
		countries2.append(countries[a:])
		lon2.append(lons[a:])
		lat2.append(lats[a:])
		case2.append(cases[a:])
		cure2.append(cures[a:])
		death2.append(deaths[a:])
		hover_text2.append(hover_texts[a:])

# for index, column_header in enumerate(header_row):
# 	print(index, column_header)

fig = make_subplots(
	rows = 2, cols = 3,
	row_heights = [0.7, 0.3],
	specs = [[{'type': 'scattergeo', 'colspan': 3}, None, None],
			 [{'type': 'bar'}, {'type': 'scatter', 'colspan': 2}, None]],
	# subplot_titles = (None,'Countries with most cases'),
	)
colors = ['firebrick', 'forestgreen', 'slateblue']

for k in range(len(case2)):
	fig.add_trace(
		go.Scattergeo(
			visible = False,
			lat = lat2[k],
			lon = lon2[k],
			showlegend = False,
			marker = dict(
				size = 3 * np.log2(case2[k]),
				color = case2[k],
				cmax = max(case2[k]),
				colorscale = 'Viridis',
				reversescale = True,
				opacity = 0.7,
				colorbar_len = 0.5,
				colorbar_xanchor = 'right',
				colorbar_yanchor = 'bottom',
				colorbar_title = 'Cases',
				),
			hoverinfo = 'text',
			hovertext = hover_text2[k],
		),
		row = 1,
		col = 1,
	)

	countries3 = []
	cases3 = []
	cures3 = []
	deaths3 = []
	c1 = case2[k][:]
	c2 = countries2[k][:]
	c3 = cure2[k][:]
	d3 = death2[k][:]
	for i in range(8):
		if c1:
			m_c = max(c1)
			if m_c > 0:
				index = c1.index(m_c)
				country = c2[index]
				cure = c3[index]
				death = d3[index]
				countries3.append(country)
				cases3.append(m_c)
				cures3.append(cure)
				deaths3.append(death)
				del c1[index]
				del c2[index]
				del c3[index]
				del d3[index]

	fig.add_trace(
		go.Bar(
			visible = False,
			showlegend = False,
			x = countries3, y = cases3,
			hoverinfo = 'text',
			hovertext = ['Cases: ' + f'{case}' for case in cases3]
		),
		row = 2,
		col = 1,
	)

	fig.add_trace(
		go.Bar(
			visible = False,
			showlegend = False,
			x = countries3, y = cures3,
			hoverinfo = 'text',
			hovertext = ['Cures: ' + f'{cure}' for cure in cures3]
		),
		row = 2,
		col = 1,
	)

	fig.add_trace(
		go.Bar(
			visible = False,
			showlegend = False,
			x = countries3, y = deaths3,
			hoverinfo = 'text',
			hovertext = ['Deaths: ' + f'{death}' for death in deaths3]
		),
		row = 2,
		col = 1,
	)

	day_trend = [cases3, cures3, deaths3]
	for k2 in range(3):
		fig.add_trace(
			go.Scatter(
				visible = False,
				showlegend = False,
				x = trends[countries3[0]][0],
				y = trends[countries3[0]][k2+1],
				marker = dict(
					color = colors[k2]),
				mode = 'lines',
				hoverinfo = 'y',
			),
			row = 2,
			col = 2,
		)

		fig.add_trace(
			go.Scatter(
				visible = False,
				showlegend = False,
				x = [date2[k][0]],
				y = [day_trend[k2][0]],
				marker = dict(
					# symbol = 8,
					size = 12,
					opacity = 0.6,
					color = colors[k2]),
				mode = 'markers',
				hoverinfo = 'text',
				hovertext = 'Here now.',
			),
			row = 2,
			col = 2,
		)

for i in range(10):
	fig.data[i].visible = True

steps = []
for i in range(len(case2)):
	step = dict(
		method = 'update',
		args = [{'visible': [False] * len(fig.data)},
				{'title': 'Date: ' + f'{date2[i][0]}'}],
		label = f'{date2[i][0]}',)
	for j in range(10):
		step['args'][0]['visible'][10*i+j] = True
	steps.append(step)

sliders = [dict(
	active = 0,
	currentvalue = {'prefix': 'Date: '},
	pad = {'t': 30},
	steps = steps,
)]

fig.update_layout(
	geo = dict(
		projection = dict(
			type = 'natural earth'),
		),
	sliders = sliders,
	barmode = 'group',
	title = 'COVID-19 Map'
	)

fig.show()