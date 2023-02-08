
# importing os module
import os
 
 
# using getlogin() returning username
pcuser =os.getlogin()
chromeuser = r"--user-data-dir=C:\\Users\\"+pcuser+r"\\AppData\Local\Google\Chrome\User Data"
print(chromeuser)