Welcome to a complete guide on how to integrate NxWitness VMS with Paxton Door Access Control.
==============================================================================================


Starting from version 3.1 NxWitness __Media Server__ can send __HTTP Requests__ on demand every time a "Soft Trigger" is clicked via NxWitness __Desktop Client__.


Links to the 3rd Party installers:


- https://www.paxton-access.com/


- http://www.networkoptix.com/


- http://www.net2scripting.nl/ ==> Downloads

PART ONE. Paxton API.
---------------------


Once you have Paxton Access Control Server installed and configured, follow the steps below:
--------------------------------------------------------------------------------------------

1. Download __Paxton API__ and install it on your computer.
2. Copy the script __paxton_script.py__ into the folder __Net2Scripting\samples__.
3. Move to a directory with the Utility installed and locate the file __Net2Scripting.exe.config__.
4. Two options have to be modified:


- A file to execute via the Utility has to be replaced by __paxton_script.py__.


- __Confirm_wait__ has to be changed to __false__.

Launch the Utility
------------------

The shortcut to the Net2Scripting should be visible on your Desktop.


The app shall go through the authentication process.


Once done, Paxton Server will be available for incoming requests.


PART TWO. Create a rule within NxWitness Desktop Client.
--------------------------------------------------------


While defining HTTP Requests properties via the Client towards Paxton, next field have to be completed:


1. Action - Do HTTP Request.


2. Interval of Action - 5 sec.


3. HTTP URL: http://localhost:7777.


4. HTTP Content: madagascar.


Comments:


- HTTP content will be compared to a variable's value in the script.


- 7777 port can be modified, please make sure you modify the script accordingly.


- By default the script will block requests every 10 seconds after receiving the first one. By defining a 5 sec interval via Nx, you prevent NxWitness from sending multiple requests
 within a 10 second period as a result of several triggers(Eg.: multiple clicks on soft trigger).
