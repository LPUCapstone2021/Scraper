# Scraper

## Setup
```bash
$ # build docker image
$ docker build --tag scraper .

$ # execute container
$ docker run --interactive --tty \
--name capstone-scraper \
--mount type=bind,source=`pwd`,target=/app \
scraper

$ # create spider(s)
$ scrapy startproject Scraper
$ cd Scraper
$ scrapy genspider -t crawl cardekho cardekho.com
$ scrapy genspider -t crawl zigwheels zigwheels.com
```

## Run crawler
```bash
$ docker start capstone-scraper
$ docker exec -it capstone-scraper bash
$ scrapy crawl cardekho -o data/data.csv
$ scrapy crawl zigwheels -o data/data.csv
```

## Clean data
Open [clean.ipynb](./clean.ipynb) in Google Colab and use `cars.csv` present in `Scraper/spiders/data` as input.

<!-- TODOs
	make High Anonymity Proxies middleware
-->