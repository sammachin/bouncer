from chalice import Chalice
import boto3
import nexmo
import requests
import os


NEXMO_APP_ID = os.environ['NEXMO_APP_ID']
S3_BUCKET = os.environ['S3_BUCKET']
REGION = os.environ['REGION']
EMAIL_TO = os.environ['EMAIL_TO']
EMAIL_FROM = os.environ['EMAIL_FROM']


app = Chalice(app_name='bouncer')
app.debug = False
client = nexmo.Client(application_id=NEXMO_APP_ID, private_key="private.key")
S3 = boto3.client('s3')
SES = boto3.client('ses',region_name=REGION)


@app.route('/ncco', methods=['POST'])
def ncco():
    data = app.current_request.json_body
    headers = app.current_request.headers
    print(data)
    url = "https://" + headers['host'] + "/api/recording"
    print(url)
    rncco =  [{
            		"action": "record",
            		"eventUrl": [url]
            	},
            	{
            		"action": "connect",
            		"from": data['to'],
            		"endpoint": [{
            			"type": "phone",
            			"number": data['from']
            		}]
            	}
            ]
    print(rncco)
    return rncco


@app.route('/recording', methods=['POST'])
def recording():
    data = app.current_request.json_body
    key = "bouncer/"+data['conversation_uuid']+".mp3"
    headers =  client._Client__headers()
    response = requests.get(data['recording_url'], headers=headers)
    S3.put_object(
            Bucket=S3_BUCKET,
            Key=key,
            Body=response.content,
            ContentType='audio/mp3'
            )
    S3.put_object_acl(ACL='public-read', Bucket=S3_BUCKET, Key=key)
    SES.send_email(
            Destination={'ToAddresses': [EMAIL_TO],},
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': 'https://{}/{}'.format(S3_BUCKET, key) ,
                    },
                },
                'Subject': {'Charset': 'UTF-8', 'Data': 'New Bouncer Recording',
                },
            },
            Source=EMAIL_FROM
            )
    return "ok"

    
@app.route('/event', methods=['POST'])
def event():
    data = app.current_request.json_body
    print(data)
    return "ok"