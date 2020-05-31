import csv
import numpy as np
from datetime import datetime

import plotly.graph_objects as go

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
			hover_text = f'{country} has {case} cases now.'
			hover_text += f'{cure} covered, {death} dead in total.'
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
date2, countrie2, lon2, lat2 = [], [], [], []
case2, cure2, death2 = [], [], []
hover_text2 = []
for i in range(len(dates)):
	if i < len(dates)-1:
		if dates[i] != dates[i+1]:
			date2.append(dates[a:i+1])
			countrie2.append(countries[a:i+1])
			lon2.append(lons[a:i+1])
			lat2.append(lats[a:i+1])
			case2.append(cases[a:i+1])
			cure2.append(cures[a:i+1])
			death2.append(deaths[a:i+1])
			hover_text2.append(hover_texts[a:i+1])
			a = i+1
	else:
		date2.append(dates[a:])
		countrie2.append(countries[a:])
		lon2.append(lons[a:])
		lat2.append(lats[a:])
		case2.append(cases[a:])
		cure2.append(cures[a:])
		death2.append(deaths[a:])
		hover_text2.append(hover_texts[a:])

# for index, column_header in enumerate(header_row):
# 	print(index, column_header)

fig = go.Figure()

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
				colorbar_title = 'Cases',
				),
			hovertext = hover_text2[k],
			),
		)

fig.data[0].visible = True

steps = []
for i in range(len(fig.data)):
	step = dict(
		method = 'update',
		args = [{'visible': [False] * len(fig.data)},
				{'title': 'Date: ' + f'{date2[i][0]}'}],
		label = f'{date2[i][0]}',)
	step['args'][0]['visible'][i] = True
	steps.append(step)

sliders = [dict(
	active = 0,
	currentvalue = {'prefix': 'Date: '},
	pad = {'t': 30},
	steps = steps
	)]

fig.update_layout(
	geo = dict(
		projection = dict(
			type = 'natural earth')
		),
	sliders = sliders,
	title = 'COVID-19 Map'
	)

fig.show()