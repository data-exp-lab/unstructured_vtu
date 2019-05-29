import numpy as np
import zlib
import base64
import xmltodict

def decode_binary(blob, zlib = True):
    split_location = blob.find(b"==") + 2
    first = base64.decodebytes(blob[:split_location])
    second = base64.decodebytes(blob[split_location:])
    if zlib:
        second = zlib.decompress(second)
    return np.frombuffer(first, dtype="<f4"), np.frombuffer(second, dtype="<f4")

with open("solution-00100.0000.vtu", "rb") as fd:
#with open("test.xml", "rb") as fd:
    doc = xmltodict.parse(fd.read())

#import pprint
#with open("output.txt", "w") as fd:
#    fd.write(pprint.pformat(doc['VTKFile']['UnstructuredGrid']))

base = doc['VTKFile']['UnstructuredGrid']

# set(_['DataArray'][0]['#text'] for _ in base['FieldData'])

def parse_dataarray(node):
    array_type = node['@type']
    ncomponents = node['@NumberOfComponents']
    array_format = node['@format']
    value = node['#text']
    return decode_binary(value)

def make_piece(node):
    ncells = node['@NumberOfCells']
    npoints = node['@NumberOfPoints']
    points = parse_dataarray(node['Points']['DataArray'])
    cells = parse_dataarray(node['Cells']['DataArray'])

for piece in base['Piece']:
    print(piece['@NumberOfPoints'])
