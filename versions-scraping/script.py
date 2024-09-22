import requests
from bs4 import BeautifulSoup
import re
import csv

def scrape_for_version():
    apps = [
        ["Microsoft todo", "div", "subver", "https://www.techspot.com/downloads/7392-microsoft-to-do.html"],
        ["WhatsApp", "div", "subver", "https://www.techspot.com/downloads/6839-whatsapp-desktop.html"],
        ["Telegram", "a", "Link--primary Link", "https://github.com/telegramdesktop/tdesktop/releases"],
        ["Discord", "div", "subver", "https://www.techspot.com/downloads/6871-discord.html"],
        ["Microsoft Teams", "table", "", "https://learn.microsoft.com/en-us/officeupdates/teams-app-versioning"],
        ["Epic Games", "li", "bg", "https://www.filehorse.com/download-epic-games-launcher/"],
        ["Google Drive", "p", "", "https://support.google.com/a/answer/7577057?hl=en"],
        ["Anaconda", "table", "", "https://docs.anaconda.com/anaconda/pkg-docs/"],
        ["Adobe Premiere Pro", "h1", "TopHeader", "https://www.videohelp.com/software/Adobe-Premiere-Pro/version-history"],
        ["Adobe Photoshop", "h1", "TopHeader", "https://www.videohelp.com/software/Adobe-Photoshop"],
        ["Adobe After Effects", "h1", "TopHeader", "https://www.videohelp.com/software/Adobe-After-Effects"],
        ["ShareX", "span", "colour4a small db fc1 uppercase", "https://sharex.en.lo4d.com/download"],
        ["JIRA", "a", "conf-macro output-inline", "https://confluence.atlassian.com/jirasoftware/jira-software-release-notes-776821069.html"],
        ["Docker Desktop", "h2", "scroll-mt-20", "https://docs.docker.com/desktop/release-notes/"],
        ["Notepad++", "a", "Link--primary Link", "https://github.com/notepad-plus-plus/notepad-plus-plus/releases"],
        ["Atom", "a", "Link--primary Link", "https://github.com/atom/atom/releases"],
        ["Draw.io", "a", "Link--primary Link", "https://github.com/jgraph/drawio-desktop/releases"],
        ["Studio 3T", "a", "Link--primary Link", "https://github.com/Studio3T/robomongo/releases"],
        ["Arduino IDE", "a", "Link--primary Link", "https://github.com/arduino/arduino-ide/releases"],

        # SAP products
        ["SAP NetWeaver", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP ERP", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP S/4HANA", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP CRM", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP SCM", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP Solution Manager", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
        ["SAP SRM", "table", "", "https://support.sap.com/en/my-support/software-downloads/support-package-stacks/product-versions.html?anchorId=section_486851042"],
    ]

    results = {}

    for app in apps:
        app_name = app[0]
        url = app[3]
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # SAP product version extraction
            if "SAP" in app_name:
                table_idx = {
                    "SAP NetWeaver": 0,
                    "SAP ERP": 1,
                    "SAP S/4HANA": 2,
                    "SAP CRM": 3,
                    "SAP SCM": 4,
                    "SAP Solution Manager": 5,
                    "SAP SRM": 6
                }.get(app_name, 0)

                tables = soup.find_all('table')
                if len(tables) > table_idx:
                    table = tables[table_idx]
                    rows = table.find_all('tr')[1:]  # Skip header row
                    if rows:
                        columns = rows[0].find_all('td')
                        if len(columns) == 3:
                            sap_product_version = columns[0].get_text(strip=True)
                            latest_version = sap_product_version
                        else:
                            latest_version = "Not Found"
                    else:
                        latest_version = "Not Found"
                else:
                    latest_version = "Table not found"

            # Non-SAP application handling
            elif app_name == "Microsoft Teams":
                table = soup.find_all("table")[0] if soup.find_all("table") else None
                latest_version = table.find("tbody").find_all("tr")[0].find_all("td")[2].get_text(strip=True) if table else "Table not found"
            elif app_name == "Epic Games":
                li_element = soup.find("li", class_="bg")
                latest_version = li_element.find_all("p")[1].get_text(strip=True).replace("LATEST", "").strip() if li_element else "Not Found"
            elif app_name == "Google Drive":
                for p in soup.find_all("p"):
                    if "Version" in p.text:
                        latest_version = p.text.split("Version ")[1].strip()
                        break
                else:
                    latest_version = "Not Found"
            elif app_name in ["Anaconda", "SAP NetWeaver"]:
                table = soup.find("table", class_="table")
                if table:
                    first_row = table.find("tbody").find_all("tr")[0]
                    latest_version = first_row.find_all("td")[1].get_text(strip=True)
                else:
                    latest_version = "Table not found"
            elif app_name in ["Adobe Premiere Pro", "Adobe Photoshop", "Adobe After Effects"]:
                h1_tag = soup.find("h1", id="TopHeader")
                a_tags = h1_tag.find_all("a") if h1_tag else []
                latest_version = re.search(r"\d+\.\d+", a_tags[2].text.strip()).group() if len(a_tags) >= 3 else "Not Found"
            elif app_name == "ShareX":
                version_span = soup.find("span", class_="colour4a small db fc1 uppercase")
                latest_version = version_span.find_all("span")[1].text.strip() if version_span and len(version_span.find_all("span")) > 1 else "Not Found"
            elif app_name == "JIRA":
                first_match = soup.find('a', class_='conf-macro output-inline', attrs={'data-macro-name': 'sp-nobody-link'}, string=re.compile(r'Jira Software \d+\.\d+\.x release notes'))
                version_numbers = re.findall(r'\d+\.\d+', first_match.get_text()) if first_match else []
                latest_version = version_numbers[0] if version_numbers else "Not Found"
            elif app_name == "Docker Desktop":
                element = soup.find("h2", class_="scroll-mt-20", id="4331")
                latest_version = element.get_text() if element else "Not Found"
            else:
                version_element = soup.find(app[1], class_=app[2])
                latest_version = version_element.text.strip() if version_element else "Not Found"

            # Remove non-numeric characters except for dots
            latest_version = re.sub(r'[^0-9.]', '', latest_version)

            results[app_name] = latest_version
            print(f"The latest {app_name} version is: {latest_version}")

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving the page for {app_name}: {e}")
            results[app_name] = "Error"

    # Save to CSV
    with open('app_versions.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["App Name", "Version", "URL"])
        for app in apps:
            writer.writerow([app[0], results[app[0]], app[3]])

    return results

# Run the scraper
app_versions = scrape_for_version()
