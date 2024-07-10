import requests
from django.conf import settings


def send_notification(payload, type, message, token):
    url = settings.NOTIFICATION_SERVICE_URL
    data = {
        'payload': payload,
        'type': type,
        'message': message
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Log the data and headers
    print(f"Sending notification to {url} with data: {data} and headers: {headers}")
    
    response = requests.post(url, json=data, headers=headers)
    
    # Log the response status and content
    print(f"Notification response status: {response.status_code}, response content: {response.content}")
    
    response.raise_for_status()
