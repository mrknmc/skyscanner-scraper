## Scraper for Skyscanner internship 2013 application

#### Dependencies
The dependencies for this scraper can be seen in the text file requirements.txt.
They are the Selenium Python Bindings 2 and a scraping library called Scrapy.

#### Scraping
I decided to scrape the monthly chart view Skyscanner uses for viewing the best prices of plane tickets in a particular month. This allows to scrape the most important data for me (the cheapest tickets) in a larger quantity.
Since the Skyscanner website uses javascript to load the monthly chart view,
to be able to scrape it you first have to start up the selenium browser server.
This is done by running `java -jar selenium-server.jar`.
After that you can run the Skyscanner scrapy spider.
To do this run `scrapy crawl sky`. This takes at least 2 arguments all of
which have to be preceded by `-a`. If you don't supply any arguments flights from Bratislava to Edinburgh this month will be scraped. The arguments are:
- from - the airport code of the airport you want to fly from (required)
- to - the airport code of the airport you want to fly to (required)
- date - the month at which you wish to fly, the format is YYMM (default: this month)
- rtn - int flag, could be 0 or 1, specifies whether you scrape one-way or return journeys (default: 0)
For example to find return flights from Bratislava to Edinburgh in September use:
`$ scrapy crawl sky -a from=BTS -a to=EDI -a date=1309 -a rtn=0`.

#### Going forward
To further improve the scraper an option for looking for flights from an airport to anywhere in the world could be implemented. This would require going to
skyscanner.net/flights-from/AIRPORTCODE and then following the links in the list of countries and later scraping information from the links of airports.
Furthermore, instead of just picking the flights with best prices for each day from the monthly view, we could scrape individial dates for more flights. This could be done by visiting skyscanner.net/flights/FROM/TO/DATE/ and scraping the list of flights.