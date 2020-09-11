#Sends an email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Emailer:

   
    text = """\
    URL"""

    html = """<html><body><a href="URL">URL</a></p></body></html>"""
    message = MIMEMultipart("alternative")


#Construct and Load Config

    # Update Message
    def updateMessage( self, queueNumber, queueURL ):

        print("Email URL:" + str( queueURL ) )
        Emailer.message["Subject"] = self.setMessage( queueNumber )
        Emailer.text = Emailer.text.replace('URL', queueURL )
        Emailer.html =  Emailer.html.replace('URL', queueURL )

    #Set Subject
    def setMessage ( self, queueNumber ):

        queueNumber = str( queueNumber ) # Convert to string to accept "Ready to book" string
        if ( queueNumber <= '5'):
            return  "FINAL DVSA Practical Test Position: " + queueNumber
        else:
           return "DVSA Practical Test Position: " + queueNumber

    def mimeMessage( self ):
       
        plain = MIMEText( Emailer.text, "plain")
        html = MIMEText(Emailer.html, "html")

      
        Emailer.message.attach( plain )   # Add HTML/plain-text parts to MIMEMultipart message
        Emailer.message.attach( html )  # The email client will try to render the last part first


    #Send Email
    def send( self, queueNumber, server, port, email, password ):

        context = ssl.create_default_context() #Create ssl object
    
        Emailer.message["From"] =  email
        Emailer.message["To"] =  email

        with smtplib.SMTP( server , port  ) as server:
            server.starttls( context=context )
            server.ehlo()  # Can be omitted
            server.login( email , password )
            server.ehlo()  # Can be omitted
            server.sendmail( email , email, Emailer.message.as_string() )
