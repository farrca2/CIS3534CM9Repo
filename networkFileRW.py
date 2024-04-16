#corey Farrell
#networkFileRW.py
#update routers and switches
#updated for github lab
#4/16/24

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Error importing JSON module.")

##---->>>> Create file constants for the file names; file constants can be reused
EQUIP_R_FILE = 'equip_r.txt'
EQUIP_S_FILE = 'equip_s.txt'
UPDATED_FILE = 'updated.txt'
INVALID_FILE = 'errors.txt'

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount
        
def main():
    ##---->>>> open files here
    try:
        with open(EQUIP_R_FILE) as f:
            routers = json.load(f)
    except FileNotFoundError:
        print(f"Sorry, the file {EQUIP_R_FILE} doesnt exist.")
        return
    
    try:
        with open(EQUIP_S_FILE) as f:
            switches = json.load(f)
    except FileNotFoundError:
        print(f"Sorry, the file {EQUIP_S_FILE} doesnt exist.")
        return

    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)

    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    with open(UPDATED_FILE, 'w') as f:
        json.dump(updated, f)

    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    with open(INVALID_FILE, 'w') as f:
        json.dump(invalidIPAddresses, f)

    print("List of invalid addresses written to file 'errors.txt'")

if __name__ == "__main__":
    main()





