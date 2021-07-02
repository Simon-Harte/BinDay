# BinDay
## Small script to notify me when it's bin day. Using Python along with Twilio, Selenium and python-dotenv

So this project was borne of a confusion in my apartment complex as to when the bins go out. Recycling boxes are weekly so that's not an issue, but 
the general waste bins are fortnightly, so some confusion can arise!

It works by scraping the relevant web pages with selenium to grab the date of the next bin collection. It then compares that date with tomorrow's date. If they are a match,
a text notification is sent via Twilio's SMS API.

## Issues

So at the moment, there are several issues which I need to fix:
  1. The recycling URL is hard-coded to my area. I just wanted to get this prototype out fast, so some more scraping automation is needed. Which brings me to:
  2. This project works by scraping the local council's websites. 
      - If the HTML/CSS formatting were to change then the tool may not work as required
      - This approach is fine for one domicile/postcode. To scrape information for a number of addresses/postcodes would require lots of difficult automation

