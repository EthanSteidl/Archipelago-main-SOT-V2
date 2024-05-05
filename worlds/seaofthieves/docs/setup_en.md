# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy) by loggin in

## Setup Procedure

1. Configure your Options by navigating to supported games, Sea of Thieves, and clicking options. Then once configured, export your YAML file. Do this for each player in your game
2. Host a world from your YAML files
3. You must now [login](https://www.seaofthieves.com/profile/captaincy/). Once you login, your browser is sent a Microsoft authentication cookie that prevents you from needing to login again.
4. While on the website, open the developer tools and look at the network information. There is an XHR request named "captaincy", if you do not see one, hard refresh your page.
5. View the "Request Headers" section of the "captaincy" HXR GET request. In the header is a field named "Cookie". Copy the value of the cookie you will need it later. This cookie is long.
6. Each player that is connecting to the hosted world must run the client, the Sea of Thieves client can be found in the launcher. 
You will be asked for the server address, ship id, your randomizer player name, and your microsoft cookie.  Provide these details. The mscookie you aquired from the earlier step must be saved to a text file on your computer. You will need to provide the file path for this during the launch of the client.
7. The client should run and connect you to the room at this point. Once connected, you should not see errors related to polling the SOT API. If you do, then you likely did one of the following wrong 
The Ship id you gave does not exist, they are numbered starting from 0 in order left to right on the [website](https://www.seaofthieves.com/profile/captaincy/your-ships). 
The cookie you copied is out of date or you copy/pasted it incorrectly
8. Everything should now function
