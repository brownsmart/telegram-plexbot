# telegram-plexbot
Pull data from your Plex Media Server's API to send as messages using Telegrams Bot API

==========
Shout Outs
==========
1. YuKuKu [https://github.com/yukuku/telebot] for without this I would of never got this far!
2. Dane22 [https://forums.plex.tv/profile/dane22] for showing me where to find the PLEX API Overview details

===========================
Requirements & Instructions
===========================

1. Python 2.7
2. Google Cloud Engine Account
3. Plex Media Server & Plex Account (Plex Pass not required)
4. Plex Media Server Address (URL e.g. http://PMS:32000/library/section/1)
5. Visit https://github.com/Arcanemagus/plex-api/wiki/Plex-Web-API-Overview or
6. Visit https://code.google.com/p/plex-api/wiki/PlexWebAPIOverview or commands
7. Get your Plex Token visit https://support.plex.tv/hc/en-us/articles/204059436
8. Visit https://github.com/yukuku/telebot and setup your Telegram Bot, Google Cloud Engine and Webhooks (You can run this via another server using Python but not sure if there is a SSL requirement if using your own server and Python and Telegram API)
9. Update TOKEN = '' with your TELEGRAM TOKEN in the "main.py" file.
10. Scroll down through the "main.py" file and look for "I CUSTOMISED HERE" (Line: 114)
11. Edit the lines 117 through to 153 to accomdate how your PMS API XML data is displayed, e.g. your sections http://PMS_ADDRESS:32400/library/sections will show you which numbers are which so you know what to put in the URL
12. After that its about which API commands you need for your bot.

===================
Things i want to do 
===================

1. Change the way I use the "if '/tv' in text" option in instead of just using if '/tv': as command, because if the user was to put /tv in a conversation while the bot is in a group chat then the command would be triggered.

2. Add notifications where a user enters something like "/tv alert power s02 episode 08" the bot will send a private message to the telegram user letting them know the show has been added. Same for movies and other forms of content.

3. "/whoswatching" this will query using http://PMS:32000/status/sessions command and parse the XML from "root.findall('./Video/User')" and "root.findall('./Video')" from the User <User title=""> Attributes and from Video the <title=""> attributes. Problem I have is I think i need to write a simultaneous loop in python to pluck out of one child node in the XML and then go back in deeper to get another child node then push out both attributes using the reply(var1 +' - ' + var2) but just cant get it to root.findall, then root.findall again "YET"!!

4. Eventually I want this re-done in NodeJs, as much as I am loving python, I want to do this in Javascript, so I am going to fork https://github.com/pintux/whataboutBot as a start!, but going to use this python as my quick and simple playground first.
