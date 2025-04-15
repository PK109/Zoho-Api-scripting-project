import os, datetime, json

def save_response_to_file(response_data, filename=None, updated_fields=None):
    """Zapisuje response do pliku, dodając metadane"""
    if filename == None:
        filename = f"response_{str(datetime.date.today())}.json"
    if not updated_fields:
        print("Brak informacji o zmienionych polach. Backup nie zostanie zapisany.")
        return
    
    data_to_save = {
        "metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "updated_fields": updated_fields
        },
        "backup": response_data  # Kopiujemy czysty backup
    }
    if os.path.exists(filename):
        raise FileExistsError(f"Plik '{filename}' już istnieje! Nie można nadpisać.")
    else:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)
    
        print(f"Response data zapisane do {filename} z metadanymi: {data_to_save['metadata']}")


def save_backup_to_file(backup_data, filename=None, updated_fields=None):
    """Zapisuje backup do pliku, dodając metadane"""
    if filename == None:
        filename = f"backup_{str(datetime.date.today())}.json"
    if not updated_fields:
        print("Brak informacji o zmienionych polach. Backup nie zostanie zapisany.")
        return
    
    data_to_save = {
        "metadata": {
            "timestamp": datetime.datetime.now().isoformat(),
            "updated_fields": updated_fields
        },
        "backup": backup_data  # Kopiujemy czysty backup
    }
    if os.path.exists(filename):
        raise FileExistsError(f"Plik '{filename}' już istnieje! Nie można nadpisać.")
    else:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, indent=4, ensure_ascii=False)

        print(f"Backup zapisany do {filename} z metadanymi: {data_to_save['metadata']}")


def load_backup_from_file(filename):
    """Wczytuje backup_data z pliku JSON"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            backup_data = data.get("backup", {})  # Pobieramy tylko część "backup"
            metadata = data.get("metadata",{})
            print(f"Backup wczytany z {filename}.\nParametry backupu:\n{metadata}")
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje. Tworzę pusty backup.")
        backup_data = {}
    return backup_data
