# Django imports
import seaborn as sns
import pandas as pd
import tarfile
import logging
import base64
import json
import csv
import re
import os
from wsgiref.util import FileWrapper
from ast import literal_eval
from io import BytesIO
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

# Late imports
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt


# Graphic spacing variables
spacing = 15
tsSpacing = 5

# Logger to log
logger = logging.getLogger(__name__)

# region Graphic filters


def hist_post(request):
    """
    Deals with the post data to process the histogram
    """

    # If is POST
    if request.method == 'POST':

        # Get the POST data in HistForm
        form = HistForm(request.POST)

        # If the form is valid
        if form.is_valid():
            # Read max and min cutoff values from POST
            mincutoff = form.cleaned_data['mincutoff']
            maxcutoff = form.cleaned_data['maxcutoff']

            # Parse the histogram
            preHistogram = parseHistogram()

            # Read info from parsed histogram dictionary
            datas = preHistogram["datas"]
            names = preHistogram["names"]

            # Compute the length of graphic
            sizeHist = len(datas)
            datasLen = len(datas[0])

            # List to hold which data will be deleted (should be reverse deletion)
            deleter = []

            # If both restrictions are imposed
            if mincutoff != None and maxcutoff != None:
                # For each serie in dataset
                for index in range(1, datasLen):
                    # For each element in the serie
                    for innerIndex in range(0, sizeHist):
                        # If the element does not respect restrictions
                        if datas[innerIndex][index] < mincutoff or datas[innerIndex][index] > maxcutoff:
                            # Flag its index to delete it (decrescent)
                            deleter.insert(0, index)
                            break

            # If only an upper bound is imposed
            elif mincutoff == None and maxcutoff != None:
                # For each serie in dataset
                for index in range(1, datasLen):
                    # For each element in serie
                    for innerIndex in range(0, sizeHist):
                        # If the element does not respect the restriction
                        if datas[innerIndex][index] > maxcutoff:
                            # Flag its index to delete it (decrescent)
                            deleter.insert(0, index)
                            break

            # If only a lower bound is imposed
            elif mincutoff != None and maxcutoff == None:
                # For each serie in dataset
                for index in range(1, datasLen):
                    # For each element in serie
                    for innerIndex in range(0, sizeHist):
                        # If the element does not respect the restriction
                        if datas[innerIndex][index] < mincutoff:
                            # Flag its index to delete it (decrescent)
                            deleter.insert(0, index)
                            break

            # If there are any flagged index to delete
            if deleter:
                # For each flagged item (this is a decrescent list)
                for delet in deleter:
                    # Delete its name
                    del names[delet-1]

                    # For each serie in dataset
                    for index in range(0, sizeHist):
                        # Delete the element from data serie
                        del datas[index][delet]

            # Create de histogram dictionary
            histogram = {}

            # Add info to it
            histogram["names"] = names
            histogram["datas"] = datas
            histogram["dsize"] = len(datas) * spacing

            # Create the response data object (dictionary)
            response_data = {}

            # Define a default size
            size = 0

            # If there is any name
            if names:
                # Set its size
                size = (len(names) + 1) * spacing

                # Start to create the print data
                toPrint = "\n\tvar chart = c3.generate({\n\t\tbindto: '#show-histogram',\n\t\tdata: {\n\t\t\tcolumns: [\n\t"

                # Get size of dataset
                dataslen = len(datas) - 1

                # For each serie in dataset
                for index, data in enumerate(datas):
                    # Append more info
                    toPrint = toPrint + "\t\t["

                    # Get the length of serie
                    datalen = len(data) - 1

                    # For each element in serie
                    for innerIndex, info in enumerate(data):
                        # If is the first element
                        if innerIndex == 0:
                            # It's the name
                            toPrint = toPrint + "'" + str(info) + "'"
                        else:
                            # Its a number
                            toPrint = toPrint + str(info)

                        # If its not last element
                        if not innerIndex == datalen:
                            # Add a comma
                            toPrint = toPrint + ", "

                    # If its not the last element
                    if not index == dataslen:
                        # Close the bracket and add comma
                        toPrint = toPrint + "],\n\t"
                    else:
                        # Jus close the bracket
                        toPrint = toPrint + "]\n\t"

                # Add more info to print
                toPrint = toPrint + \
                    "\t],\n\t\ttype: 'bar'\n\t\t},\n\t\tsize: {\n\t\t\theight: 600,\n\t\t\twidth: "

                # If the size is lower than 400 (small graphic)
                if size < 400:
                    # If is smaller than 380 (small graphic)
                    if size <= 380:
                        # Set its size to 400
                        toPrint = toPrint + "400"
                    else:
                        # Since is a not so small graphic, the graphic will have its size between 400 and 420
                        toPrint = toPrint + str(420-size)
                else:
                    # Otherwise the graphic will have the size itself
                    toPrint = toPrint + str(size)

                # Add more info
                toPrint = toPrint + \
                    "\n\t\t},\n\t\tpadding: {\n\t\t\tbottom: 80,\n\t\t\tright: 20\n\t\t},\n\t\taxis: {\n\t\t\tx: {\n\t\t\t\ttype: 'category',\n\t\t\t\ttick: {\n\t\t\t\t\trotate: 60,\n\t\t\t\t\tmultiline: false\n\t\t\t\t},\n\t\t\t\tcategories: ["

                # Compute the length of names
                nameslen = len(names) - 1

                # For each name in names
                for index, name in enumerate(names):
                    # Append it (will be label)
                    toPrint = toPrint + "'" + str(name) + "'"

                    # If its not the last index
                    if not index == nameslen:
                        # Add a comma
                        toPrint = toPrint + ", "

                # Append more info
                toPrint = toPrint + \
                    "]\n\t\t\t}\n\t\t},\n\t\tbar: {\n\t\t\twidth: {\n\t\t\t\tratio: 0.7\n\t\t\t}\n\t\t}\n\t});\n"
            else:
                # Throw an error
                toPrint = "alert('No results matching your filter!');"

            # Add all the data to response_data
            response_data["script"] = toPrint

            # Process names sizes
            if names:
                # If its smaller than 400
                if size < 400:
                    # Set its size to 400
                    response_data["style"] = "\n\t.html2canvas-container\n\t{\n\t\twidth: " + str(
                        400) + "px !important;\n\t\theight: 600px !important;\n\t}"
                else:
                    # Otherwise keep its size
                    response_data["style"] = "\n\t.html2canvas-container\n\t{\n\t\twidth: " + str(
                        size) + "px !important;\n\t\theight: 600px !important;\n\t}"
            else:
                # Since there is no name, there is no style to apply
                response_data["style"] = ""

            # Return the http response as a json
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

    else:
        # Since is not POST, return a dummy json
        return HttpResponse(
            json.dumps(
                {"nothing to see": "You're not suppose to sniff this."}),
            content_type="application/json"
        )


def line2d_post(request):
    """
    Deals with the post data to process the line plot
    """

    # If is POST
    if request.method == 'POST':
        # Get the POST data in TwodmapFormLine
        form = TwodmapFormLine(request.POST)

        # If the form is valid
        if form.is_valid():
            # Read max, min cutoff and types2d values from POST
            mincutoff2d = form.cleaned_data['mincutoff2d']
            maxcutoff2d = form.cleaned_data['maxcutoff2d']
            choice = form.cleaned_data['types2d']

            # Create a dictionary to hold response data
            response_data = {}

            # alt attribute
            alt = ''
            # src attribute
            l2d = ''

            # If user has choosen simple graphic
            if choice == "simple":
                # Get the base64 img string from simple graphic
                l2d = simplePlot(mincutoff2d, maxcutoff2d)
                # Set the alt to the image
                alt = '2D simple line graphic'

            else:
                # Get the base54 img string from running average graphic
                l2d = runningAvg(mincutoff2d, maxcutoff2d)
                # Set the alt to the image
                alt = '2D running average line graphic'

            # Create the response data line2d entry
            response_data['line2d'] = '<img src="data:image/png;base64, ' + \
                l2d + '" id="line-img" alt="' + alt + '"/>'

            # Close all open plots (otherwise will eat all memory)
            plt.close('all')

            # Return a success HttpResponse in json format
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            # Return a fail (form not valid) HttpResponse in json format
            return HttpResponse(
                json.dumps({"Wrong": "Form not valid"}),
                content_type="application/json"
            )

    else:
        # Return a fail (No post) HttpResponse in json format
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def heat2d_post(request):
    """
    Deals with the post data to process the heatmap plot
    """

    # If is POST
    if request.method == 'POST':
        # Get the POST data in TwodmapFormHeat
        form = TwodmapFormHeat(request.POST)

        # If the form is valid
        if form.is_valid():
            # Read max and min cutoff values from POST
            mincutoffheat2d = form.cleaned_data['mincutoffheat2d']
            maxcutoffheat2d = form.cleaned_data['maxcutoffheat2d']

            # Create reponse data dictionary
            response_data = {}

            # Add the heat2d data as a complete img tag
            response_data['heat2d'] = '<img src="data:image/png;base64, ' + heatMap(
                mincutoffheat2d, maxcutoffheat2d) + '" id="heat-img" alt="2D map heatmap"/>'

            # Close all open plots (otherwise will eat all memory)
            plt.close('all')

            # Return a success HttpResponse in json format
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )

        else:
            # Return a fail (form not valid) HttpResponse in json format
            return HttpResponse(
                json.dumps({"Wrong": "Form not valid"}),
                content_type="application/json"
            )

    else:
        # Return a fail (No post) HttpResponse in json format
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def distrib2d_post(request):
    """
    Deals with the post data to process the heatmap plot
    """

    # If is POST
    if request.method == 'POST':
        # Get the POST data in TwodmapFormDistrib
        form = TwodmapFormDistrib(request.POST)

        # If the form is valid
        if form.is_valid():
            # Read max, min cutoff and types2ddistrib values from POST
            mincutoff2d = form.cleaned_data['mincutoffdistrib2d']
            maxcutoff2d = form.cleaned_data['maxcutoffdistrib2d']
            choice = form.cleaned_data['types2ddistrib']

            # Create response dictionary
            response_data = {}

            # alt attribute
            alt = ''
            # src attribute
            l2d = ''

            # If user has choosen strip type
            if choice == "strip":
                # Get base64 string of distribStrip
                l2d = distribStrip(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map distribuition graphic strip style'

            # If user has choosen box type
            elif choice == "box":
                # Get base64 string of distribBox
                l2d = distribBox(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map distribuition graphic box style'

            # User has choosen Violin type
            else:
                # Get base64 string of distribViolin
                l2d = distribViolin(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map distribuition graphic violin style'

            # Close all open plots (otherwise will eat all memory)
            plt.close('all')

            # Add the distrib2d data as a complete img tag
            response_data['distrib2d'] = '<img src="data:image/png;base64, ' + \
                l2d + '" id="distrib-img" alt="' + alt + '"/>'

            # Return a success HttpResponse in json format
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            # Return a fail (form not valid) HttpResponse in json format
            return HttpResponse(
                json.dumps({"Wrong": "Form not valid"}),
                content_type="application/json"
            )

    else:
        # Return a fail (No post) HttpResponse in json format
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def facet2d_post(request):
    """
    Deals with the post data to process the facet plot
    """

    # If is post
    if request.method == 'POST':
        # Get the POST data in TwodmapFormFacet
        form = TwodmapFormFacet(request.POST)

        # If form is valid
        if form.is_valid():
            # Read max, min cutoff and types2ddistrib values from POST
            mincutoff2d = form.cleaned_data['mincutofffacet2d']
            maxcutoff2d = form.cleaned_data['maxcutofffacet2d']
            choice = form.cleaned_data['types2dfacet']

            # Create response dictionary
            response_data = {}

            # alt attribute
            alt = ''
            # src attribute
            l2d = ''

            # User has choosen a normal facet grids graphic
            if choice == "fg":
                # Get base 64 string of a normal face grid graphic
                l2d = facetGrids(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map facet grid graphic'

            # User has choosen facet grid rolling graphic
            elif choice == "fgrolling":
                # Get base64 string of Rolling plot
                l2d = facetGridsRolling(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map rolling facet grid graphic'

            # User has choosen facet grid dist graphic
            elif choice == "fgdistplot":
                # Get base64 string of dist plot
                l2d = facetGridsDistPlot(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map facet grid dist graphic'

            # User has choosen facet grid separate graphic
            else:
                # Get base64 string of separate plot
                l2d = facetGridsSeparate(mincutoff2d, maxcutoff2d)
                # Set the alt atribute
                alt = '2D map facet grid separate dist graphic'

            # Close all open plots (otherwise will eat all memory)
            plt.close('all')

            # Add the facet2d data as a complete img tag
            response_data['facet2d'] = '<img src="data:image/png;base64, ' + \
                l2d + '" id="facet-img" alt="' + alt + '"/>'

            # Return a success HttpResponse in json format
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            # Return a fail (form not valid) HttpResponse in json format
            return HttpResponse(
                json.dumps({"Wrong": "Form not valid"}),
                content_type="application/json"
            )

    else:
        # Return a fail (No post) HttpResponse in json format
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

# endregion

# region Parse files


def parseTimeseries():
    """
    Parse the timeseries.csv file
    """

    # Create the path string
    path = os.path.join(settings.FILES_DIR, 'dats/timeseries.csv')

    # Open file
    info = readfile(path)

    # List to hold removed items (if needed in future is here)
    # remInfo = []

    # Remove all lines which starts with a # char
    while info[-1][0] == '#':
        # Add the removed item to a list (if needed in fiture is here)
        # remInfo.append(info[-1])

        # Delete the line
        del info[-1]

    # Lists to hold names and datas
    names = []
    datas = []

    # For each line in dataset
    for index, line in enumerate(info):
        # If is the first index
        if index == 0:
            # Its a name
            names = line  # list(filter(None, re.split(',| |\t|\n', line)))
        else:
            # Otherwise is data
            datas.append(line)
            # datas.append(list(filter(None, re.split(',| |\t|\n', line))))

    # Transpose datas list
    datas = list(map(list, zip(*datas)))

    # Get datas size then mutiply to a global variable time series Spacing
    datasize = len(datas[0]) * tsSpacing

    # Add the name of the series on the top of the each datas line
    for index, line in enumerate(datas):
        line.insert(0, names[index])

    # Return a dictionary with all gathered info
    return {"names": names, "x": names[0], "datas": datas, "dsize": datasize}


def parseHistogram():
    """
    Parse the histogram.dat file
    """

    # Create the path string
    path = os.path.join(settings.FILES_DIR, 'dats/histogram.dat')

    # Open file
    info = readfile(path)

    # Lists to hold names and datas
    names = []
    datas = []

    # For each line in read data
    for line in info:
        # The First 2 positions of list are the name
        names.append(str(line[0]) + " " + str(line[1]))

        # The last 2 are datas
        datas.append([line[2], line[3]])

    # Transpose the list
    datas = list(map(list, zip(*datas)))

    # Get datas size
    datasize = len(datas[0]) * spacing

    # If size is lower than 400
    if datasize < 400:
        # If the size is lower than 380
        if datasize <= 380:
            # Size will be 400
            datasize = 400
        else:
            # Size will be between
            datasize = 420 - datasize
    else:
        # Otheriwse size will be increased in 20 px
        datasize = datasize + 20

    # Add name on the top of every line of data
    for index, line in enumerate(datas):
        line.insert(0, "Data " + str(index))

    # Return a dictionary with all gathered info
    return {"names": names, "datas": datas, "dsize": datasize}


def parseCSV():
    """
    Parse the database.csv file
    """

    # Create the path string
    path = os.path.join(settings.FILES_DIR, 'database.csv')

    # Open file
    reader = csv.DictReader(open(path))

    # Dictionary to hold all data
    dataInfo = {}

    # For each object in csv
    for idx, line in enumerate(reader):
        # Dictionary to hold lines
        localData = {}

        # For each element in line
        for key, value in line.items():
            # If is "ID"
            if key == "ID":
                # Put it on "id" field
                localData["id"] = tryToRound(value, 2)
            # If has no key
            elif key == "":
                # Put it on "ID" field
                localData["ID"] = tryToRound(value, 2)
            else:
                # Try to lower the key
                try:
                    localData[key.lower()] = tryToRound(value, 2)
                except:
                    localData[key] = tryToRound(value, 2)

        # Add the local data to data info
        dataInfo[str(idx)] = localData

    # Get all keys
    keys = reader.fieldnames

    # Sday that the key with no index is the ID
    keys[keys.index("")] = "ID"

    # Return the tuple
    return (dataInfo, keys)


def parse2Dmap(mincutoff2d, maxcutoff2d):
    """
    Read 2D_map.dat and return its contents
    """

    # Create path variable
    path = os.path.join(settings.FILES_DIR, 'dats/2D_map.dat')

    # Read csv
    df = pd.read_csv(path, delim_whitespace=True,
                     header=None).drop([0], axis=1)

    # If there is min and max cutoff
    if mincutoff2d != None and maxcutoff2d != None:
        # Make it
        df = df[(df > mincutoff2d) & (df < maxcutoff2d)].dropna(axis='columns')

    # If there is just a max cutoff
    elif mincutoff2d == None and maxcutoff2d != None:
        # Make it
        df = df[(df < maxcutoff2d)].dropna(axis='columns')

    # If there is just a min cutoff
    elif mincutoff2d != None and maxcutoff2d == None:
        # Make it
        df = df[(df > mincutoff2d)].dropna(axis='columns')

    # Return data
    return df

# endregion

# region 2dGraphic generating functions


def simplePlot(mincutoff2d, maxcutoff2d):
    """
    Return a base64 string of a simple plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff2d, maxcutoff2d)

    # Plot it
    df.plot(figsize=(10, 5))

    # Set legend position
    plt.legend(loc='upper right')

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png')

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def runningAvg(mincutoff, maxcutoff):
    """
    Return a base64 string of a running average plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # Perform a "running average" for each 100 steps.
    df.rolling(window=100).mean().plot(figsize=(10, 5))

    # Set legend position
    plt.legend(loc='upper right')

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def heatMap(mincutoff, maxcutoff):
    """
    Return a base64 string of a heatmap plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # Set fig size
    plt.figure(figsize=(15, 5))

    # Plot as a heatmap. ( não sei arrumar os xticks )
    sns.heatmap(df.transpose(), cmap="viridis")

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def distribStrip(mincutoff, maxcutoff):
    """
    Return a base64 string of a distribution strip plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # Set fig size
    plt.figure(figsize=(15, 5))

    # Plot as a heatmap. ( não sei arrumar os xticks )
    sns.catplot(data=df.melt(), x='variable',
                y='value', kind='strip', aspect=2)

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def distribBox(mincutoff, maxcutoff):
    """
    Return a base64 string of a distribution box plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # Set fig size
    plt.figure(figsize=(15, 5))

    # Plot as a heatmap. ( não sei arrumar os xticks )
    sns.catplot(data=df.melt(), x='variable', y='value', kind='box', aspect=2)

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def distribViolin(mincutoff, maxcutoff):
    """
    Return a base64 string of a distribution violin plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # Set fig size
    plt.figure(figsize=(15, 5))

    # Plot as a heatmap. ( não sei arrumar os xticks )
    sns.catplot(data=df.melt(), x='variable',
                y='value', kind='violin', aspect=2)

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def facetGrids(mincutoff, maxcutoff):
    """
    Return a base64 string of a facet grid plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.

    # Plot as a heatmap. ( não sei arrumar os xticks )
    g = sns.FacetGrid(data=df.melt(), col='variable', col_wrap=3, sharey=False)
    g.map(plt.plot, 'value')

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def facetGridsRolling(mincutoff, maxcutoff):
    """
    Return a base64 string of a facet grid rolling plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.

    # Plot as a heatmap. ( não sei arrumar os xticks )
    g = sns.FacetGrid(data=df.rolling(window=100).mean().melt(),
                      col='variable', col_wrap=3, sharey=False)
    g.map(plt.plot, 'value')

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def facetGridsDistPlot(mincutoff, maxcutoff):
    """
    Return a base64 string of a facet grid dist plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.

    # Plot as a heatmap. ( não sei arrumar os xticks )
    g = sns.FacetGrid(data=df.melt(), hue='variable', aspect=4)
    g.map(sns.distplot, 'value', hist=False)

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64


def facetGridsSeparate(mincutoff, maxcutoff):
    """
    Return a base64 string of a facet grid separate plot image
    """

    # Get the data frame
    df = parse2Dmap(mincutoff, maxcutoff)

    # col = coluna
    # hue = cores
    # col_wrap = maximo por coluna.
    # sharey = compartilhar o eixo Y.

    # Plot as a heatmap. ( não sei arrumar os xticks )
    g = sns.FacetGrid(data=df.melt(), col='variable',
                      col_wrap=3, hue='variable', aspect=1)
    g.map(sns.distplot, 'value', hist=False)

    # Create a buffer
    fig_buffer = BytesIO()

    # Save the image as png
    plt.savefig(fig_buffer, format='png', dpi=150)

    # Convert image to base64
    image_base64 = base64.b64encode(
        fig_buffer.getvalue()).decode('utf-8').replace('\n', '')

    # Close the buffer
    fig_buffer.close()

    # Return string
    return image_base64

# endregion

# region Auxiliar functions


def build_nested_helper(path, text, container):
    """
    Convert string into dict [RECURSIVELY]
    """

    # Split string with /
    segs = path.split('/')

    # First will be head
    head = segs[0]

    # The others are tail
    tail = segs[1:]

    # If tail is empty
    if not tail:
        # Its a file
        container[head] = 'file'
    else:
        # If head is not in dict yet
        if head not in container:
            # Add it as a new dict
            container[head] = {}

        # Call the function recursively
        build_nested_helper('/'.join(tail), text, container[head])


def build_nested(paths):
    """
    Initialize vars then call the recursive function to build dict
    """

    # New dict to hold everything
    container = {}

    # For each path in list
    for path in paths:
        # Build its tree (container is passed by reference)
        build_nested_helper(path, path, container)

    # Return the tree
    return container


def getListOfFilesHelper(dirName):
    '''
    For the given path, get the List of all files in the directory tree 
    '''

    # create a list of file and sub directories names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)

        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFilesHelper(fullPath)
        else:
            # Otherwise add the path
            allFiles.append(fullPath)

    # Return the list of files paths
    return allFiles


def getListOfFiles(dirName):
    """
    Process list of files
    """

    # Get the list of all files
    allFiles = getListOfFilesHelper(dirName)

    # Sort paths
    allFiles.sort()

    # Remove given path
    allFiles = [fil.replace(dirName, '') for fil in allFiles]

    # Return parsed data
    return build_nested(allFiles)


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

    # Try to convert if does not fail, its a number
    try:
        int(s, 16)
        return True

    except:
        # If fails, its not a number
        return False


def tryToRound(val, elems):
    """
    Try to round the passed value if is float, otherwise return the value itself.
    """

    # Try to round the value
    try:
        # Evaluate the value
        value = literal_eval(val)

        # If is flagged as integer
        if isinstance(value, int):
            # Return the value, since its impossible to rount an integer
            return val

        # Return the number rounded
        return round(value, elems)

    except:
        # Its not a number, so its impossible to round return it
        return val

# endregion

# region Download


def downloadPOST(request):
    """
    Function to download a file with POST info
    """

    # Load the .csv data
    data = parseCSV()

    # Read get data
    lineId = request.GET.get('id')

    # If no get is passed
    if not lineId:
        # Stop!
        raise Http404("Invalid or null ID")

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = FilesSubfiles(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # Read which choices were made
            ids = literal_eval(form.cleaned_data['choices'])

            # Create the response object being an application/x-gzip
            response = HttpResponse(content_type='application/x-gzip')

            # Add the file on it
            response['Content-Disposition'] = 'attachment; filename=datas.tar.gz'

            # Create a tar file passing the response as path
            tar = tarfile.open(fileobj=response, mode="w:gz")

            # Create a path set
            paths = set()

            # For each id in list
            for id in ids:
                dataid = id.split('-')
                logger.warn(id)

                # If is a file (other checkboxes are purely functional, no neede data over there)
                if dataid[0] == 'lv3':
                    innerdataid = '-'.join(dataid[1:]).replace('+._.+', '/')

                    # Create the path
                    path = os.path.join(settings.FILES_DIR, ''.join(
                        ['summary/', data[0][lineId]['complex'].upper(), '/', innerdataid]))

                    # If path has not been added to tar yet
                    if path not in paths:
                        # Add it
                        tar.add(path, arcname=''.join(
                            [data[0][lineId]['complex'].upper(), '/', innerdataid]))

                    # Add the path to paths set
                    paths.add(path)

            logger.warn(paths)
            # Close the tar
            tar.close()

            # Return the response
            return response

    # Parse histogram
    histogram = parseHistogram()

    # Parse time series
    timeSeries = parseTimeseries()

    # Parametrize min and max values
    minlimit = 0
    maxlimit = None

    # Get images for line2d, heatmap, distrib and facet graphics
    line2d = simplePlot(minlimit, maxlimit)
    heatmap = heatMap(minlimit, maxlimit)
    distrib = distribStrip(minlimit, maxlimit)
    facet = facetGrids(minlimit, maxlimit)

    path = os.path.join(settings.FILES_DIR, ''.join(
        ['summary/', data[0][lineId]['complex'].upper(), '/']))
    fileTree = getListOfFiles(path)
    # logger.warn((', '.join("{fname} {lname}".format_map(p) for p in a)))

    # Put it all in variables
    variables = {
        "histForm": HistForm,
        "2DmapForm": TwodmapFormLine,
        "2DheatForm": TwodmapFormHeat,
        "2DdistribForm": TwodmapFormDistrib,
        "2DfacetForm": TwodmapFormFacet,
        "filesSubfilesForm": FilesSubfiles,
        'info': data[0][lineId],
        'keys': data[1],
        'fileTree': fileTree,
        'bigID': lineId,
        'histogram': histogram,
        'timeSeries': timeSeries,
        'line2d': line2d,
        'heatmap': heatmap,
        'distrib': distrib,
        'facet': facet
    }

    # Render it
    return render(request, 'complexTable/detailedInfo.html', variables)


def download(request):
    """
    Function to download a file
    """

    # Create file path
    file_path = os.path.join(
        settings.FILES_DIR, 'summary/BCD-ACA/resp/complex/complex.prmtop')

    # Call download function
    downloadFile(file_path)


def downloadFile(path):
    """
    Download a file trough http procotol from given path
    """

    # If file exists
    if os.path.exists(path):
        # Open it
        with open(path, 'rb') as fh:
            # Create a respose objects with the file being an application/octet-stream
            response = HttpResponse(
                fh.read(), content_type="application/octet-stream")

            # Add content to it (the file)
            response['Content-Disposition'] = 'inline; filename=' + \
                os.path.basename(path)

            # Return it
            return response

    # If file has not been found, throw a 404
    raise Http404("File not Found")


def downloadFiles(request):
    """
    Function to download data from complexTable page
    """

    # Load the .csv data
    data = parseCSV()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = CheckForm(request.POST)

        # check whether it's valid:
        if form.is_valid():

            # Read which choices were made
            ids = form.cleaned_data['choices']

            # Create the response object being an application/x-gzip
            response = HttpResponse(content_type='application/x-gzip')

            # Add the file on it
            response['Content-Disposition'] = 'attachment; filename=datas.tar.gz'

            # Create a tar file passing the response as path
            tar = tarfile.open(fileobj=response, mode="w:gz")

            # Create a path set
            paths = set()

            # For each id in list
            for id in ids:
                # If data is in the list
                if not isinstance(data[0][id], list):
                    # Add its path
                    path = os.path.join(settings.FILES_DIR, ''.join(
                        ['summary/', data[0][id]['complex'].upper(), '/']))

                    # If path has not been added to tar yet
                    if path not in paths:
                        # Add it
                        tar.add(path, arcname=data[0][id]['complex'].upper())

                    # Add the path to paths set
                    paths.add(path)

            # Close the tar
            tar.close()

            # Return the response
            return response

    # Add needed variables to dictionary
    variables = {
        "checkForm": CheckForm,
        'table': data[0],
        'keys': data[1]
    }

    # Return the response
    return render(request, 'complexTable/complexTable.html', variables)

# endregion

# region Filters


@register.filter
def get_type(value):
    """
    Return the type of a given value
    """
    return type(value)


@register.filter
def getItem(dictionary, key):
    """
    Return an item from given dictionary
    """
    return dictionary.get(key)

# endregion


class IndexView(generic.ListView):
    """
    Class to work with index.html template
    """

    def get(self, request, **kwargs):
        """
        Get function to the class
        """

        # Render page index.html within the request and variables
        return render(request, 'complexTable/index.html')


class ComplexView(generic.ListView):
    """
    Class to work with complexTable app and complexTable.html
    """

    def get(self, request, **kwargs):
        """
        Get function to the class
        """

        # Parse the .csv
        data = parseCSV()

        # Store data in variables
        variables = {
            "checkForm": CheckForm,
            'table': data[0],
            'keys': data[1]
        }

        # Render page complexTable.html within the request and variables
        return render(request, 'complexTable/complexTable.html', variables)


class DetailedView(generic.ListView):
    """
    Class to work with complexTable app and defailedInfo.html
    """

    def get(self, request, **kwargs):
        """
        Get function to the class
        """

        # Read get data
        lineId = request.GET.get('id')

        # Parse the csv
        data = parseCSV()

        # Parse histogram
        histogram = parseHistogram()

        # Parse time series
        timeSeries = parseTimeseries()

        # Parametrize min and max values
        minlimit = 0
        maxlimit = None

        # Get images for line2d, heatmap, distrib and facet graphics
        line2d = simplePlot(minlimit, maxlimit)
        heatmap = heatMap(minlimit, maxlimit)
        distrib = distribStrip(minlimit, maxlimit)
        facet = facetGrids(minlimit, maxlimit)

        path = os.path.join(settings.FILES_DIR, ''.join(
            ['summary/', data[0][lineId]['complex'].upper(), '/']))
        fileTree = getListOfFiles(path)
        # logger.warn((', '.join("{fname} {lname}".format_map(p) for p in a)))

        # Put it all in variables
        variables = {
            "histForm": HistForm,
            "2DmapForm": TwodmapFormLine,
            "2DheatForm": TwodmapFormHeat,
            "2DdistribForm": TwodmapFormDistrib,
            "2DfacetForm": TwodmapFormFacet,
            "filesSubfilesForm": FilesSubfiles,
            'info': data[0][lineId],
            'keys': data[1],
            'fileTree': fileTree,
            'bigID': lineId,
            'histogram': histogram,
            'timeSeries': timeSeries,
            'line2d': line2d,
            'heatmap': heatmap,
            'distrib': distrib,
            'facet': facet
        }

        # Render it
        return render(request, 'complexTable/detailedInfo.html', variables)
