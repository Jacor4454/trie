# a trie hosted on a server that can host multiple concurrect clients

hi, this is the code for a trie that is hosted on a server, how you add it to a server is up to you but mine is running on an AWS server.

## server

The server hosts the trie as a global value between 2 different types of threads, one is the contoler that makes sure the trie is efficient and dead threads are removed, and the other is the communication threads that link to the clients. The reason they are all threads is so multiple users can connect at once and all access the server at once. The client sends a request to the server with a verification phrase (to make sure only valid clients link). From then on anything that is entered into the command line is sent to the server and a responce is sent back. The only processing done by the client is for displaying the trie. 
