# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy) by loggin in

## Setup Procedure

This guide covers running the game from source as other forms are not yet supported

Navigate to the website linked above and login to view captaincy details.
Once on the page that displays "Pirate Milestones" and "Ship Milestones", do not click any further. (Going further causes Microsofts web server to cache our data and makes the randomizer update slower in game)

Open the developer tools in browser, navigate to the Network tab, and refresh the page.
You should see an XHR packet with the name "captaincy", select this and vew the request header information. There is a variable named "Cookie" copy this text string.


Once you are here, perform the following steps to generate a game
1. Run WebHost.py
2. Navigate to your browser and visit the localhost
3. Go to Supported Games and click on Options
4. Once your options are selected, click export options
5. Take your YAML file and place it into the Players folder of this code
6. Run Generate.py
7. There should now be an output file containing your world
8. If you are hosting a session, run MultiServer.py with your output files
9. Verify step 8 worked by looking in the terminal and seeing everything looks good
10. Each player must now run the python file "SotCustomClient.py" with the propper command line arguments and all will work.
- "--address ip:port" example: "--address 192.0.0.1:25565"
- "--ship id" example "--ship 1"
- "--mscookie sometext" example "--mscookie asefaw9hfwhafw4"
- "--user name" example "--user PlayerNameForP1"
- Example full command "python SotCustomClient.py --address 192.0.0.1:25565 --ship 1 --user PlayerNameForP1" --mscookie 123123"

Your ship id is found by going to https://www.seaofthieves.com/profile/captaincy/your-ships then number each ship from left to right from 0..X
For example, I have two ships "Falcon" and "Avalon", my ship id of "Avalon" is 1 while "Falcon" is 0
11. Your client should connect and not crash. If it connects, then crashes this is because you gave an invalid ship id for the mscookie you provided, please verify these are correct.
12. What will happen now is your Multiworld will update with things done in SOT. There is a 5ish minute delay due to a technical limitation I am looking into, but just know this is a thing
