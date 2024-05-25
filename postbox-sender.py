import os
import boto3
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import openpyxl
import io

CHARSET = "utf-8"
SENDER = os.environ.get('FROM')
LIST_ID = os.environ.get('LIST_ID')
UNSUBSCRIBE_LINK = os.environ.get('UNSUBSCRIBE_LINK')
UNSUBSCRIBE_MAIL = os.environ.get('UNSUBSCRIBE_MAIL')
#SUBJECT = "Важная информация о нашем новом сервисе PostBox"
#TEXT = "Plain text placeholder"
#ATTACHMENT = "./attach.txt"
#RECIPIENTS = ("a@example.com", "b@example.com")
RECIPIENTS = []
BLACKLIST = []

def postbox_send(email,subject,message):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject 
    msg['From'] = SENDER 
    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')

    BODY_HTML = '''\
    <html>
    <head></head>
    <body>
    <h1>Привет!</h1>
    <p>''' + message +'''\
    </p><p><small><small>
    <a href="''' + UNSUBSCRIBE_LINK + '?email=' + email + '&l=' + LIST_ID + '''"\
    >Отписаться</a></small></small></p>
    </body>
    </html>
    ''' 
    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(message.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    # Add the text and HTML parts to the child container.
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    #att = MIMEApplication(open(ATTACHMENT, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    #att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)

    # Add the attachment to the parent container.
    #msg.attach(att)
    msg.add_header('List-Unsubscribe','<' + UNSUBSCRIBE_LINK + '?email=' + email + '&l=' + LIST_ID + '>, <mailto: ' + UNSUBSCRIBE_MAIL + '?subject='+ email.replace('@','%40') + '&body=' + LIST_ID +'>')
    msg.add_header('List-Unsubscribe-Post','List-Unsubscribe=One-Click')
    msg.add_header('List-ID', '<' + LIST_ID + '>')

    try:
        #Provide the contents of the email.
        response = client.send_email(
            FromEmailAddress=SENDER,
            Destination={'ToAddresses':[
                email
            ]},
            Content={'Raw':
                        {
                            'Data':msg.as_string(),
                        },
            }                    
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID: " + response['MessageId']),
    time.sleep(1)

if os.path.exists('/function/storage/bucket/bulkemail.xlsx'):
   wb = openpyxl.load_workbook ('/function/storage/bucket/bulkemail.xlsx')
   sheet = wb.worksheets[0]
   for row in sheet:
       RECIPIENTS.append(row[2].value) 
   #print (RECIPIENTS)

if os.path.exists('/function/storage/bucket/blacklist.xlsx'):
    wb_bl = openpyxl.load_workbook ('/function/storage/bucket/blacklist.xlsx')
    sheet_bl = wb_bl.worksheets[0]
    for row in sheet_bl:
        BLACKLIST.append(row[0].value) 
    #print (BLACKLIST)

# The email body for recipients with non-HTML email clients.
#BODY_TEXT = TEXT
# The HTML body of the email.

# Create a new SES resource and specify a region.
client = boto3.client(service_name='sesv2', endpoint_url='https://postbox.cloud.yandex.net', region_name='ru-central1')

RECIPIENTS = list(set(RECIPIENTS) - set(BLACKLIST))
print (RECIPIENTS)

for row in sheet:
    if (row[2].value in RECIPIENTS):
        postbox_send(row[2].value,row[0].value,row[1].value)
      
if os.path.exists('/function/storage/bucket/bulkemail.xlsx'):
   os.rename('/function/storage/bucket/bulkemail.xlsx', '/function/storage/bucket/bulkemail.xlsx' + '_done')

def handler(event, context):
    return {
        'statusCode': 200,
        'body': 'ok!',
    }
