

import smtplib
from email.mime.text import MIMEText


def SendEmailToAdmin(Options,Title,Contents):
        
    s = smtplib.SMTP(Options['WorkFlowSettings:emailserver'])
    Recipients=[Options['WorkFlowSettings:ToEmail'],'alistair@intersect.org.au']
    #Recipients=[Options['WorkFlowSettings:ToEmail']]
    #Recipients=[Options['WorkFlowSettings:ToEmail']]
    msg = MIMEText(Contents)
    msg['Subject'] = Title
    msg['From'] = Options['WorkFlowSettings:senderEmail']
    msg['To'] = ','.join(Recipients)#Options['WorkFlowSettings:ToEmail']
    
    #s.sendmail(Options['WorkFlowSettings:senderEmail'],Recipients,msg.as_string())
    
    
    
    s.quit()