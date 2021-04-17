# Scraper

# Setup
```bash
$ docker build --tag scraper .
```
```bash
$ docker run --interactive --tty \
--name capstone-scraper \
--mount type=bind,source=`pwd`,target=/app \
scraper
```
```bash
$ scrapy startproject Scraper
$ cd Scraper
$ scrapy genspider -t crawl cardekho cardekho.com
```

# Run crawler
```bash
$ docker start capstone-scraper
```
```bash
$ docker exec -it capstone-scraper bash
```
```bash
$ scrapy crawl cardekho -o data/cars.csv
```

# Clean data
Open [clean.ipynb](./clean.ipynb) in Google Colab and use `cars.csv` present in `Scraper/spiders/data` as input.

<!-- TODOs
	make High Anonymity Proxies middleware
-->