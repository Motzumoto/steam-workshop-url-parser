# Steam Workshop URL Parser

A Python tool to extract Mod IDs, Workshop IDs, and Vehicle IDs from Steam Workshop URLs.

## Introduction

This tool is designed for server admins and mod enthusiasts who want to easily retrieve Mod IDs, Workshop IDs, and Vehicle IDs from provided Steam Workshop URLs. It streamlines the process of collecting essential identifiers for mod management and server setup.

## Features

- Extract Mod IDs, Workshop IDs, and Vehicle IDs from given URLs.
- Robust parsing mechanism that cleanly handles URL variations.
- User-friendly command-line interface.
- Gracefully manages request errors and provides informative feedback.

## Requirements

- Python 3.6+
- `requests` and `beautifulsoup4` libraries

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Motzumoto/steam-workshop-url-parser.git
   ```

2. Navigate to the project directory:
   ```
   cd steam-workshop-url-parser
   ```

3. Install required libraries:
   ```
   pip install requests beautifulsoup4
   ```

## Usage

1. Run the script:
   ```
   python steam_workshop_parser.py
   ```

2. Follow the on-screen prompts to input your Steam Workshop URLs.

3. Type `DONE` when you're finished, and the script will display the extracted Mod IDs, Workshop IDs, and Vehicle IDs.

## Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/licenses/MIT) file for details.

