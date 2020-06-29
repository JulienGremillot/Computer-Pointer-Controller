### Download models in this directory

With the help of the OpenVino toolkit, you'll have to download the 4 models used in this project.
The default values in the code suppose you execute these commands from the "model" directory.

You'll end up with a directory structure like this :

![](../resources/models_tree.png)

But you are of course free to use any compatible model, and specify these with the corresponding parameters.

#### Windows syntax example

This will download the models in all precisions available. You can add a ```--precisions``` argument if you only want a specific precision.
These example are for the default installation of OpenVino 2020.2.117
```
python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\tools\model_downloader\downloader.py" --name face-detection-adas-binary-0001
python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\tools\model_downloader\downloader.py" --name head-pose-estimation-adas-0001
python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\tools\model_downloader\downloader.py" --name landmarks-regression-retail-0009
python "C:\Program Files (x86)\IntelSWTools\openvino\deployment_tools\tools\model_downloader\downloader.py" --name gaze-estimation-adas-0002
``` 
