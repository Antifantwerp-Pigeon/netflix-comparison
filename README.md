# Netflix-Comparison

A companion piece to the [Netflix & Poverty spreadsheet](https://docs.google.com/spreadsheets/d/12CSo6NqJ29Yi7cTZSZ0tQm7nqzLYfc_Kotf_n30et0w/edit?usp=sharing). This project is set up to grow naturally alongside the developments of Netflix's plans to [possibly test a free version supported by ads](https://www.bloomberg.com/news/newsletters/2024-06-23/netflix-s-advertising-challenge-it-isn-t-big-enough), and is as such intended to juxtapose that to the when and where Netflix's password sharing crackdown began.


## How-to
### Usage
This script has no dependencies aside from having Python 3 installed.
```bash
git clone https://github.com/Antifantwerp-Pigeon/netflix-comparison.git
cd netflix-comparison
python index.py
```
This will download a bunch of html files, which will be cached for future runs.

## Explanation
### What does the script do?
- Download & cache Netflix help pages
- Do rudimentary scraping to collect all required info
- Output that data in output.csv. This file is meant to be imported into the [Netflix & Poverty spreadsheet](https://docs.google.com/spreadsheets/d/12CSo6NqJ29Yi7cTZSZ0tQm7nqzLYfc_Kotf_n30et0w/edit?usp=sharing)

### Why average wage?
The [worlddata.info average income page](https://www.worlddata.info/average-income.php) ironically describes why I don'. Income keeps external gains in mind, e.g. for companies.

> A peron's income [...] includes all wages and salaries, but also other income, e.g. from capital gains. At first glance, that may sound somewhat inaccurate in a country comparison, as companies also generate an income. Regardless of size, the company is also owned by individuals. Therefore, the income of the owners increases to the same extent as the income of their companies.

I don't care how well big company owners are doing. They're big company owners. This is about the average person, and they do not own considerable amounts of external income.

### Why host the sheet on Google Drive?
Map charts and free public hosting. That's pretty much it.

#### Why is there no Central America zoom-in in the spreadsheet
Google Sheets doesn't have an option for it. If I end up finding a map chart with the option that is hostable online with Central America, I'll move to there.

### Why do this?
Structural problems affect us all, and businesses can still make dubious to unethical decisions even when they follow the law.
