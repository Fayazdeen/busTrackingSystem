# busTrackingSystem
This repository has the step by step procedures and driver codes for building busTrackingSystem using AWS services

Steps to be followed:

1, Login to the AWS Management Console with your IAM credentials which has autorization to fully access the following AWS Services: IoT, Lambda, DynamoDB, SNS
2, Go to the AWS IoT Core service
3, Click on the "Connect one device" option in the navigation section
4, Read and follow the "Prepare your device" section that pops up and then click "Next"
5, "Register and secure your device" section appears. 
6, Here choose "Create a new Thing"
7, Give a name for your device and then click "Next"
8, Under the "Device Platform OS" section, choose your appropriate Platform. I have choosen "Linux/MacOS" for this demo.
9, Under the "AWS IoT Device SDK" section. choose "Python" and then click "Next".
10, Follow the steps under "Download connection kit". 
11, Once the download complete. Unzip the folder and then give the "execute"  permission for the "start.sh" file, as mentioned "Run connection kit".
12, Execute the "./start.sh" file. You will see the required certificates and sdks being installed. Once the device started publishing the data. Stop the execution.
13, Now go to the following path and open the file for editing: "aws-iot-device-sdk-python-v2/samples/pubsub.py" and update the "pubsub.py" file as given in this repository.
14, Execuet the "./start.sh" file to see the ${"Lat": 0.1, "Long": 2.1} message on the console.
  
