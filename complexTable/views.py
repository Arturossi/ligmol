
# Django imports
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.template.defaulttags import register
from django.http import HttpResponse, Http404

# Models import
from complexTable.models import Complex

# Python imports
from ast import literal_eval
from wsgiref.util import FileWrapper

import os

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
    import csv

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

        @register.filter
        def getItem(dictionary, key):
            return dictionary.get(key)

        def get(self, request, **kwargs):
            # we will pass this context object into the
            # template so that we can access the data
            # list in the template
            
            data = parseCSV()

            return render(request, 'complexTable/complexTable.html', {'table': data[0], 'keys': data[1]})

class DetailedView(generic.ListView):
    def get(self, request, **kwargs):

        lineId = request.GET.get('id')

        data = parseCSV()

        return render(request, 'complexTable/detailedInfo.html', {'info': data[0][lineId], 'keys': data[1], 'bigID': lineId})