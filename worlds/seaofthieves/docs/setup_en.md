# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy)

## Setup Procedure

1. Configure your Options by navigating to supported games, Sea of Thieves, and clicking options on the Archipelago
   website. Then once configured, export your YAML file. Do this for each player in your game

2. Host a world from your YAML files, during generation there should be an output file with the extension "apsmSOTCI"
   for each player. Each player needs to save their file and load their appropriate file when starting the client. It is
   recommended renaming your "apsmSOTCI" file to a short filename like "P2.apsmSOTCI".

3. You must now [login](https://www.seaofthieves.com/profile/captaincy/) to the Sea of Thieves website.

4. While on the website, open the developer tools and look at the network information. There is an XHR request named "
   captaincy", if you do not see one, hard refresh your page (cntrl+F5).

5. View the "Request Headers" section of the "captaincy" HXR GET request. In the header is a field named "Cookie". Copy
   the value of the "Cookie" field and save it to a text file on your computer like "cookie.txt". Make sure you do not
   save extra newlines at the top of the file. At this point you should have two files, the options file and the cookie
   file. Verify you did not copy "Set-Cookie" but instead the "Cookie" field.

6. Each player that is connecting to the hosted world must run the client, the Sea of Thieves client can be found in the
   launcher.

7. Once launched, to run a valid session you must perofrm the following steps: the client will ask for some details. For
   the clientInput and cookie, provide the absolute filepath to those files on your computer. Your ship id is an
   integer, not a name. When on the captain website, view your ships and number them from top left to bottom right
   starting with 0. This is the id of your ship. INSTEAD of entering a ship id, you may enter "NA" to launch in pirate
   mode
    - Run `/setcookie <filepath>` to set your cookie. Use the absolute path to your cookie.txt file. EX: "C:
      /Users/Bob/cookie.txt"
    - Run `/setsotci <filepath>` to set your sotci file. Use the absolute path like above.
    - Run `/setmode <mode>` to set your initial game mode to pirate or ship. If you want to run pirate mode,
      run `/setmode NA`. If you want to run ship mode, run `/setmode #` where # is the integer value of your ship
      starting at 0. You can figure this number out by
      opening [view your captaincy](https://www.seaofthieves.com/profile/captaincy) and viewing your ships. Starting
      left to right, number your ships 0, 1, 2 ... This is the number of your ship.

8. Enter the IP:PORT you are connecting to and click connect. You should not see any errors and connection should
   establish
    - If you failed to connect to the room, some details to check are: did you port forward if hosting locally?, did you
      connect to the right ip:port?
    - If you failed to connect to the Sea of Thieves service, then your cookie may have expired, this is normal. Repeat
      the cookie step. Make sure you leave the webpage open in browser to prevent expiry early.

9. If there are no errors in the client, then Open Sea of Thieves and you are all set to play. See the general Sea of
   Thieves guide for game/client information.
