# Scraper

# Setup
### Build Image
```bash
$ docker build --tag scraper .
```
### Execute Container
```bash
$ docker run --interactive --tty \
--name capstone-scraper \
--mount type=bind,source=`pwd`,target=/app \
scraper
```
### Create Spider(s)
```bash
$ scrapy startproject Scraper
$ cd Scraper
$ scrapy genspider -t crawl cardekho cardekho.com
```

# Run crawler
```bash
$ docker start capstone-scraper
$ docker exec -it capstone-scraper bash
$ scrapy crawl cardekho -o data/cars.csv
```

# Clean data
Open [clean.ipynb](./clean.ipynb) in Google Colab and use `cars.csv` present in `Scraper/spiders/data` as input.

<!-- TODOs
	make High Anonymity Proxies middleware
-->