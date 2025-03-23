import initial
import webinitial
import keylogic

username, password, phonenumber, desired_time_slot = initial.getinfo()
driver = webinitial.start(username,password)
keylogic.make_reservation(driver,desired_time_slot,phonenumber)

