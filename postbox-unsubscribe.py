import json
import openpyxl
import os

l = ""
email = ""

def append_to_excel(email,l,filename):
        print (email + "," + l)
        if os.path.exists(filename):
            wb_bl = openpyxl.load_workbook(filename)
            sheet_bl = wb_bl.worksheets[0]
            sheet_bl.append([email,l])
            wb_bl.save(filename)
            print(filename + " updated")
        else:
            print (filename + " not found")
            
def handler(event, context):
    #data = json.dumps(event)
    if 'messages' in event:
        print ("email reveived")
        for m in event['messages']:
            print (m['message'])
            l = m['message']
            for h in m['headers']:
                if h['name'] == 'Subject':
                    print (h['values'][0])
                    email = h['values'][0].replace('%40','@')
                    append_to_excel(email,l,'/function/storage/bucket/blacklist.xlsx')
        return {
            'statusCode': 200,
            'body': email + " unsubscribed from " + l,
        }            
    
    elif ('queryStringParameters' in event):
        print ("http request reveived")
        params = event['queryStringParameters']
        email = event['queryStringParameters']['email']
        l = event['queryStringParameters']['l']
        email = params['email']
        l = params['l']
        append_to_excel(email,l,'/function/storage/bucket/blacklist.xlsx')

        return {
            'statusCode': 200,
            'body': email + " unsubscribed from " + l,
        }

    else:
        return {
            'statusCode': 200,
            'body': 'error',
        }
    
