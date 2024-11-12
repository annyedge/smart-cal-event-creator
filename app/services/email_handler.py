import imaplib
import email

def check_email():
    mail = imaplib.IMAP4_SSL('imap.example.com')
    mail.login('username', 'password')
    mail.select('inbox')
    # Fetch emails and process them
