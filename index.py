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
HEADERS = ["id", "name", "plan", "currency", "lowest price", "lowest plan", "highest price", "highest plan", "sharing available"]


# REGEX
re_alphanumeric = compile(r"[\d\w]")
re_countries = compile(r"(?<=\"allCountries\": )\[.*?]", MULTILINE)
re_help = compile(r"(?<=<div class=\"c-wrapper\">).*?(?=</div>)", MULTILINE)
re_pricing = compile(r"<strong>(?P<plan>\w*?)</strong>?: (?P<currencyone>(\W|[A-Za-zč])*?|)(?P<price>(\d|\.|,)*) ?(?P<currencytwo>(\W|[A-Za-zč])*?|) ?/ ?(?P<term>\w*)", MULTILINE)


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
    
    ok(f"\tLOADED: {filename} ({url})")
    print()
    
    return data

def scrape_help(url):
    # Not sure if this applies everywhere but it'll do the thing for now
    return re_help.findall(scrape(url))[0]


# https://stackoverflow.com/a/3191811
def write_csv(data: list, headers=HEADERS, filename="output.csv"):
    with open(filename, "w", encoding="UTF-8", newline="") as file:
        csv_writer = writer(file)
        csv_writer.writerow(headers)
        csv_writer.writerows(data)

if __name__ == "__main__":
    system("color")  # Enable terminal colors in Windows

    output = []
    unavailable = []
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
            unavailable.append(country)
            continue

        if "Share Netflix with someone who doesn’t live with you".lower() in help_acc_sharing.lower():
            log("\tSHARING AVAILABLE:", False)
            ok("TRUE")
            country.append(1)            
        else:
            log("\tSHARING AVAILABLE:", False)
            err("FALSE")
            country.append(0)
        
        # Pricing
        currency = None
        lowest_price = 99999999999
        lowest_plan = "None"
        highest_price = 0
        highest_plan = "None"
        pos = 0
        while True:
            query = re_pricing.search(help_pricing, pos)
            try:
                data = query.groupdict()
            except AttributeError:
                break
            # Currency
            plan_currency = data["currencyone" if "currencytwo" in data else "currency2"].strip()
            
            # Check input
            if len(plan_currency) > 3:
                err(f"\tCurrency '{plan_currency}' has a suspicious length {len(plan_currency)}. Please double-check and change the length/regex as applicable")

            # Save currency if not yet saved. Alternatively, double check it's the same
            if currency == None:
                currency = plan_currency
                log("\tCurrency: ", False)
                log_cy(currency)
            elif plan_currency != currency:
                err("\tDifferent plans in the same country have different currencies. Assuming error, exiting.")
                exit()
            
            # Price
            price = float(data["price"].replace(",", ""))  # TODO CHANGE
            if price == lowest_price or price == highest_price:
                err("\tTwo identical pricing plans have been found. Assuming error, exiting")
                exit()
            plan_label = f"/{data['term']} ({data['plan']})"
            if price < lowest_price:
                lowest_price = price
                lowest_plan = plan_label
            if price > highest_price:
                highest_price = price
                highest_plan = plan_label


            pos = query.end()
                
        
        log(f"\tLowest price:", False)
        log_bl(f"{lowest_price}{lowest_plan}")
        log(f"\tHighest price:", False)
        log_bl(f"{highest_price}{highest_plan}")

        country.append(currency)
        country.append(lowest_price)
        country.append(lowest_plan)
        country.append(highest_price)
        country.append(highest_plan)

        output.append(country)

    write_csv(output)
    write_csv(unavailable, ["id", "name"], "unavailable.csv")       




