# enable lambda proxy for the methods,timeout:15 mins
#when you test for GET send the data through query params ie:url?name=zubair or give in key, value in params
import json

data_list = []

def lambda_handler(event, context):
    
    print("event is ================",type(event),event)
    
    http_method = event['httpMethod']
    print('http_method-------------',http_method)
    
    if http_method == 'POST':
        body = json.loads(event['body'])
        print('body--------',type(body),body)
        name = body.get('name')
        place = body.get('place')
        
        data = {
            'name': name,
            'place': place
        }
        
        data_list.append(data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data added successfully'})
        }
    
    elif http_method == 'GET':
        query_params = event.get('body', {})
        print("query_params and its type", query_params, type(query_params))
        name = query_params['name']
        
        if name:
            filtered_data = [item for item in data_list if item.get('name') == name]
            
            return {
                'statusCode': 200,
                'body': json.dumps(filtered_data)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps(data_list)
            }
    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid HTTP method'})
        }
