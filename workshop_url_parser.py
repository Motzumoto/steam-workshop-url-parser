import re
import time
from typing import Any, Dict, List, Tuple

NAME: str = "Steam Workshop URL Parser"
GITHUB_URL: str = f"https://github.com/Motzumoto/{NAME.lower().replace(' ', '-')}"


def _with_python_path(package_name: str, /) -> str:
    import sys

    return f"'{sys.executable} -m pip install {package_name}'"


try:
    import requests  # type: ignore
except ImportError:
    print(f"Please install the 'requests' package using the following: {_with_python_path('requests')}")
    exit(1)
try:
    import bs4  # type: ignore
except ImportError:
    print(f"Please install the 'beautifulsoup4' package using the following: {_with_python_path('beautifulsoup4')}")
    exit(1)

del _with_python_path


def extract_modpack_mods(url: str, headers: Dict[str, Any]) -> List[str]:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch mod pack {url} with status code: {response.status_code}")
        return []

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    mod_divs: bs4.ResultSet[bs4.Tag] = soup.select('[id^="sharedfile_"]')

    divs: List[str] = []
    for mod_div in mod_divs:
        aid = mod_div["id"]
        _id = (aid[0] if isinstance(aid, list) else aid).replace("sharedfile_", "")
        divs.append(f"https://steamcommunity.com/sharedfiles/filedetails/?id={_id}")

    return divs


def extract_mod_and_workshop_ids(url: str, headers: Dict[str, Any]) -> Tuple[List[str], List[str], List[str]]:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to fetch {url} with status code: {response.status_code}")
        return [], [], []

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    try:
        description = soup.select_one(".workshopItemDescription").text
    except AttributeError:
        print(f"Failed to find the description for {url}")
        return [], [], []

    mod_ids: List[str] = []
    workshop_ids: List[str] = []
    vehicle_ids: List[str] = []

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

    print(
        f"Collected Workshop IDs: {workshop_ids}",
        f"Collected Mod IDs: {', '.join(mod_ids)}",
        (f"Collected Vehicle IDs: {';'.join(vehicle_ids)}") if vehicle_ids else "",
        sep="\n",
    )
    return workshop_ids, mod_ids, vehicle_ids


def main():
    BASE_URL = "https://steamcommunity.com/"
    WELCOME_MESSAGE: str = f"Welcome to the {NAME}!"

    print(f"{WELCOME_MESSAGE}\n{'-' * len(WELCOME_MESSAGE)}")
    print("Enter the mod URLs one by one. Type 'DONE` when you have finished entering all the URLs.")

    urls = []
    while True:
        msg = f"[{len(urls)}] Enter another Mod/Modpack URL or type 'DONE' to finish: "
        if not urls:
            msg = "Enter a Mod/Modpack URL: "

        url = input(msg).strip()
        if url == "DONE":
            break
        if not url:
            print("URL cannot be empty!")
            continue
        if url in urls:
            print("URL already entered!")
            continue

        if not url.startswith(BASE_URL) or url == BASE_URL:
            print(f"URL must start with {BASE_URL}")
            continue

        urls.append(url)

    if not urls:
        print("\nNo URLs entered. Exiting...")
        exit(1)

    all_mod_ids = []
    all_workshop_ids = []
    all_vehicle_ids = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for url in urls:
        mod_urls = extract_modpack_mods(url, headers) if "/?id=" in url else [url]
        for mod_url in mod_urls:
            workshop_ids, mod_ids, vehicle_ids = extract_mod_and_workshop_ids(mod_url, headers)
            all_workshop_ids.extend(workshop_ids)
            all_mod_ids.extend(mod_ids)
            all_vehicle_ids.extend(vehicle_ids)
            print(f"Processed URL: {mod_url}")
            time.sleep(1)  # 1-second delay between requests

    print(
        "\nParsed Information:\n------------------",
        "Mods: " + ";".join(all_mod_ids),
        "WorkshopItems: " + ";".join(all_workshop_ids),
        ("VehicleIDs: " + ";".join(all_vehicle_ids)) if all_vehicle_ids else "",
        sep="\n",
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nKeyboardInterrupt detected. Exiting...")
    finally:
        BASE_MESSAGE = f"Thank you for using the {NAME}."
        STAR_MESSAGE = f"Please consider giving it a ⭐ Star on GitHub if you found it useful:"
        print(
            "-" * (len(STAR_MESSAGE) + 5),
            f"\n{BASE_MESSAGE}\n{STAR_MESSAGE}\n{GITHUB_URL}\n",
            "-" * (len(STAR_MESSAGE) + 5),
        )
