import time

import requests
from bs4 import BeautifulSoup


def fetch_and_parse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        return extract_mod_and_workshop_ids(url, headers)
    except requests.RequestException as e:
        print(f"Error fetching {url}. Error: {str(e)}")
        return [], []

    except Exception as e:
        print(f"General error for {url}. Error: {str(e)}")
        return [], []


def extract_mod_and_workshop_ids(url, headers):
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch {url} with status code: {response.status_code}")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.select_one(".workshopItemDescription").text

    mod_ids = []
    workshop_ids = []

    lines = description.split("\n")
    for line in lines:
        line = line.strip()
        if "Mod ID:" in line:
            mod_id = line.split(":")[-1].strip()
            mod_ids.append(mod_id)
        elif "Workshop ID:" in line:
            workshop_id = line.split(":")[-1].strip()
            if workshop_id.isdigit():
                workshop_ids.append(workshop_id)

    # In case the Workshop ID isn't in the description
    if not workshop_ids:
        workshop_id_from_url = url.split("?id=")[-1]
        workshop_ids.append(workshop_id_from_url)

    return workshop_ids, mod_ids


def main():
    print("Welcome to the Steam Workshop URL Parser!")
    print(
        "Enter the mod URLs one by one. Type 'DONE' when you have finished entering all the URLs."
    )
    urls = []

    while True:
        url = input("Enter a mod URL: ")
        if url == "DONE":
            break
        urls.append(url)

    all_mod_ids = []
    all_workshop_ids = []

    for url in urls:
        workshop_ids, mod_ids = fetch_and_parse(url)
        all_mod_ids.extend(mod_ids)
        all_workshop_ids.extend(workshop_ids)
        time.sleep(1)  # 1-second delay between requests

    print("\nParsed Information:")
    print("Mods=" + ";".join(all_mod_ids))
    print("WorkshopItems=" + ";".join(all_workshop_ids))


if __name__ == "__main__":
    main()
