import xmltodict

with open("1.xml") as fd:
    doc = xmltodict.parse(fd.read())

xmin = int(doc['annotation']['object']['bndbox']['xmin'])
xmax = int(doc['annotation']['object']['bndbox']['xmax'])
ymin = int(doc['annotation']['object']['bndbox']['ymin'])
ymax = int(doc['annotation']['object']['bndbox']['ymax'])

print("xmin: " + str(xmin))
print("xmax: " + str(xmax))
print("ymin: " + str(ymin))
print("ymax: " + str(ymax))