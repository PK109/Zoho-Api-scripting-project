import requests, time
from config import secrets, settings, update_token


def obtain_token():
    """
        Use this method if you need to request for:
        - tokens for the first time
        - extended token scope 
    """

    authorization_code = input("Paste authorization code from Zoho API Console:")
    token_url = settings.oauth_url
    params = {
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'client_id': secrets.client_id,
        'client_secret': secrets.client_secret,
        'redirect_uri': secrets.redirect_uri 
    }
    response = requests.post(token_url, data=params)
    tokens = response.json()
    
    if tokens.get('access_token') is not None:
        accessToken = tokens.get('access_token')
        refreshToken = tokens.get('refresh_token')
        expires_in = tokens.get('expires_in')
        localtime = time.localtime(time.time() + expires_in)
        print('Scope:', tokens.get('scope'))
        print(f"Token expires at:\t{localtime.tm_hour:02d}:{localtime.tm_min:02d}:{localtime.tm_sec:02d}")
        update_token("access_token", accessToken)
        update_token('refresh_token', refreshToken)
        print("Token values updated")
    else:
        print("Error in authorization:")
        print(tokens)
    

def refresh_token():
    """
        Use this method if you need to request new access_token.
        It is working only for 1 hour since generation.
    """
    token_url = settings.oauth_url
    
    params = {
        'refresh_token': secrets.refresh_token,
        'grant_type': 'refresh_token',
        'client_id': secrets.client_id,
        'client_secret': secrets.client_secret,
        'redirect_uri': secrets.redirect_uri 
    }
    response = requests.post(token_url, data=params)
    tokens = response.json()
    
    if tokens.get('access_token') is not None:
        accessToken = tokens.get('access_token')
        update_token("access_token", accessToken)
        expires_in = tokens.get('expires_in')
        localtime = time.localtime(time.time() + expires_in)
        print('Scope:', tokens.get('scope'))
        print(f"Token expires at:\t{localtime.tm_hour:02d}:{localtime.tm_min:02d}:{localtime.tm_sec:02d}")
        print("Token values updated")
    else:
        print("Error in authorization:")
        print(tokens)
    