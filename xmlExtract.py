import xmltodict

with open("multiple-objects.xml") as fd:
    doc = xmltodict.parse(fd.read())

subDoc = doc['annotation']['object']

print(subDoc) #subDoc contains the info for EACH object. a For loop onto the doc will seperate out the info.

#This will print out multiple objects.
for labeledObject in doc['annotation']['object']:
    print(str(labeledObject['bndbox']))


#print(doc['annotation']['object'][0]['bndbox']['xmin'])
#print(doc['annotation']['object'][1]['bndbox']['xmin'])
#print(doc['annotation']['object'][2]['bndbox']['xmin'])
#print(doc['annotation']['object'][3]['bndbox']['xmin'])

#xmin = doc['annotation']['object']['bndbox']['xmin']
#xmax = doc['annotation']['object']['bndbox']['xmax']
#ymin = doc['annotation']['object']['bndbox']['ymin']
#ymax = doc['annotation']['object']['bndbox']['ymax']

#print("xmin: " + xmin)
#print("xmax: " + xmax)
#print("ymin: " + ymin)
#print("ymax: " + ymax)