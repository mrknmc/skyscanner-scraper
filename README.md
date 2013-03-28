# Scraper for Skyscanner internship application

## Dependencies
The dependencies for this scraper can be seen in the text file requirements.txt.
They are the Selenium Python Bindings 2 and a scraping library called Scrapy.

## Scraping
Before scraping you have to start up the selenium server. This is done by
running `java -jar selenium-server.jar`. After that you run the scrapy crawler.
To do this execute `scrapy crawl sky`. This takes at least 2 arguments all of
them have to be preceded by `-a`. The arguments are:
- from - the airport code of the airport you want to fly from
- to - the airport code of the airport you want to fly to
- date - the month at which you wish to fly, the format is YYMM
- rtn - int flag that could be 0 or 1, it specifies whether you are looking for one way or return journeys.
For example to find return flights from Bratislava to Edinburgh in september use:
`$ scrapy crawl sky -a from=BTS -a to=EDI -a date=1309 -a rtn=0`.