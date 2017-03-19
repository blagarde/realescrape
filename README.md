realEscrape
======

My own real estate property listing


Real estate websites generally don't display PPSQM (Price Per SQuare Meter).

This small project scrapes property sizes and prices, and outputs a CSV with the PPSQM field added.
A blacklist can optionally be supplied, to filter out ads with descriptions that contain undesired terms.


# Dependencies
```
# nodejs
$ brew install node
# bower
$ sudo npm install -g bower
```

# Setup
```
git clone https://github.com/blagarde/realescrape && cd realescrape
# Backend
pip install -r requirements.txt
# Frontend
npm install

# create sqlite DB
$ python manage.py syncdb --noinput

```

# Exporting to a sheet
```
# 1. Scrape "leboncoin.fr"
$ scrapy crawl lbc -o lbc.json
(...)
# 2. Filter the output against a custom blacklist
$ python analyze.py -b blacklist.txt lbc.json filtered.csv
Total/selected/censored: 641/323/318
# 3. Open `filtered.csv` in OpenOffice, and sort by PPSQM
```

# UI mode
```
# 1. Run the backend (port 8000)
$ cd realescrape
$ python manage.py runserver

# 2. In another terminal, run the frontend (port 8001)
$ npm start

# 3. Install a plugin to disable X-Frame-Option:
Chrome: https://chrome.google.com/webstore/detail/ignore-x-frame-headers/gleekbfjekiniecknbkamfmkohkpodhe/related
Firefox: https://addons.mozilla.org/en-US/firefox/addon/ignore-x-frame-options/

# 4. Populate the database by scraping a site:
# Single site:
$ scrapy crawl lbc
# All sites:
$ python manage.py scrape

# 5. With the backend and the frontend running, point your browser to:
http://127.0.0.1:8001
```

