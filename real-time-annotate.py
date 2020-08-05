#To engage with the webcam
from _thread import *
import cv2
from imutils.video import VideoStream
import imutils as im

#Engage with LabelImg XML
import xmltodict
import pathlib
import os

#Engage with config file.
import yaml
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

def saveFrame(frame, counter, doc):
    fileName = str(counter) + ".jpg"
    xmlName = str(counter) + ".xml"
    cv2.imwrite(fileName,frame)
    print("Frame saved as " + fileName)

    #Change values for this new image's annotation file, using the original as a template.
    doc['annotation']['filename'] = fileName
    filePath = pathlib.Path.cwd() / fileName
    doc['annotation']['path'] = filePath

    folderName = os.path.dirname(filePath)
    folderName = os.path.basename(folderName)
    doc['annotation']['folder'] = str(folderName)

    #Test out unparsing
    print(xmltodict.unparse(doc, pretty=True))
    f = open(xmlName, "w")
    f.write(xmltodict.unparse(doc, pretty=True))
    f.close()
    print("File " + xmlName + " written!")



def XMLExtract():
    print("Opening " + str(config['xml_to_extract']) + " and extracting bounding box coords..." )
    with open(config['xml_to_extract']) as fd:
        doc = xmltodict.parse(fd.read())
    xmin = int(doc['annotation']['object']['bndbox']['xmin'])
    xmax = int(doc['annotation']['object']['bndbox']['xmax'])
    ymin = int(doc['annotation']['object']['bndbox']['ymin'])
    ymax = int(doc['annotation']['object']['bndbox']['ymax'])

    print("Extracted coords: ")
    print("xmin: " + str(xmin))
    print("xmax: " + str(xmax))
    print("ymin: " + str(ymin))
    print("ymax: " + str(ymax))

    print("Extracting size of image and setting camera resolution to that size...")
    width = int(doc['annotation']['size']['width'])
    height = int(doc['annotation']['size']['height'])

    #Test out unparsing
    print(xmltodict.unparse(doc, pretty=True))

    return doc, xmin, xmax, ymin, ymax, width, height

def XMLExtractMultiple():
    print("Opening " + str(config['xml_to_extract']) + " and extracting bounding box coords..." )
    with open(config['xml_to_extract']) as fd:
        doc = xmltodict.parse(fd.read())
    subDoc = doc['annotation']['object'] #Contains the 'object' information from the XML file, for each labeled object.
    
    print("Extracting size of image...")
    width = int(doc['annotation']['size']['width'])
    height = int(doc['annotation']['size']['height'])

    #Test out unparsing
    #print(xmltodict.unparse(doc, pretty=True))
    #print(subDoc)

    return doc, subDoc, width, height

def webcam_handler_multiple():
    vs = VideoStream().start() #Opens the first webcam it finds
    #Retreive the bndbox coords from each labeled object.
    doc, subDoc, width, height = XMLExtractMultiple()
    color = (255, 0, 0)
    thickness = 2
    counter = int(config['counter'])
    while True:
        key = cv2.waitKey(1) & 0xFF

        frame = vs.read()
        frame = im.resize(frame, height=height)
        frame = im.resize(frame, width=width)

        #Now, add the rectangles as per the bndboxes within the XML file...
        for labeledObject in subDoc:
            #print(labeledObject)
            xmin = int(labeledObject['bndbox']['xmin'])
            xmax = int(labeledObject['bndbox']['xmax'])
            ymin = int(labeledObject['bndbox']['ymin'])
            ymax = int(labeledObject['bndbox']['ymax'])

            start_point = (xmin, ymin)
            end_point = (xmax, ymax)

            rectangleFrame = cv2.rectangle(frame, start_point, end_point, color, thickness)
        
        cv2.imshow("Real-Time Annotate", rectangleFrame)

        if key == ord("q"):
            break

        if key == ord("s"):
            svFrame = vs.read()
            svFrame = im.resize(svFrame, height=height)
            svFrame = im.resize(svFrame, width=width)
            saveFrame(svFrame, counter, doc)
            counter = counter + 1
    
    cv2.destroyAllWindows()
    vs.stop()


def webcam_handler():
    vs = VideoStream().start() #Opens the first webcam it finds.
    #Retreive the coords from the XML file.
    doc, xmin, xmax, ymin, ymax, width, height = XMLExtract()
    start_point = (xmin,ymin)
    end_point = (xmax, ymax)
    color = (255, 0, 0)
    thickness = 2
    counter = int(config['counter'])
    while True:
        key = cv2.waitKey(1) & 0xFF

        frame = vs.read()
        frame = im.resize(frame, height=height)
        frame = im.resize(frame, width=width)
        #originalFrame = frame

        #Now, add the rectangle from the XML file.
        rectangleFrame = cv2.rectangle(frame, start_point, end_point, color, thickness)

        cv2.imshow("Real-Time Annotate", rectangleFrame)

        if key == ord("q"):
            break
        
        if key == ord("s"):
            svFrame = vs.read()
            svFrame = im.resize(svFrame, height=height)
            svFrame = im.resize(svFrame, width=width)
            saveFrame(svFrame, counter, doc)
            counter = counter+1
    
    cv2.destroyAllWindows()
    vs.stop()

if config['multiple-objects-in-file'] == True:
    webcam_handler_multiple()
else:
    webcam_handler()
