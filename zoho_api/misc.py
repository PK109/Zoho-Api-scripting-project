import requests
from config import secrets, settings

def list_departments(activeDepts = True):
    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }
    
    # Wykonanie żądania GET do API
    response = requests.get(
        f'{settings.api_url}/departments?isEnabled={activeDepts}',
        headers=headers
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 200:
        dept_data = response.json()
        dept_dict = {entry["name"]: entry["id"] for entry in dept_data["data"]}
        return dept_dict, response
    else:
        print(f'Błąd: {response.status_code}')
        print(response.text)
        return None, response

def list_views(departmentName = "Technical support", module="accounts"):
    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }
    depts , response = list_departments()
    deptId = depts[departmentName]
    # Wykonanie żądania GET do API
    response = requests.get(
        f'{settings.api_url}/views?module={module}&departmentId={deptId}',
        headers=headers
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 200:
        views_data = response.json()
        view_dict = {entry["name"]: entry["id"] for entry in views_data["data"]}
        return view_dict, response
    else:
        print(f'Błąd: {response.status_code}')
        print(response.text)
        return None, response
    

