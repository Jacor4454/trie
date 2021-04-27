(please note I had to manually reset the server at about 9:30 (UK time) on the 27/4/21 because I updated the servers os, if you added words before they will have been removed, sorry for the inconvenience)

# a trie hosted on a server that can host multiple concurrect clients

Hi, this is the code for a trie that is hosted on a server, how you add it to a server is up to you but mine is running on an AWS server.

## server (trie3.py)

The server hosts the trie as a global value between 2 different types of threads, one is the controller that makes sure the trie is efficient and dead threads are removed, and the other is the communication threads that link to the clients. The reason they are all threads is so multiple users can connect at once and all access the server at once. The client sends a request to the server with a verification phrase (to make sure only valid clients link). From then on anything that is entered into the command line is sent to the server and a response is sent back. The only processing done by the client is for displaying the trie. The server can be hosted anywhere with the script in this repository, just change the client IPv4 address from the one in there to a new one, or you can keep the one in there to access my server running on an aws ec2 virtual machine. 

## client(.py) installation

As said above all you really need is the client and the .ttf file (and an internet connection and the python libraries sys, os, socket and pygame, but if you have python you will almost certainly have the first 3), just download the client and Roboto.ttf, save it to a location and copy/memorise the directory, then run in command line or terminal with the python command (python for windows or python3 for linux) followed by the file location (something like C:\a_place\maybe_another\client.py) and there you have it, you will automatically be linked to a server and any supported commands you enter (commands will be written below but can also be seen by typing help into the running codes interface). 

## client commands:
        search  -  the word following it will be searched for in the trie
        add  -  the word following it will be added to the trie
        delete  -  the word following it will be deleted for in the trie (but all data will remain)
        purge  -  the word following it will be searched for in the trie (and all data will be removed if able to do so)
        display  -  copies current trie data to your device and displays it
        predict - the word following it will be used to search the list for any words it can be the first part of (like auto predict)
        quit - stops the connection and terminates program (please use rather than ctrl C, it still works but ctrl C takes time for the server to realise the connection has been lost)

## last words

This was a project that was very out of my comfort zone, the only thing I have had previous experience on starting a week ago was the trie itself, I had to do some much documentation reading for the socket and threading libraries and aws server FAQs), but its now working and my one regret is not having more time to enjoy the learning process, rather than this REALLY steep learning curve I was faced with, but hey ho. 
