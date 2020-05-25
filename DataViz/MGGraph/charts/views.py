from django.shortcuts import render, redirect
from django.contrib import messages

from bokeh.transform import transform
from bokeh.models import (ColumnDataSource, Plot,
                          Grid, HoverTool, LinearColorMapper)
from bokeh.models.widgets import Slider
from bokeh.models.callbacks import CustomJS
from bokeh.plotting import figure
from bokeh.layouts import column, gridplot
from bokeh.embed import components
from bokeh.transform import cumsum
from bokeh.palettes import inferno, viridis, cividis

import pandas as pd
import numpy as np
from numpy.random import random
from datetime import date
import timeit
from math import pi
from .mgcharts import mg_bar, mg_select, mg_slider


def time_function(function):
    def wrapper(*args, **kwargs):
        print(function.__name__, 'starting...')
        start = timeit.default_timer()
        result = function(*args, **kwargs)
        stop = timeit.default_timer()
        print(function.__name__, 'took:', stop - start, 'seconds')
        return result
    return wrapper


@time_function
def index(request):
    # Check that the request is POST type
    if request.method == 'POST':
        # Declare variables
        count = 0
        df_csv = pd.DataFrame()

        # Check that is compare charts
        if 'compare_charts' in request.POST:
            _list = []
            csv_files_compare = request.FILES.getlist('compareCharts')
            for csv in csv_files_compare:
                _list.append(csv.name)
            return redirect('graph_2', csv=_list[0], csv_2=_list[1])

        # Get csv coordenate file
        csv_coordenates = pd.read_csv(request.FILES['csvCoordenates'])

        # Loop through all file list
        csv_files = request.FILES.getlist('csvFile')
        for csv in csv_files:
            # Check if it is a csv file
            if not csv.name.endswith('.csv'):
                messages.error(
                    request,
                    'One of the file uploaded is not a cvs file: ' +
                    csv.name)
                continue

            # DataFrame csv
            df = pd.read_csv(csv)

            # Add row total
            col_list = list(df)
            col_list.remove('Time')
            df['sumTime'] = df[col_list].sum(axis=1)

            # Add csv id
            df.insert(0, 'id', count)

            # Add csv name
            df.insert(1, 'csvName', csv.name)

            # Add coordenates
            df.insert(1, 'coordX', csv_coordenates.iat[count, 0])
            df.insert(1, 'coordY', csv_coordenates.iat[count, 1])

            # Append csv to csvList
            df_csv = df_csv.append(df)

            count = count + 1

        # export csvList
        csv_name = request.POST.get(
            'experiment') + '_' + str(date.today()) + '.csv'
        df_csv.to_csv(csv_name)

        return redirect('graph', csv=csv_name)

    template = 'pages/index.html'
    return render(request, template)


def one_experiment(csv):
    # Get csv
    df = pd.read_csv(csv)

    # Get Data
    # Coordenates
    x = df['coordX'].unique()
    y = df['coordY'].unique()

    # csvList
    csvList = list(df['csvName'].unique())

    # Get csv Count
    sumtime = df.loc[df['Time'] == 1]
    countList = list(sumtime['sumTime'])

    # Get time Count
    time = df.loc[df['id'] == 1]

    # Get cvs time values in x Time
    timeList = []
    for i in range(len(time)):
        l = df.loc[df['Time'] == i + 1]
        lList = list(l['sumTime'])
        timeList.append(lList)

    # Scatter Graphic:
    # Colors
    N = len(sumtime['sumTime'])
    _x = random(size=N) * 100
    color_count = np.asarray(countList)
    colors = ["#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(
        50 + 2 * _x, (30 + 2 * (color_count / 100)))]

    # Data Source
    source = ColumnDataSource(dict(
        x=x,
        y=y,
        csv=csvList,
        count=countList,
        colors=colors))

    # Hover
    hover = HoverTool(tooltips=[
        ('csv', '@csv'),
        ('Total', '@count')
    ])

    scatter = figure(tools=[hover])

    scatter.scatter(x='x', y='y', size=16, source=source,
                    fill_color='colors', fill_alpha=0.7)

    # Bar Graph
    # Get Column List
    col_list = list(df)
    col_list.remove('id')
    col_list.remove('coordY')
    col_list.remove('coordX')
    col_list.remove('csvName')
    col_list.remove('Time')
    col_list.remove('sumTime')
    col_list.remove('Unnamed: 0')

    # Get df for first csv
    bar_initial = df.loc[df['id'] == 0]
    bar_initial = bar_initial[col_list]

    gene_list = []
    # Get list of gene values
    count_csv = len(df['id'].unique())
    for i in range(count_csv):

        # Get gene values for a single csv
        bar_initial = df.loc[df['id'] == i]
        bar_initial = bar_initial[col_list]
        aux_gene = []
        for rows in bar_initial.itertuples(index=False):
            x = list(rows)
            aux_gene.append(x)

        gene_list.append(aux_gene)

    heatmap_data = np.array(gene_list).sum(axis=0).T

    print(heatmap_data.shape)
    heatmap_genes = ('WW', 'WH', 'WE', 'WR', 'WB', 'HH', 'HE', 'HR',
                     'HB', 'EE', 'ER', 'EB', 'RR', 'RB', 'BB')
    heatmap_df = pd.DataFrame(data=heatmap_data, index=heatmap_genes)
    heatmap_df.columns.name = 'time'
    heatmap_df.index.name = 'gene'
    heatmap_data = pd.DataFrame(heatmap_df.stack(),
                                columns=['value']).reset_index()
    heatmap_source = ColumnDataSource(heatmap_data)

    # Heatmap
    heatmap_colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2",
                      "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
    mapper = LinearColorMapper(palette=heatmap_colors,
                               low=heatmap_data.value.min(),
                               high=heatmap_data.value.max())

    heatmap = figure(
        plot_width=800,
        plot_height=300,
        title="Heatmap",
        x_range=list(heatmap_df.columns.astype('str')),
        y_range=heatmap_genes,
        toolbar_location=None,
        tools=""
    )

    heatmap.rect(x="time", y="gene", width=1, height=1, source=heatmap_source,
                 line_color=None, fill_color=transform('value', mapper))

    csv_selected = gene_list[0]

    # Get data for graph
    counts = csv_selected[0]

    # Get colors
    bar_colors = cividis(len(col_list))

    bar_source = ColumnDataSource(data=dict(
        col_list=col_list,
        counts=counts,
        bar_colors=bar_colors,
        gene_list=gene_list))

    status = ColumnDataSource(data={
        'time': [1],
        'csv': [0]
    })

    bar = mg_bar(col_list, bar_source)

    # Slider
    slider = mg_slider(source, timeList, time, bar_source, status)

    # Select
    select = mg_select(csvList, bar_source, status)
    return heatmap, bar, slider, select


@time_function
def graph(request, csv):
    heatmap, bar, slider, select = one_experiment(csv)

    # Create grid for graphics
    grid = gridplot([[column(slider, heatmap, width=800), column(
        select, bar, width=800)]], toolbar_location=None)

    # Store components
    script, div = components(grid)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
                  'pages/base.html', {'script': script, 'div': div})


@time_function
def graph_2(request, csv, csv_2):
    scatter, bar, slider, select = one_experiment(csv)

    scatter_2, bar_2, slider_2, select_2 = one_experiment(csv)

    # Create grid for graphics
    grid = gridplot([[column(slider, scatter, slider_2, scatter_2, width=800),
                      column(select, bar, select_2, bar_2, width=800)]],
                    toolbar_location=None)

    # Store components
    script, div = components(grid)

    # Return to Django with Components sent as arguments which will then de
    # displayed
    return render(request,
                  'pages/base.html', {'script': script, 'div': div})
