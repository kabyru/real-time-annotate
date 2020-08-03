# Real Time Annotation Tool for Constantly Positioned Objects
## Developed by Kaleb Byrum for Raytheon Technologies, Missiles & Defense
### This tool intends to speed up the annotation process by making the assumption that objects being labeled are constant in position and lighting. This assumption is helpful in creating Object Detection systems in industrial environments.

## Introduction
Custom Object Detection tasks empowered by TensorFlow models are created by introducing a TensorFlow training program to multitudes of *labeled* images that identify for the computer that is within the image it is analyzing. Using these labeled images, a TensorFlow training program outputs a **model** file which is used in a driving program that performs object identification, either through taken images or in real-time using a connected camera.

The task of *labeling raw images* is a cumbersome task. For a one-man show, it is an ***even more cumbersome task.*** So, in order to minimize the time necessary to prepare the training of a TensorFlow Object Detection model, this program automatically annotates images while taking the images that will be used as input.

This is possible by using *one hand-annotated image as input*, which serves as a template for the rest of the images within the training set. *This process reduces the data collection and annotation process to one that takes minutes.*

## How it works
Real-Time Annotation can be separated into two steps:
- Hand-Annotation of *one* image of the training set you intend to real-time annotate.
- Set the configurations of the program by modifying the *config .yaml* file.
- The execution of *real-time-annotate .py* program, which will read the hand-annotated XML to generate a shape for which to fit the new input images.

The hand-annotated image must be annotated in XML format, which is standard for individual TensorFlow annotations. Hand-annotations can be created using the [**LabelImg** tool, which is available on GitHub.](https://github.com/tzutalin/labelImg)

There are three configurations to consider within *config .yaml*:
- The width and height of the images within your training set.
- The counter for which to start. (if you are starting on the first labeled set, this can be 0 or 1, but you would want to change this to the next starting number when you get to the next labeled set, to prevent overwrite.)
- The XML file to use as a template. This file path should lead to the XML file hand-annotated in Step 1.

**real-time-annotation .py** can be executed on the command line, and takes no input parameters. The parameters used by the program are held within **config .yaml.**

Upon execution, the program first initiates the webcam stream which will be used to take images of the labeled set. The program makes use of the first webcam available, and can be modified in the code should another webcam be used. After ensuring a webcam is available and can be used, the program then begins extracting the contents of the hand-annotated XML, looking for the bounding-box coordinates of the object, as well as the width and height of the image.

For generated annotation XML files from this template, the bounding box coordinates are not modified, rather the file names, file path, and the folder names are modified for each image. This ensures that TensorFlow sees the template image and the real-time image taken are unique images to consider.

**To take images and create annotations within the program, press the 's' key. Check the terminal to confirm that the image has been taken.Images are saved to the current working directory.**

These XMLs are then ready for conversion to CSV, once the program has been run for each labeled set. [Refer to this guide to continue on with the next steps of creating a TensorFlow Custom Object Detection Model](https://towardsdatascience.com/custom-object-detection-using-tensorflow-from-scratch-e61da2e10087)
