import requests, copy
from config import secrets, settings
from .misc import list_views

#  Odpytanie serwera o konto
def read_account(account_id: str):
    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }
    
    # Wykonanie żądania GET do API
    response = requests.get(
        f'{settings.api_url}/accounts/{account_id}?include=owner',
        headers=headers
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 200:
        account_data = response.json()
        return account_data, response
    else:
        print(f'Błąd: {response.status_code}')
        print(response.text)
        return None, response
    

# aktualizacja danych konta na podstawie wprowadzonych danych
def update_account(account_id: str, payload: dict):

    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id,
        'Content-Type': 'application/json'
    }
    
    # Wykonanie żądania PATCH do API
    response = requests.patch(
        f'{settings.api_url}/accounts/{account_id}',
        json=payload,
        headers=headers
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 200:
        account_data = response.json()
        return account_data, response
    else:
        print(f'\nBłąd: {response.status_code}')
        print(response.text)
        return None, response


def backup_updated_fields(accountId: str, updateData: dict, backup_data: dict, response_data: dict):
    """
        Tworzy kopię zapasową tylko tych pól, które będą aktualizowane.
    """
    try:
        account, response = read_account(accountId)
        assert response.status_code == 200, f"Status code from response is {response.status_code}"
        if accountId not in backup_data:
            backup_data[accountId] = {key: account.get(key) for key in updateData}
            response_data[accountId] = copy.deepcopy(account)
        else:
            print(f"\rWpis dla {accountId} już istnieje.\t", end='')
        return account

    except Exception as e:
        print(f"\rBłąd odczytu konta {accountId}: {e}")
        return None


def restore_updated_fields(accountId: str, backup_data: dict):
    """
        Przywraca tylko te pola, które były zmieniane.
    """
    if accountId in backup_data:
        original_data = backup_data[accountId]
        try:
            account, response = update_account(accountId, original_data)

            assert response.status_code == 200, f"Status code from response is {response.status_code}"

            print(f"\rPola {list(original_data.keys())} dla konta {accountId} zostały przywrócone.", end='')

        except Exception as e:
            print(f"\nBłąd odczytu konta {accountId}: {e}")
            return None
    else:
        print(f"Brak kopii zapasowej dla konta {accountId}.")


def _count_accounts(view: str):
    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id
    }
    
    # Wykonanie żądania GET do API
    response = requests.get(
        f'{settings.api_url}/accounts/count?viewId={view}',
        headers=headers
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 200:
        account_data = response.json()
        return account_data, response
    else:
        print(f'Błąd: {response.status_code}')
        print(response.text)
        return None, response

def list_accounts(view: str, limit = 100, field_list = ['id', 'accountName','cf_account_id']):

    views, _ = list_views()
    viewId = views[view]
    count, _ = _count_accounts(viewId)
    fields = ','.join(field_list)
    # Nagłówki żądania
    account_data = []
    for index in range(1,int(count['count']),limit):
        headers = {
            'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
            'orgId': secrets.org_id
        }
        # Wykonanie żądania GET do API
        response = requests.get(
            f'{settings.api_url}/accounts?limit={limit}&viewId={viewId}&from={index}&fields={fields}',
            headers=headers
        )
        # Sprawdzenie odpowiedzi
        if response.status_code == 200:
            data = response.json()
            account_data.extend(data['data'])
        else:
            print(f'Błąd: {response.status_code}')
            print(response.text)
    return account_data

def associate_sla(account_id: str, associate: bool, sla_id:str):
    # Nagłówki żądania
    headers = {
        'Authorization': f'Zoho-oauthtoken {secrets.access_token}',
        'orgId': secrets.org_id,
        'Content-Type': 'application/json'
    }
    payload = {
        'associate' : str(associate)
    }
    # Wykonanie żądania POST do API
    response = requests.post(
        f'{settings.api_url}/accounts/{account_id}/sla/{sla_id}',
        headers=headers,
        json=payload        
    )
    
    # Sprawdzenie odpowiedzi
    if response.status_code == 204:
        return None
    else:
        print(f'Błąd: {response.status_code}')
        print(response.text)
        return response
    
def apply_sla(account_id: str, sla_id:str):
    account_data, response = read_account(account_id)
    print(f"For accountID {account_id}", end='')
    if account_data['associatedSLAIds'] is None:
        current_sla = ''
    else:
        assert len(account_data['associatedSLAIds']) <2, "Przypisane więcej niż 1 SLA"
        current_sla = account_data['associatedSLAIds'][0]
    if sla_id != current_sla:
        if current_sla != '': 
            associate_sla(account_id=account_id, sla_id=current_sla, associate=False)
            print(f", SLA {current_sla} is removed ", end='')
        if sla_id != '':
            associate_sla(account_id=account_id, sla_id=sla_id, associate=True)
            print(f", SLA {sla_id} is applied ", end='')

    else:
        print(", there are no SLA changes", end='')

    print(".")