import time
from net2xs import Net2XS
from pylog4net import Log4Net
import socket
import sys
import re

secret_word = 'madagascar' # protects your socket from false openings, triggered by different services.
                           # will be compared to the HTTP Content delivered by Nx Witness 
opening = True

# Operator id 0 is System Engineer
OPERATOR_ID = 0
# Default Net2 password
OPERATOR_PWD = "net2"
# When running on the machine where Net2 is installed
NET2_SERVER = "localhost"

def get_doors(net2):
    """Obtain a list of all known doors
    """
    res = []
    dataset = net2.get_doors()
    if dataset and dataset.Tables.Count > 0:
        for row in dataset.Tables[0].Rows:
            res.append(row.Address)
    return res

# Create logger object
logger = Log4Net.get_logger('open_lock')

with Net2XS(NET2_SERVER) as net2: #create connection with Paxton Server and start the authentication process
    # Authenticate
    net2.authenticate(OPERATOR_ID, OPERATOR_PWD)
    # Get list off door addresses
    doors = get_doors(net2)

    def open_lock():
        global opening    
        # Open lock    
        if not net2.hold_door_open(doors[0]): #you can choose any door from a list created (based on how many ACUs you have in your system).
            logger.Error(
                "Failed to hold lock open: %s." %
                (net2.last_error_message))
        else:
            logger.Info("Set lock open.")

        logger.Info("Now the lock is open...")
        time.sleep(3)

        # Close lock    
        if not net2.close_door(doors[0]):
            logger.Error(
                "Failed to close lock: %s." %
                (net2.last_error_message))
        else:
            logger.Info("Set lock closed.")

        logger.Info("Now the lock is closed again")
        opening = False
        return opening

    def open_socket():
        entry_point = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        try:
            entry_point.bind(('localhost', 7777)) # verify port 7777 is not taken by other services
        except socket.error as msg:
            print(str(msg[0]))
            sys.exit()

        entry_point.listen(5)
        (exit_point, address) = entry_point.accept()

        data = exit_point.recv(1024)
        if len(data) > 0:
            content = data.split(' ')[-1]        
            if content.find(secret_word) > -1:
                open_lock()
                entry_point.close()
            else:
                print "error"        
        else:
            entry_point.close()
    
    while opening == True:
        open_socket()
        time.sleep(10) # close the socket for 10 seconds to avoid multiple openings as a result of a single event. 
        opening = True
        
    entry_point.close()
