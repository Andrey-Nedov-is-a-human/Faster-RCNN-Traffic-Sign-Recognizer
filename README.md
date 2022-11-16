# Traffic sign recognition system with Mask-RCNN

<img src="/Release/img1.png" alt="img1" width="800"/>

*Developers*
1. [Oleg Botnar](https://github.com/fronos)
2. [Andrey Nedov](https://github.com/Andrey-Nedov)


## Task
Make a system that receives an image from the front camera of the car as input, which outputs a JSON file with markup describing the masks and classes of all road signs found in the image.

## System architecture
<img src="/Release/img2.jpg" alt="img1" width="800"/>

Communication with the system occurs on two UDP ports: <br/> 
1. UPD UI - user system configuration management console
2. UDP manager - the port on which the system receives images and sends JSON markup

## Mask-RCNN
The Mask-RCNN model was trained on a dataset composed of records from DVR cameras and marked up in the editor.

<img src="/Release/img4.png" alt="img1" width="800"/>

The trained model can be downloaded from the repository using the link [model.pt](https://drive.google.com/file/d/1vuOjKoNq4VE6BUToBDe6hceUEEWTRve_/view?usp=sharing)

## Console interface of the system

The console interface of the system (on the right) has a set of parameters that allow you to set the area of interest in the image (ROI), set the threshold for the classifier, etc.

<img src="/Release/img6.jpg" alt="img1" width="800"/>

## The result

<img src="/Release/img3.jpg" alt="img1" width="800"/>

The system was developed as part of a project to create an unmanned vehicle - one of the main projects of the IT faculty [Moscow Polytech](https://new.mospolytech.ru/) and moved on down the pipeline. Records with the result of the work could not be found, there were only a couple of test images processed by the system.




