import smtplib

s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
s.starttls()
  
# Authentication
s.login("shubhu2603@gmail.com", "Shubhankar123#")
  
# message to be sent
message = "Social Distancing Violation Alert"
  
# sending the mail
s.sendmail("shubhu2603@gmail.com", "hingneshubhankar@gmail.com", message)
  
# terminating the session
s.quit()