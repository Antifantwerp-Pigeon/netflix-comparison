from urllib.request import urlretrieve
from re import compile, MULTILINE, match
from time import sleep
from os import makedirs, system
from os.path import exists, join
from json import loads
from csv import writer

# CONSTANTS
CACHE_DIR = ".cache"
EXPECTED_COUNTRY_COUNT = 249
HEADERS = ["id", "name", "sharing available"]


# REGEX
re_alphanumeric = compile(r"[\d\w]")
re_countries = compile(r"(?<=\"allCountries\": )\[.*?]", MULTILINE)
re_help = compile(r"(?<=<div class=\"c-wrapper\">).*?(?=</div>)", MULTILINE)


def _print(code, text, newline=True):
    end = "\n" if newline else ""
    print("\x1b[" + str(code) + "m", text, "\x1b[0m", end=end)


def log(text, newline=True):
    end = "\n" if newline else ""
    print(text, end=end)

def ok(text, newline=True):
    _print(92, text, newline)

def log_bl(text, newline=True):
    _print(36, text, newline)

def log_cy(text, newline=True):
    _print(94, text, newline)

def warn(text, newline=True):
    _print(93, text, newline)

def err(text, newline=True):
    _print(91, text, newline)


def scrape(url):
    filename = join(CACHE_DIR, "".join(re_alphanumeric.findall(url)))
    if not exists(filename):
        log_cy(f"\tRATE-LIMIT-LIMIT: sleeping for 5...")
        sleep(5)
        log_cy(f"\tRETRIEVING: {url}...")
        urlretrieve(url, filename)
    else:
        log_bl(f"\tCACHED: {url}")

    with open(filename, "r", encoding="UTF-8") as file:
        data = file.read().replace("\n", "")
    
    ok(f"\tLOADED: {url}")
    print()
    
    return data

def scrape_help(url):
    # Not sure if this applies everywhere but it'll do the thing for now
    return re_help.findall(scrape(url))[0]
    

if __name__ == "__main__":
    system("color")  # Enable terminal colors in Windows

    output = []
    makedirs(CACHE_DIR, exist_ok=True)


    netflix_countries = loads(re_countries.search(scrape("https://help.netflix.com/en/node/123277/ci"))[0])
    if (len(netflix_countries) != EXPECTED_COUNTRY_COUNT):
        warn(f"Expected to find {EXPECTED_COUNTRY_COUNT} countries, but found {len(netflix_countries)}")
        input("Press ENTER to continue:")

    for country_data in netflix_countries:
        id = country_data["value"]
        name = country_data["label"]
        
        country = [id, name]

        print()
        log_cy("-" * 30)
        log(f"Country: {name} ({id})")
        
        help_pricing = scrape(f"https://help.netflix.com/en/node/24926/{id}")
        help_acc_sharing = scrape(f"https://help.netflix.com/en/node/123277/{id}")

        if "Pricing (" not in help_pricing:
            err("\tCOUNTRY UNAVAILABLE")
            continue

        if "Share Netflix with someone who doesn’t live with you".lower() in help_acc_sharing.lower():
            log("\tSHARING AVAILABLE:", False)
            ok("TRUE")
            
            country.append(1)
            
        else:
            log("\tSHARING AVAILABLE:", False)
            err("FALSE")
            country.append(0)
        

        output.append(country)

    # https://stackoverflow.com/a/3191811
    with open("output.csv", "w", encoding="UTF-8", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(HEADERS)
        csv_writer.writerows(output)
        





