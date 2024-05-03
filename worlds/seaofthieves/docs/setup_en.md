# Sea of Thieves MultiWorld Setup Guide

## Required Software

- Sea of Thieves must be installed (agnostic of launcher)
- You must have Captain status in Sea of Thieves or be playing in the same world as someone who does
- Must be able to login to [view your captaincy](https://www.seaofthieves.com/profile/captaincy) by loggin in

## Setup Procedure

Navigate to the website linked above and login to view captaincy details.
Once on the page that displays "Pirate Milestones" and "Ship Milestones", do not click any further. (Going further causes Microsofts web server to cache our data and makes the randomizer update slower in game)

Open the developer tools in browser, navigate to the Network tab, and refresh the page.
You should see an XHR packet with the name "captaincy", select this and vew the request header information. There is a variable named "Cookie" copy this text string.

Start the Sea of Thieves client giving your cookie as a command line argument

