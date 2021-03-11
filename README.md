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
$ cd Scraper
$ scrapy crawl cardekho
```


<!-- TODOs
	make High Anonymity Proxies middleware
-->