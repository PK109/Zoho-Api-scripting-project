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
    

def list_tags(limit = None, departmentName = "Technical support"):
    depts, _ = list_departments()
    deptId = depts[departmentName]
    # Nagłówki żądania
    tag_data = {}
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }
    index = 0
    # do - while loop
    while True:
        response = requests.get(
            f'{settings.api_url}/ticketTags?limit={limit}&departmentId={deptId}&from={index}',
            headers=headers
        )
        # Sprawdzenie odpowiedzi
        if response.status_code == 200:
            data = response.json()
            tags_cleaned = {record['id'] : record['name'] for record in data['data']}
            tag_data.update(tags_cleaned)
            print(f"Index: {index}")
            print(f"Picked {len(data['data'])} tags.")
        if len(data['data']) != limit:
            break #Exit the loop
        index += limit

    return tag_data

def list_tags(limit=None, departmentName="Technical support"):
    # If limit is None, fetch all tags
    depts, _ = list_departments()
    deptId = depts[departmentName]

    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }

    tag_data = {}
    index = 0
    page_limit = 100 if limit is None else min(limit, 100)  # use 100 max per page

    while True:
        response = requests.get(
            f'{settings.api_url}/ticketTags?limit={page_limit}&departmentId={deptId}&from={index}',
            headers=headers
        )

        if response.status_code != 200:
            print(f'Błąd: {response.status_code}')
            print(response.text)
            return None

        data = response.json()
        tags_cleaned = {record['id']: record['name'] for record in data['data']}
        tag_data.update(tags_cleaned)

        # Stop if fewer results were returned than requested (end of data)
        if len(data['data']) < page_limit:
            break

        index += page_limit

        # Stop if total collected tags reach the specified limit
        if limit is not None and len(tag_data) >= limit:
            tag_data = dict(list(tag_data.items())[:limit])
            break

    return tag_data