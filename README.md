# busTrackingSystem
This repository has the step by step procedures and driver codes for building busTrackingSystem using AWS services

# Steps to be followed:

  # 1, IAM role for lambda:
  
* Go to IAM service. Click on **"Create Role"**
* Choose "AWS Service" under trusted entity type.
* In this case, we require AWS Lambda to read and write data to and from Dynamodb along with publishing the message to SNS.
* Hence, attach the policies accordingly. For example, "AWSLambdaInvocation-DynamoDB" can be attached and then give a suitable name. You can further attach the policies at this section also.


  # 2, AWS Lambda:

* Create a **lambda function**
* Give a suitable name under "Function Name"
* Choose the suitable Runtime: "Python 3.10" and Architecture: "x86_64"
* Under the "Change default execution role", choose use existing role and give the role that we have created in step 1.
* In the code section, paste the content of "lambda_function.py".
* Also Configure the test event. Click on "Configure test event". Choose "Create test event". Give a suitable name and choose "Private". Under the Event JSON, paste the following test event: "{\"Lat\": 10.5, \"Long\": 11.1}"
* Deploy the lambda function for all the changes to reflect


  # 3, AWS IoT - Device side preparation: 

* Login to the AWS Management Console with your IAM credentials which has autorisation to fully access the following AWS Services: IoT, Lambda, DynamoDB, SNS
* Go to the **AWS IoT Core service**
* Click on the "Connect one device" option in the navigation section
* Read and follow the "Prepare your device" section that pops up and then click "Next"
* "Register and secure your device" section appears. 
* Here choose "Create a new Thing"
* Give a name for your device and then click "Next"
* Under the "Device Platform OS" section, choose your appropriate Platform. I have chosen "Linux/MacOS" for this demo.
* Under the "AWS IoT Device SDK" section. choose "Python" and then click "Next".
* Follow the steps under "Download connection kit". 
* Once the download complete. Unzip the folder and then give the "execute"  permission for the "start.sh" file, as mentioned "Run connection kit".
* Execute the "./start.sh" file. You will see the required certificates and SDKs being installed. Once the device started publishing the data. Stop the execution.
* Now go to the following path and open the file for editing: "aws-iot-device-sdk-python-v2/samples/pubsub.py" and update the "pubsub.py" file as given in this repository.
* Execute the "./start.sh" file to see the ${"Lat": 0.1, "Long": 2.1} message on the console.
  
  # 4, AWS IoT Rule Preparation:

* From the navigation pane, go to the following Rules page: AWS IoT > Message routing > Rules.
* Choose **"Create rule"**
* Give a suitable Rule name and description. Then select "Next"
* In the SQL Statement, give the below statement: "SELECT * FROM 'sdk/test/python'"
* Under the "Rule Actions". Choose an action by typing "Lambda", Select the lambda that you have created in Step 2.
* Click on Create.

  # 5, AWS SNS Topic Creation:

* Go to AWS SNS Service
* Choose **"Topics > Choose Topic"**
* Choose "Standard" Type
* Provide "Name" and "Display Name"
* Once the Topic is created, click on "Subscription". Choose "Email" under protocol and enter your "Email address" in the  Endpoint field . Click on "Create Subscription". 
* You would have received the Notification from AWS SNS Service. Click on the link to subscribe for the topic.
* Go back to the Topic that you have just created. And then copy the topic ARN. Now paste the topic ARN in the lambda code that you have created at Step no 4.
* To validate the above Setting, Click on the Test option in the AWS lambda function that you have created. You should receive an email to the subscribed email ID.

  # 6, AWS DynamoDB table:

* Go to AWS DynamoDB service.
* Choose **"Tables > Create Table"**
* Give the table name as "bus_live_location"
* Give "bus_id" as Partition key and "timestamp" as Sort Key. Then create the table with default setting

  # 7, AWS API Gateway:

* Go to AWS API Gateway.
* Choose **"API> Create API"**
* Choose Rest API > Build > New API
* Give a suitable name and choose Regional Option and then click "Create API"
* Click on the create resource and then create the resource as "bus-location"
* Later create one more resource under it using "{bus_id}"
* Under the "{bus_id}" resource, click the create method option.
* Enter the following detail
  - Method type : Get
  - Integration type: AWS Service
  - AWS Region: Your region
  - AWS service: DynamoDB
  - HTTP method: POST
  - Action type: Use action name
  - Action name: Query
  - Execution role: Create a role for APIGateway to query the dynamodb table and use it here
  - Request body passthrough: When no template matches the request content-type header
  - Mapping templates:
      - application/json
      - Template body:
      -   {
            "TableName": "bus_live_location", 
            "PrimaryKey":"bus_id",
            "SortKey":"timestamp",
            "KeyConditionExpression": "bus_id = :v1", "ExpressionAttributeValues": {   
                    ":v1": {        
                        "S": "$input.params('bus_id')"   
                    }    
                },
            "Limit":1, 
            "ScanIndexForward":false 
            }
* Deploy the api with stage name as "test"

# Demo: 

* Now from your device, run the "./start.sh" file. This should publish the message in the 'sdk/test/python' topic. This will trigger the Lambda code that you have created. 
Eventually, after the suitable processing the message will be published to the subscribed email id.
* Use the API that was created in the step 7 on your browser to get the current location of the bus.

