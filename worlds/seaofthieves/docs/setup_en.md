# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy)

## Setup Procedure

1. Configure your Options by navigating to supported games, Sea of Thieves, and clicking options. Then once configured, export your YAML file. Do this for each player in your game

2. Host a world from your YAML files, duing generation there should be an output file with the extension "apsmSOTCI" for each player. Each player needs to save this file and load their appropriate file when starting the client.

3. You must now [login](https://www.seaofthieves.com/profile/captaincy/). Once you login, your browser is sent a Microsoft authentication cookie that prevents you from needing to login again.

4. While on the website, open the developer tools and look at the network information. There is an XHR request named "captaincy", if you do not see one, hard refresh your page.

5. View the "Request Headers" section of the "captaincy" HXR GET request. In the header is a field named "Cookie". Copy the value of the cookie and save it to a text file on your computer. At this point you should have two files, the options file and the cookie file.

6. Each player that is connecting to the hosted world must run the client, the Sea of Thieves client can be found in the launcher.

7. Once launched, the client will ask for some details. For the clientInput and cookie, provide the absolute filepath to those files on your computer. Your ship id is an integer, not a name. When on the captain website, view your ships and number them from top left to bottom right starting with 0. This is the id of your ship. INSTEAD of entering a ship id, you may enter "NA" to launch in pirate mode

8. The client should run and connect you to the room at this point. There are two things that could fail here, the first is you failed to connect to the room. The second is the authentication to the Sea of Thieves web service failed. 
If you failed to connect to the room, you enter enterd your player incorrectly, did not port forward, or connected to the wrong IP most likely.
If you failed to connect to the Sea of Thieves service, then your cookie may have expired, get another. Make sure you leave the webpage open in browser to prevent expiry early.

9. If there are no errors in the client, then Open Sea of Thieves and you are all set to play. See genearl Sea of Thieves guide for game/client information.
