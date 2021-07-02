
import time
import os
from twilio.rest import Client
from time import asctime, sleep
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


"""
    This function takes the wheely bin and recycling URLs, 
    the postcode and the address and looks up the relevant websites
    to get the bin collection dates
"""
def getBinDates(wheelyURL, recyclingURL, postCode, myAddress):
    # disable browser notifications
    options = Options()
    options.add_argument("--disable-notifications")

    # this doesn't work in windows but works for Linux
    #options.add_argument('--headless')

    # instantiate the driver for chrome
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#   this is the driver path for a Linux build 
#   driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=options)    

    # go to the council page
    driver.get(wheelyURL)


    # the elements on the wheely bin page
    postCodeSelect = "searchBy_radio_1"
    postCodeTextBox = "Postcode_textbox"

    # get the postcode radio button
    driver.find_element_by_id(postCodeSelect).click()

    # input the postcode into the text box
    textBox = driver.find_element_by_id(postCodeTextBox)
    textBox.send_keys(postCode)

    # address lookup functionality
    addressLookup = "AddressLookup_button"
    driver.find_element_by_id(addressLookup).click()

    #iterate through the addresses in the select element
    addresses = Select(driver.find_element_by_id("lstAddresses"))
    for address in addresses.options:
        if myAddress in address.text:
            address.click()
            break
    
    # grab the date from the appropriate place
    wheelyDate = driver.find_element_by_xpath("//table[@id='ItemsGrid']/tbody/tr[2]/td[4]").text.split()[:3]
    
    # move to the recycling page
    driver.get(recyclingURL)

    # so far this goes straight to the page for my specific address, so updating is needed

    # grab the text from the site
    recyclingDate = driver.find_element_by_xpath("//div[@class='rf-copy']/p[2]/strong").text.split()[:3]

    # chop down the day string to 3 chars
    recyclingDate[0] = recyclingDate[0][:3]

    # chop the 'st', 'nd', 'rd', 'th' off the date
    recyclingDate[1] = recyclingDate[1][:-2]
    # if its only one char long then add a 0 for comparison
    if len(recyclingDate[1]) == 1:
        recyclingDate[1] = "0"+recyclingDate[1]
        
    # chop the month to 3 chars
    recyclingDate[2] = recyclingDate[2][:3]

    #put the finished dates in a dictionary

    dates = {
        'Recycling':recyclingDate,
        'Wheely': wheelyDate
    }
     
    # return the dates
    return dates

"""
    This method sends the actual notification
"""
def sendMessage(key, recipient, source):
    
    # assign the vars
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    
    
    # start the client
    client = Client(account_sid, auth_token)

    ## construct the message
    message ="From BinDay:\n" + key + " bins tomorrow!"

    # creates the noficication and sends it
    message = client.messages \
                    .create(
                        body=message,
                        from_=source,                   
                        to=recipient
                        )


def main():
    
    # load environment vars
    load_dotenv()

    # assign environment vars
    postCode = os.getenv('POST_CODE')
    myAddress = os.getenv('ADDRESS')
    number = os.getenv('PHONE_NUMBER')
    source = os.getenv('SOURCE_NUMBER')
    if not postCode or not myAddress or not number:
        print("Authorisation issue")
        return
    # grab tomorrow's date using datetime object
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d %a %b").split()

    #get the wheelyURL, recyclingURL,for the bin site
    wheelyURL = os.getenv('WHEELY_URL')
    recyclingURL = os.getenv('RECYCLING_URL')

    #get the dates for the bins
    dates = getBinDates(wheelyURL, recyclingURL, postCode, myAddress)

    # iterate through the dates comparing tomorrow's date with the bin day
    for key in dates.keys():
        # if they match send the notification
        if set(tomorrow) == set(dates[key]):
            sendMessage(key, number, source)


if __name__ == "__main__":
    main()
    

