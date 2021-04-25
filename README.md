# a trie hosted on a server that can host multiple concurrect clients

hi, this is the code for a trie that is hosted on a server, how you add it to a server is up to you but mine is running on an AWS server.

## server

The server hosts the trie as a global value between 2 different types of threads, one is the contoler that makes sure the trie is efficient and dead threads are removed, and the other is the communication threads that link to the clients. The reason they are all threads is so multiple users can connect at once and all access the server at once. The client sends a request to the server with a verification phrase (to make sure only valid clients link). From then on anything that is entered into the command line is sent to the server and a responce is sent back. The only processing done by the client is for displaying the trie. The server can be hosted anywhere with the script in this repository, just change the client IPv4 adress from the one in there to a new one, or you can keep the one in there to access my server running on an aws ec2 virtual machine. 

## client installation

As said above all you really need is the client (and an internet connection and the python libraries sys, os, socket and pygame, but if you have python you will almost certainly have the first 3), just download the client, save it to a location and copy/memorise the directory, then run in command line or termonal with the python command (python for windows or python3 for linux) followed by the file location (something like C:\a_place\maybe_another\client.py) and there you have it, you will automatically be linked to a server and any supported commands you enter (commands will be written below but can also be sen by typing help into the running codes interface). 

commands:
