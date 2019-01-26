# Django imports
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.template.defaulttags import register
from django.http import HttpResponse, Http404

# Models import
from complexTable.models import Complex

from complexTable.models import PostHistogram
from complexTable.forms import HistForm

# Python imports
from ast import literal_eval
from wsgiref.util import FileWrapper

import os
import re
import csv
import json
import logging

spacing = 15

logger = logging.getLogger(__name__)

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
            response_data['histData'] = histogram
            

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
            
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def isHex(s):
    try:
        int(s, 16)
        return True

    except:
        return False

def readfile(path):
    info = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            datas = list(filter(None, re.split(',| |\t|\n', line)))
            parsedLine = []

            for data in datas:
                if isHex(data):
                    parsedLine.append(data)
                else:
                    try:
                        parsedLine.append(literal_eval(data))
                    except:
                        parsedLine.append(data)

            info.append(parsedLine)
            
    return info

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

    for index, line in enumerate(datas):
        line.insert(0, "Data "+ str(index))

    return {"names": names, "datas": datas, "dsize": datasize}

# Function to round floats
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


def download(request):
    """
    Function to download a file
    """
    file_path = os.path.join(settings.FILES_DIR, 'summary/BCD-ACA/resp/complex/complex.prmtop')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404("File not Found")

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
                    localData[key] = tryToRound(value, 2)

        # dataInfo.append(localData)
        dataInfo[str(idx)] = localData

    keys = reader.fieldnames
    keys[keys.index("")] = "ID"

    return (dataInfo, keys)

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

        # @register.filter
        # def getItem(dictionary, key):
        #     return dictionary.get(key)

        def get(self, request, **kwargs):
            # we will pass this context object into the
            # template so that we can access the data
            # list in the template
            
            data = parseCSV()

            variables = {
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

        variables = {
            "histForm": HistForm,
            'info': data[0][lineId],
            'keys': data[1],
            'bigID': lineId,
            #'histogram': json.dumps(histogram),
            'histogram': histogram
            }

        return render(request, 'complexTable/detailedInfo.html', variables)