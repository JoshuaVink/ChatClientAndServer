### James Brands and Josh Vink
### CIS 457 03 - Data Communications
# Chat Client And Server - Group Chat

This project is a multi-user group chat application developed in python using TCP sockets. All users are entered into one global space where people can chat. We created a GUI using tkinter for the client side adding features such as emojis and clickable links.

# Our project has 2 Main Components

## 1. Server
 - Listen on a user defined port
 - Accepts incoming clients
 - Sends messages to all clients
 - Sends output when users join and leave (no join yet)
 - Supports multiple clients at once
## 2. Client
 - Asks user for a username
 - Opens a user friendly application using Tkinter
 - displays incoming messages
 - allows to multi-line inputs
 - runs a thread in the background for incoming messages from the server
 - handles exit when disconnecting

# Team Members Responsibilties
## James
 - Ability to Shift+Enter to allow multiple lines of text
 - Output message when a user leaves the chat
 - Emoji shortcuts for users
 - Documentation and ReadMe.d file
## Josh
 - Ouput message when a user joins the chat
 - URL to clickable links
 - Highlights for messages sent by the client (easier to read messages)
## Both
 - Getting starter code working and original tkinter client to open as well as getting server to work
 - If server terminated abruptly clients terminate gracefully
 - Tested on multiple machines

### Git Repository: (make public?)
https://github.com/JoshuaVink/ChatClientAndServer
