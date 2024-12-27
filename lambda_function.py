import boto3
import json
from datetime import datetime
import traceback


dynamodb = boto3.client('dynamodb')
sns_email = boto3.client("sns")



def get_proximity_status(received_latitude, received_longitude, my_latitude, my_longitude):
    """
    Determines how close the bus has come
    from the starting location to the current destination
    :param received_latitude: Bus's Lattitude co-ordinates
    :param received_longitude: Bus's Longitude co-ordinates
    :param my_latitude: Current Lattitude co-ordinates
    :param my_longitude: Current Longitude co-ordinates
    :return: proximity status of the bus reative to the current location
    """
    received_avg_location = (received_latitude + received_longitude) // 2
    current_avg_location = (my_latitude + my_longitude) // 2
    avg_location_delata = received_avg_location - current_avg_location
    if avg_location_delata < -2:
        return "Approaching"
    elif -2 <= avg_location_delata < 5:
        return "Reached"
    elif avg_location_delata >= 5:
        return "Left"
    else:
        return False


def update_table(received_latitude, received_longitude):
    """
    Makes entry into the bus_live_location dynamodb table
    :param received_latitude: Bus's Latitude co-ordianates from the GPS device
    :param received_longitude: Bus's Longitude co-ordianates from the GPS device
    :return: 
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    item_str = {'bus_id': {'S': '1001'}, 'timestamp': {'S': current_time}, 'Latitude': {'S': str(received_latitude)},
                'Longitude': {'S': str(received_longitude)}}
    dynamodb.put_item(TableName='bus_live_location', Item=item_str)


def lambda_handler(event, context):
    """
    The lambda invocation starts here
    :param event: Data received by the AWS Lambda service
    :param context:  Information about the invocation, function, and execution environment
    :return: event which has the Bus's GPS co-ordinates
    """

    my_latitude = 10.1
    my_longitude = 12.1

    received_latitude = json.loads(event).get("Lat")
    received_longitude = json.loads(event).get("Long")

    try:
        update_table(received_latitude, received_longitude)
    except Exception as e:
        traceback.print_exception(type(e), value=e, tb=e.__traceback__)

    try:
        proximity = get_proximity_status(received_latitude, received_longitude, my_latitude, my_longitude)
    except Exception as prox_ex:
        traceback.print_exception(type(e), value=prox_ex, tb=e.__traceback__)
    
    if proximity:
        message_str = "Your Bus {} your destination point".format(proximity)
           
    else:
        message_str = "Issue with your Bus's GPS tracking system"
        

    try:
        sns_email.publish(
            TopicArn="<Your Topic ARN>",
            Message=message_str,
            Subject="Live Bus Tracking",
        )
    except Exception as sns_ex:
        traceback.print_exception(type(e), value=sns_ex, tb=e.__traceback__)
        
        
    return event
