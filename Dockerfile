FROM python:latest

LABEL version "0.0.1" \
      maintainer "Aniruddha Pandey <anirudh.pandev@gmail.com>"

WORKDIR /app

ENV EMAIL anirudh.pandev@gmail.com
ENV GITHUB_USERNAME pandevim

# Use Bash as default
SHELL ["/bin/bash", "-c"]

# Root privelage
USER root

# Install Scraping Dependencies
RUN pip install scrapy

CMD ["/bin/bash"]
