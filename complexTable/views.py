# Django imports
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.template.defaulttags import register
from django.http import HttpResponse, Http404
from django.views.generic.edit import FormView

# Models import
from complexTable.models import Complex

from complexTable.forms import *

# Special python imports
import matplotlib
matplotlib.use('Agg')

# Python imports
from io import BytesIO
from ast import literal_eval
from wsgiref.util import FileWrapper
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import os
import re
import csv
import json
import base64
import logging
import tarfile
import pandas as pd
import seaborn as sns

# Graphic spacing variables
spacing = 15
tsSpacing = 5

# Logger to log
logger = logging.getLogger(__name__)

# region Graphic filters

def hist_post(request):
    if request.method == 'POST':
        form = HistForm(request.POST)

        if form.is_valid():
            mincutoff = form.cleaned_data['mincutoff']
            maxcutoff = form.cleaned_data['maxcutoff']

            preHistogram = parseHistogram()

            datas = preHistogram["datas"]
            names = preHistogram["names"]
            sizeHist = len(datas)
            datasLen = len(datas[0])

            deleter = []

            if mincutoff != None and maxcutoff != None:
                for index in range(0, datasLen):
                    if index != 0:
                        for innerIndex in range(0, sizeHist):
                            if datas[innerIndex][index] < mincutoff or datas[innerIndex][index] > maxcutoff:
                                deleter.insert(0, index)
                                break
            
            elif mincutoff == None and maxcutoff != None:
                for index in range(0, datasLen):
                    if index != 0:
                        for innerIndex in range(0, sizeHist):
                            if datas[innerIndex][index] > maxcutoff:
                                deleter.insert(0, index)
                                break
            
            elif mincutoff != None and maxcutoff == None:
                for index in range(0, datasLen):
                    if index != 0:
                        for innerIndex in range(0, sizeHist):
                            if datas[innerIndex][index] < mincutoff:
                                deleter.insert(0, index)
                                break

            if deleter:
                deleter = deleter
                for delet in deleter:
                    del names[delet-1]

                    for index in range(0, sizeHist):
                        del datas[index][delet]

            histogram = {}

            histogram["names"] = names
            histogram["datas"] = datas
            histogram["dsize"] = len(datas) * spacing

            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['mincutoff'] = mincutoff
            response_data['maxcutoff'] = maxcutoff
            #response_data['histData'] = histogram

            size = 0
            
            if names:
                size = (len(names) + 1) * spacing

                toPrint = "\n\tvar chart = c3.generate({\n\t\tbindto: '#show-histogram',\n\t\tdata: {\n\t\t\tcolumns: [\n\t"

                dataslen = len(datas) - 1
                for index, data in enumerate(datas):
                    toPrint = toPrint + "\t\t["
                    datalen = len(data) -1 
                    for innerIndex, info in enumerate(data):
                        if innerIndex == 0:
                            toPrint = toPrint + "'" + str(info) + "'"
                        else:
                            toPrint = toPrint + str(info)
                        
                        if not innerIndex == datalen:
                            toPrint = toPrint + ", "
                    
                    if not index == dataslen:
                        toPrint = toPrint + "],\n\t"
                    else:
                        toPrint = toPrint + "]\n\t"
                
                toPrint = toPrint + "\t],\n\t\ttype: 'bar'\n\t\t},\n\t\tsize: {\n\t\t\theight: 600,\n\t\t\twidth: "
                
                size = (len(names) + 1) * spacing

                if size < 400:
                    if size < 380:
                        toPrint = toPrint + "400"
                    else:
                        toPrint = toPrint + str(420-size)
                else:
                    toPrint = toPrint + str(size)

                toPrint = toPrint + "\n\t\t},\n\t\tpadding: {\n\t\t\tbottom: 80,\n\t\t\tright: 20\n\t\t},\n\t\taxis: {\n\t\t\tx: {\n\t\t\t\ttype: 'category',\n\t\t\t\ttick: {\n\t\t\t\t\trotate: 60,\n\t\t\t\t\tmultiline: false\n\t\t\t\t},\n\t\t\t\tcategories: ["
                
                nameslen = len(names) - 1

                for index, name in enumerate(names):
                    toPrint = toPrint + "'" + str(name) + "'"

                    if not index == nameslen:
                        toPrint = toPrint + ", "
                
                toPrint = toPrint + "]\n\t\t\t}\n\t\t},\n\t\tbar: {\n\t\t\twidth: {\n\t\t\t\tratio: 0.7\n\t\t\t}\n\t\t}\n\t});\n"
            else:
                toPrint = "alert('No results matching your filter!');"
            
            response_data["script"] = toPrint

            if names:
                if size < 400:
                    response_data["style"]= "\n\t.html2canvas-container\n\t{\n\t\twidth: " + str(400) + "px !important;\n\t\theight: 600px !important;\n\t}"
                else:
                    response_data["style"]= "\n\t.html2canvas-container\n\t{\n\t\twidth: " + str(size) + "px !important;\n\t\theight: 600px !important;\n\t}"
            else:
                response_data["style"]=""


            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def line2d_post(request):
    if request.method == 'POST':
        form = TwodmapFormLine(request.POST)
        if form.is_valid():
            logger.warn(form.cleaned_data)
            mincutoff2d = form.cleaned_data['mincutoff2d']
            maxcutoff2d = form.cleaned_data['maxcutoff2d']
            choice = form.cleaned_data['types2d']

            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['mincutoff2d'] = mincutoff2d
            response_data['maxcutoff2d'] = maxcutoff2d
            alt = ''
            l2d = ''
            style = ''

            if choice == "simple":
                l2d = simplePlot(mincutoff2d, maxcutoff2d)
                alt = '2D simple line graphic'

            else:
                l2d = runningAvg(mincutoff2d, maxcutoff2d)
                alt = '2D running average line graphic'
                style='style="height: 40%; width: 40%;"'
                
            response_data['line2d'] = '<img src="data:image/png;base64, ' + l2d + '" alt="' + alt + '" ' + style + '/>'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
            json.dumps({"Wrong": "Form not valid"}),
            content_type="application/json"
        )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def heat2d_post(request):
    if request.method == 'POST':
        form = TwodmapFormHeat(request.POST)
        if form.is_valid():
            logger.warn(form.cleaned_data)
            mincutoffheat2d = form.cleaned_data['mincutoffheat2d']
            maxcutoffheat2d = form.cleaned_data['maxcutoffheat2d']

            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['mincutoff2d'] = mincutoffheat2d
            response_data['maxcutoff2d'] = maxcutoffheat2d
                
            response_data['heat2d'] = '<img src="data:image/png;base64, ' + heatMap(mincutoffheat2d, maxcutoffheat2d) + '" alt="2D map heatmap" style="width: 1500px; height: 500px;"/>'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
            json.dumps({"Wrong": "Form not valid"}),
            content_type="application/json"
        )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def distrib2d_post(request):
    if request.method == 'POST':
        form = TwodmapFormDistrib(request.POST)
        if form.is_valid():
            logger.warn(form.cleaned_data)
            mincutoff2d = form.cleaned_data['mincutoffdistrib2d']
            maxcutoff2d = form.cleaned_data['maxcutoffdistrib2d']
            choice = form.cleaned_data['types2ddistrib']

            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['mincutoff2d'] = mincutoff2d
            response_data['maxcutoff2d'] = maxcutoff2d
            alt = ''
            l2d = ''
            style = ''

            if choice == "strip":
                l2d = distribStrip(mincutoff2d, maxcutoff2d)
                alt = '2D map distribuition graphic strip style'
                style = 'style="height: 40%; width: 40%;"'

            elif choice == "box":
                l2d = distribBox(mincutoff2d, maxcutoff2d)
                alt = '2D map distribuition graphic box style'
                style = 'style="height: 40%; width: 40%;"'
            else:
                l2d = distribViolin(mincutoff2d, maxcutoff2d)
                alt = '2D map distribuition graphic violin style'
                style = 'style="height: 40%; width: 40%;"'
                
            response_data['distrib2d'] = '<img src="data:image/png;base64, ' + l2d + '" alt="' + alt + '"' + style + '/>'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
            json.dumps({"Wrong": "Form not valid"}),
            content_type="application/json"
        )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def facet2d_post(request):
    if request.method == 'POST':
        form = TwodmapFormFacet(request.POST)
        if form.is_valid():
            logger.warn(form.cleaned_data)
            mincutoff2d = form.cleaned_data['mincutofffacet2d']
            maxcutoff2d = form.cleaned_data['maxcutofffacet2d']
            choice = form.cleaned_data['types2dfacet']

            response_data = {}

            response_data['result'] = 'Create post successful!'
            response_data['mincutoff2d'] = mincutoff2d
            response_data['maxcutoff2d'] = maxcutoff2d
            alt = ''
            l2d = ''
            style = ''

            if choice == "fg":
                l2d = facetGrids(mincutoff2d, maxcutoff2d)
                alt = '2D map facet grid graphic'
                style = 'style="height: 75%; width: 25%;"'

            elif choice == "fgrolling":
                l2d = facetGridsRolling(mincutoff2d, maxcutoff2d)
                alt = '2D map rolling facet grid graphic'
                style = 'style="height: 75%; width: 25%;"'

            elif choice == "fgdistplot":
                l2d = facetGridsDistPlot(mincutoff2d, maxcutoff2d)
                alt = '2D map facet grid dist graphic'
                style = 'style="height: 40%; width: 75%;"'
            
            else:
                l2d = facetGridsSeparate(mincutoff2d, maxcutoff2d)
                alt = '2D map facet grid separate dist graphic'
                style = 'style="height: 80%; width: 25%;"'
                
            response_data['facet2d'] = '<img src="data:image/png;base64, ' + l2d + '" alt="' + alt + '"' + style + '/>'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
            json.dumps({"Wrong": "Form not valid"}),
            content_type="application/json"
        )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

# endregion

# region Parse files

def parseTimeseries():
    path = os.path.join(settings.FILES_DIR, 'dats/timeseries.csv')

    info = readfile(path)

    remInfo = []

    while info[-1][0] == '#':
        remInfo.append(info[-1])
        del info[-1]
    
    names = []
    datas = []

    for index, line in enumerate(info):
        if index == 0:
            names = line#list(filter(None, re.split(',| |\t|\n', line)))
        else:
            datas.append(line)
            # datas.append(list(filter(None, re.split(',| |\t|\n', line))))

    datas = list(map(list, zip(*datas)))

    datasize = len(datas[0]) * tsSpacing

    
    for index, line in enumerate(datas):
        line.insert(0, names[index])

    return {"names": names, "x": names[0], "datas": datas, "dsize": datasize}

def parseHistogram():
    path = os.path.join(settings.FILES_DIR, 'dats/histogram.dat')

    info = readfile(path)
    
    names = []
    datas = []

    for line in info:
        names.append(str(line[0]) + " " + str(line[1]))
        datas.append([line[2], line[3]])
    
    datas = list(map(list, zip(*datas)))

    datasize = len(datas[0]) * spacing
    
    if datasize < 400:
        if datasize < 380:
            datasize = 400
        else:
            datasize = 420 - datasize
    else:
        datasize = datasize + 20

    for index, line in enumerate(datas):
        line.insert(0, "Data "+ str(index))

    return {"names": names, "datas": datas, "dsize": datasize}

def parseCSV():
    path = os.path.join(settings.FILES_DIR, 'database.csv')
    reader = csv.DictReader(open(path))
    dataInfo = {}

    for idx, line in enumerate(reader):
        localData = {}

        for key, value in line.items():
            if key == "ID":
                localData["id"] = tryToRound(value, 2)
            elif key == "":
                localData["ID"] = tryToRound(value, 2)
            else:
                try:
                    localData[key.lower()] = tryToRound(value, 2)
                except:
                    localData[key] = tryToRound(value, 2)
                        

        # dataInfo.append(localData)
        dataInfo[str(idx)] = localData

    keys = reader.fieldnames
    keys[keys.index("")] = "ID"

    return (dataInfo, keys)

def parse2Dmap(mincutoff2d, maxcutoff2d):
    path = os.path.join(settings.FILES_DIR, 'dats/2D_map.dat')
    df = pd.read_csv(path, delim_whitespace=True, header=None).drop([0], axis=1)

    if mincutoff2d != None and maxcutoff2d != None:
        df = df[(df > mincutoff2d) & (df < maxcutoff2d)].dropna(axis='columns')
    
    elif mincutoff2d == None and maxcutoff2d != None:
        df = df[(df < maxcutoff2d)].dropna(axis='columns')
    
    elif mincutoff2d != None and maxcutoff2d == None:
        df = df[(df > mincutoff2d)].dropna(axis='columns')

    return df

# endregion

# region 2dGraphic generating functions

def simplePlot(mincutoff2d, maxcutoff2d):
    df = parse2Dmap(mincutoff2d, maxcutoff2d)
    df.plot(figsize=(10,5))
    
    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png')
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def runningAvg(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # Agora apenas a "running average" a cada 100 passos.
    df.rolling(window=100).mean().plot(figsize=(10,5))

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def heatMap(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # Plot as a heatmap. ( não sei arrumar os xticks )
    plt.figure(figsize = (15,5))  # Truque para arrumar o tamanho da figura.
    sns.heatmap(df.transpose(), cmap="viridis")

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64
    # return response

def distribStrip(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # Plot as a heatmap. ( não sei arrumar os xticks )
    plt.figure(figsize = (15,5))  # Truque para arrumar o tamanho da figura.
    sns.catplot(data=df.melt(), x='variable', y='value', kind='strip', aspect=2)
    
    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def distribBox(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # Plot as a heatmap. ( não sei arrumar os xticks )
    plt.figure(figsize = (15,5))  # Truque para arrumar o tamanho da figura.
    sns.catplot(data=df.melt(), x='variable', y='value', kind='box', aspect=2)

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def distribViolin(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # Plot as a heatmap. ( não sei arrumar os xticks )
    plt.figure(figsize = (15,5))  # Truque para arrumar o tamanho da figura.
    sns.catplot(data=df.melt(), x='variable', y='value', kind='violin', aspect=2)

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def facetGrids(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.
    g=sns.FacetGrid(data=df.melt(),col='variable',col_wrap=3,sharey=False)
    g.map(plt.plot,'value')

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def facetGridsRolling(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.
    g=sns.FacetGrid(data=df.rolling(window=100).mean().melt(),col='variable',col_wrap=3,sharey=False)
    g.map(plt.plot,'value')

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def facetGridsDistPlot(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.
    g=sns.FacetGrid(data=df.melt(),hue='variable',aspect=4)
    g.map(sns.distplot,'value',hist=False)

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

def facetGridsSeparate(mincutoff, maxcutoff):
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.
    g=sns.FacetGrid(data=df.melt(),col='variable',col_wrap=3,hue='variable',aspect=1)
    g.map(sns.distplot,'value',hist=False)

    fig_buffer = BytesIO()
    plt.savefig(fig_buffer, format='png', dpi=150)
    image_base64 = base64.b64encode(fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    fig_buffer.close()
    return image_base64

# endregion

# region Auxiliar functions

def readfile(path):
    """
    Read file from path, split the lines with commas, whitespaces, \t and \n
        then return a list (lines) of lists (splited values from lines).
    """

    # Empty list to hold lists of lines
    info = []

    # Open file using the with environment
    with open(path) as f:
        # For each line in file
        for line in f:
            # Remove whitespaces from beggining and end of line
            line = line.strip()

            # Split the line using commas, whitespaces. \t and \n and return a list
            datas = list(filter(None, re.split(',| |\t|\n', line)))

            # Instantiate a new list to hold line datas after parse them (from string to int or float)
            parsedLine = []

            # for each element in line
            for data in datas:
                # Check if is Hexadecimal ()
                if isHex(data):
                    # If is, do not parse and append directly
                    parsedLine.append(data)
                else:
                    # Try to append parsing
                    try:
                        parsedLine.append(literal_eval(data))
                    # Since non numbers parsing throws exception, append the value as string
                    except:
                        parsedLine.append(data)
            # Add the line to list of lines
            info.append(parsedLine)
            
    return info

def isHex(s):
    """
    Check if value passed is Hexadecimal or not
    """
    try:
        int(s, 16)
        return True

    except:
        return False

def tryToRound(val, elems):
    """
    Try to round the passed value if is float, otherwise return the value itself.
    """
    try:
        value = literal_eval(val)
        if isinstance(value, int):
            return val
        return round(value, elems)
    except:
        return val

# endregion


def download(request):
    """
    Function to download a file
    """
    file_path = os.path.join(settings.FILES_DIR, 'summary/BCD-ACA/resp/complex/complex.prmtop')
    downloadFile(file_path)
    

def downloadFile(path):
    """
    Download a file trough http procotol from given path
    """
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404("File not Found")

def downloadFiles(request):
    data = parseCSV()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CheckForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            ids = form.cleaned_data['choices']

            response = HttpResponse(content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename=datas.tar.gz'
            tar = tarfile.open(fileobj=response, mode="w:gz")

            paths = set()

            for id in ids:
                if not isinstance(data[0][id], list):
                    path = os.path.join(settings.FILES_DIR, ''.join(['summary/', data[0][id]['complex'].upper(), '/']))
                    if path not in paths:
                        tar.add(path, arcname=data[0][id]['complex'].upper())
                    paths.add(path)
                        

            logger.warn(paths)
            # for path in paths:

            tar.close()
            return response

    variables = {
        "checkForm": CheckForm,
        'table': data[0],
        'keys': data[1]
        }

    return render(request, 'complexTable/complexTable.html', variables)
            #return HttpResponseRedirect('/thanks/')

# class downStuff(FormView):
#     form_class = CheckForm
#     def post(self, request, *args, **kwargs):
#         context = self.get_context_data()

#         tar = tarfile.open("datas.tar.gz", "w:gz")

#         for item in form.POST.getlist('ids'):
#             a

#         tar.close()

# Index 
class IndexView(generic.ListView):
    template_name = 'complexTable/index.html'
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Complex

class ComplexView(generic.ListView):
        #template_name = 'complexTable/complexTable.html'
        #model = Complex
        # form_class = CheckForm

        # @register.filter
        # def getItem(dictionary, key):
        #     return dictionary.get(key)

        def get(self, request, **kwargs):
            # we will pass this context object into the
            # template so that we can access the data
            # list in the template
            
            data = parseCSV()

            variables = {
                "checkForm": CheckForm,
                'table': data[0],
                'keys': data[1]
                }

            return render(request, 'complexTable/complexTable.html', variables)

@register.filter
def getItem(dictionary, key):
        return dictionary.get(key)

class DetailedView(generic.ListView):
    def get(self, request, **kwargs):

        lineId = request.GET.get('id')

        data = parseCSV()

        histogram = parseHistogram()
        timeSeries = parseTimeseries()
        
        minlimit = 0
        maxlimit = None

        line2d = simplePlot(minlimit, maxlimit)
        heatmap = heatMap(minlimit, maxlimit)
        distrib = distribStrip(minlimit, maxlimit)
        facet = facetGrids(minlimit, maxlimit)

        variables = {
            "histForm": HistForm,
            "2DmapForm": TwodmapFormLine,
            "2DheatForm": TwodmapFormHeat,
            "2DdistribForm": TwodmapFormDistrib,
            "2DfacetForm": TwodmapFormFacet,
            'info': data[0][lineId],
            'keys': data[1],
            'bigID': lineId,
            'histogram': histogram,
            'timeSeries': timeSeries,
            'line2d': line2d,
            'heatmap': heatmap,
            'distrib': distrib,
            'facet': facet
            }

        return render(request, 'complexTable/detailedInfo.html', variables)