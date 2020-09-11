import sys
from QueueChecker import QueueChecker
import schedule,time


#def run():

    # Queue = QueueChecker()
    # Queue.goToSite()
    # Queue.chrome_options

    # return schedule.CancelJob



if __name__ == "__main__":
    
    #schedule.every().minutes.at(":40").do( run )
    # schedule.every().monday.at("07:59").do( run )
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1) # Wait every second

    # sys.exit()
    QueueChecker = QueueChecker()
    QueueChecker.chromeOptions()
    QueueChecker.goToSite()
    sys.exit()

