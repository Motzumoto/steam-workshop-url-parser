import re
import time

import requests
from bs4 import BeautifulSoup


def extract_modpack_mods(url, headers):
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(
            f"Failed to fetch mod pack {url} with status code: {response.status_code}"
        )
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    mod_divs = soup.select('[id^="sharedfile_"]')
    return [
        "https://steamcommunity.com/sharedfiles/filedetails/?id="
        + mod_div["id"].replace("sharedfile_", "")
        for mod_div in mod_divs
    ]


def extract_mod_and_workshop_ids(url, headers):
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch {url} with status code: {response.status_code}")
        return [], [], []

    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.select_one(".workshopItemDescription").text

    mod_ids = []
    workshop_ids = []
    vehicle_ids = []

    # Adjusted regex for capturing Mod IDs
    mod_id_matches = re.findall(
        r"(Mod ?ID|MID): *([^\r\n\t\f\v \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff<>]+)",
        description,
        re.IGNORECASE,
    )
    for _, mod_id in mod_id_matches:
        mod_ids.append(mod_id.strip())

    # Extracting Vehicle IDs from the mod's description
    vehicle_id_matches = re.findall(r"Vehicle IDs: ([a-zA-Z0-9_, ]+)", description)
    if vehicle_id_matches:
        vehicle_list = vehicle_id_matches[0].split(",")
        for v_id in vehicle_list:
            cleaned_id = v_id.replace("Workshop ID", "").strip()
            if cleaned_id:
                vehicle_ids.append(cleaned_id)

    # Extracting Workshop IDs from the mod's description
    lines = description.split("\n")
    for line in lines:
        line = line.strip()
        if "Workshop ID:" in line:
            workshop_id = line.split(":")[-1].strip()
            if workshop_id.isdigit():
                workshop_ids.append(workshop_id)

    # In case the Workshop ID isn't in the description
    if not workshop_ids:
        workshop_id_from_url = url.split("?id=")[-1].split("&")[0]
        workshop_ids.append(workshop_id_from_url)

    print(f"Collected Workshop IDs: {workshop_ids}")
    print(f"Collected Mod IDs: {', '.join(mod_ids)}")
    if vehicle_ids:
        # Joining vehicle IDs with semicolons
        print(f"Collected Vehicle IDs: {';'.join(vehicle_ids)}")

    return workshop_ids, mod_ids, vehicle_ids


def main():
    print("Welcome to the Steam Workshop URL Parser!")
    print(
        "Enter the mod URLs one by one. Type 'DONE' when you have finished entering all the URLs."
    )
    urls = []

    while True:
        url = input("Enter a mod URL or a modpack URL: ")
        if url == "DONE":
            break
        urls.append(url)

    all_mod_ids = []
    all_workshop_ids = []
    all_vehicle_ids = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for url in urls:
        mod_urls = extract_modpack_mods(url, headers) if "/?id=" in url else [url]
        for mod_url in mod_urls:
            workshop_ids, mod_ids, vehicle_ids = extract_mod_and_workshop_ids(
                mod_url, headers
            )
            all_workshop_ids.extend(workshop_ids)
            all_mod_ids.extend(mod_ids)
            all_vehicle_ids.extend(vehicle_ids)
            print(f"Processed URL: {mod_url}")
            time.sleep(1)  # 1-second delay between requests

    print("\nParsed Information:")
    print("Mods=" + ";".join(all_mod_ids))
    print("WorkshopItems=" + ";".join(all_workshop_ids))
    if all_vehicle_ids:
        print("VehicleIDs=" + ";".join(all_vehicle_ids))


if __name__ == "__main__":
    main()
