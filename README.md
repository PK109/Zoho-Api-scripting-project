# Zoho API Scripting Project

This project provides a set of scripts and utilities to interact with the Zoho Desk API. 
It is designed to automate tasks such as account management, SLA application, and data backup.
Please find reference link to the documentation here. [`Zoho Desk API Documentation`](https://desk.zoho.eu/support/APIDocument.do#Introduction) 

## Features

- **Authentication**: Obtain and refresh OAuth tokens for secure API access.
- **Account Management**: Read, update, and manage account data.
- **SLA Management**: Apply and manage SLAs for accounts.
- **Backup Utilities**: Save and restore backups of account data with metadata.
- **Department and View Management**: List departments and views for better API interaction.

## Key Files

- **`config/settings.toml`**: Contains project settings like API URLs.
- **`config/secrets.toml`**: Stores sensitive credentials (ignored in `.gitignore`). Refer to: [`sample_secrets.toml`](config/sample_secrets.toml)
- **`zoho_api/`**: Contains modules for API interaction, including authentication, account management, and backups.
- **`src/`**: Jupyter Notebooks for utilizing Zoho API.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/PK109/Zoho-Api-scripting-project.git
   cd Zoho-Api-scripting-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure secrets:
   - Copy `config/sample_secrets.toml` to `config/secrets.toml`. Valid values can be obtained from Zoho Api Console.
   - Fill in the required fields (`access_token`, `refresh_token`, etc.).

4. Update settings in `config/settings.toml` if necessary.

## Usage

### Authentication

Use the `obtain_token` or `refresh_token` functions from [`zoho_api/auth.py`](zoho_api/auth.py) to manage API tokens.  

```python
from zoho_api import obtain_token, refresh_token

# Obtain a new token
obtain_token()

# or refresh an existing token
refresh_token()
```
Values obtained from server are updated automatically in `secrets.toml`.

### Account Management

Read, update, and backup account data using functions from [`zoho_api/accounts.py`](zoho_api/accounts.py).

```python
from zoho_api import read_account, update_account

# Read account details
account_data, response = read_account(account_id="123456789")

# Update account details
update_data = {"accountName": "Updated Name"}
updated_account, response = update_account(account_id="123456789", payload=update_data)
```

### SLA Management

Apply SLAs to accounts using the `apply_sla` function.

```python
from zoho_api import apply_sla

# Apply an SLA to an account
apply_sla(account_id="123456789", sla_id="987654321")
```

### Backup Utilities

Save and load backups using functions from [`zoho_api/backup.py`](zoho_api/backup.py).  
This makes a opportunity to revert changes in the system, if needed.

```python
from zoho_api import save_backup_to_file, load_backup_from_file

# Save a backup
save_backup_to_file(backup_data, filename="backup.json", updated_fields=["field1", "field2"])

# Load a backup
backup_data = load_backup_from_file(filename="backup.json")
```


## Disclaimer

This project is not affiliated with or endorsed by Zoho Corporation. Use it at your own risk.
