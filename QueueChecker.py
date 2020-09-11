#This following visits driverpracticaltest.dvsa.gov.uk
#using Selenium to avoid incapsula CDN
import time
import configparser
from Emailer import Emailer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from Config import email,password,server,port,desiredPosition,recheck, queueNotifications
from bs4 import BeautifulSoup

class QueueChecker(object):

    # Instantiate time 
    starttime = time.time()

    URL = 'https://logon.slc.co.uk/cas/login'
    chromePath = 'chromedriver'

    #Instantiate chrome_options 
    chrome_options = Options()

    #Email Instance
    Email = Emailer() 

    prevQueueNumber = None
    isEmailSent = False
    keepSending = True

    emailCount = 0
    lineup = 0 #in position 1
    nearQueue = 0 #near queue


    
    #Chrome options 
    def chromeOptions( self ): 

        # chrome_options.add_argument("--headless")  
        QueueChecker.chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        # QueueChecker.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    
    #Visit the driving practical test website
    def goToSite( self ): 

        service = Service( str( QueueChecker.chromePath ) )
        service.start()
        driver = webdriver.Remote(service.service_url, options=QueueChecker.chrome_options)
        driver.get( QueueChecker.URL )

        time.sleep( 5 ) # Let the user actually see something!

        self.checkQueuePosition( driver ) #Check once in case we get lucky in being close to front of queue 

        driver.close()
        driver.quit()


    # Recursively checks every 5 minutes
    def checkQueuePosition( self, driver ):

        count = 0
        obtainedQueueID = False 
        # Parse the scraped contents into a beutiful soup object
        while True:
            html = driver.page_source
            soup = BeautifulSoup( html, features='html.parser' )
            queueNumber = soup.find("span", attrs={'id': 'MainPart_lbUsersInLineAheadOfYou'}) #Update with Class ID to get Queue Number
            unavaliable = soup.find("div", attrs={'id': 'unavailability-notice'})
            queueLink = soup.find("a", attrs={'id': 'hlLinkToQueueTicket2'})

            #Obtain Queue URL so it becomes sharable accross devices
            if( not obtainedQueueID and queueLink != None):
               
               self.URL = self.URL + "&q=" + queueLink.text 
               obtainedQueueID = True

            # Unavaliable page, continue to refresh
            if( queueLink == None and unavaliable != None ):
               
                count+1
                time.sleep(2)
                driver.refresh()


            # Assume we have been redirected to main page
            # Update URL otherwise we will have to re-wait! 
            elif ( queueNumber == None and unavaliable == None ):
               
                time.sleep(5)
                self.URL = driver.current_url
                time.sleep(2) 
                self.sendEmail ( 'Ready to book' )
                break

            ## Check if Queue Notifs is enabled, send notifications
            elif ( queueNotifications ):
                
                self.keepSending = self.queueNotifs( int ( queueNumber.text ) )

            if ( self.keepSending == False ):
            
                break

    ## Queue update Notifications 
    def queueNotifs( self, queueNumber ):

        # Keep running conditionSendEmail till returns True 
        if ( self.conditionSendEmail( queueNumber ) ):
            
            print("Ending Queue")
            return False #Stop
                

        elif ( queueNumber <= 1000  ):
            
            self.prevQueueNumber = queueNumber # Update previous position of queue
            time.sleep( int( 60 ) - ((time.time() - self.starttime) % int( 60 ) )) #Recheck every minute

        else:
            
            self.prevQueueNumber = queueNumber
            time.sleep( int( recheck ) - ((time.time() - self.starttime) % int( recheck ) )) #Recheck every 5 minutes
            

    #Send emails upon a condition
    def conditionSendEmail( self, queueNumber ):
            
        if ( queueNumber == 1 ):
             
             self.sendEmail ( queueNumber )
             return True #Stop

        elif ( queueNumber > 1 and queueNumber <= 20 and self.nearQueue <= 5 and self.prevQueueNumber != queueNumber ):

            self.sendEmail ( queueNumber )
            self.nearQueue+=1
            return False #Continious


        elif ( queueNumber > 20 and queueNumber <= 500 and self.lineup <= 20 and self.prevQueueNumber != queueNumber ):

            self.sendEmail ( queueNumber )
            self.lineup+=1
            return False #Continious

        elif( queueNumber  <= int ( desiredPosition ) and self.emailCount == 0 and self.prevQueueNumber != queueNumber ):
            
            self.sendEmail( queueNumber )
            self.emailCount+=1

            return False #Continious 

        else:
           
            print ("Didn't meet a criteria") 
            return False #Continious 

    #Send Email
    def sendEmail( self, queueNumber ):

       # print("Sending email")
        print ("Queue: " + str ( queueNumber ) )
        self.Email.updateMessage ( queueNumber, self.URL )
        self.Email.mimeMessage()
        self.Email.send( queueNumber, server, port, email, password )
        print("Sent with URL: " +  str(self.URL ))