# Computer-Pointer-Controller
Control your mouse pointer with your eyes

## Description

This project use the [Gaze Estimation model](https://docs.openvinotoolkit.org/latest/_models_intel_gaze_estimation_adas_0002_description_gaze_estimation_adas_0002.html) to estimate the gaze of the user's eyes and change the mouse pointer position accordingly.

It runs multiple models in the same machine and coordinate the flow of data between those models.

![](resources/pipeline.png?raw=true)

## Prerequisites

You need OpenCV and Intel's OpenVino toolkit installed on your machine.

* [OpenCV](https://opencv.org) - The simple install should look like `pip install opencv-python`.
* [OpenVino toolKit](https://software.intel.com/en-us/openvino-toolkit) - See website for installation depending of your configuration.

### Models download

With the help of the OpenVino toolkit, you'll have to download the 4 models used in this project.
The default values in the code suppose you execute these commands from the "model" directory.

You'll end up with a directory structure like this :

![](resources/models_tree.png)

But you are of course free to use any compatible model, and specify these with the corresponding parameters.

#### Windows syntax example

This will download the models in all precisions available. You can add a ```--precisions``` argument if you only want a specific precision.
These example are for the default installation of OpenVino 2020.2.117
```
python "C:\Program Files (x86)\IntelSWTools\openvino_2020.2.117\deployment_tools\tools\model_downloader\downloader.py" --name face-detection-adas-binary-0001
python "C:\Program Files (x86)\IntelSWTools\openvino_2020.2.117\deployment_tools\tools\model_downloader\downloader.py" --name head-pose-estimation-adas-0001
python "C:\Program Files (x86)\IntelSWTools\openvino_2020.2.117\deployment_tools\tools\model_downloader\downloader.py" --name landmarks-regression-retail-0009
python "C:\Program Files (x86)\IntelSWTools\openvino_2020.2.117\deployment_tools\tools\model_downloader\downloader.py" --name gaze-estimation-adas-0002
``` 

## Licence

These scripts are my work for the "Computer Pointer Controller" project of the Udacity "Intel® Edge AI for IoT Developers Nanodegree" Program and are based on Intel Corporation base scripts provided for the project.

They should not be used to complete your own project. Plagiarism is a violation of the Udacity Honor Code. Udacity has zero tolerance for plagiarized work submitted in any Nanodegree program.
