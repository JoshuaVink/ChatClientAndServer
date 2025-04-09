### James Brands and Josh Vink
### CIS 457 03 - Data Communications
# Chat Client And Server - Group Chat

This project is a multi-user group chat application developed in python using TCP sockets. All users are entered into one global space where people can chat. We created a GUI using tkinter for the client side adding features such as emojis and clickable links.

# Our project has 2 Main Components

## 1. Server
 - Listen on a user-defined port
 - Accepts incoming clients
 - Sends messages to all clients
 - Sends output when users join and leave
 - Supports multiple clients at once
## 2. Client
 - Asks the user for a username
 - Opens a user-friendly application using Tkinter
 - displays incoming messages
 - allows multi-line inputs
 - runs a thread in the background for incoming messages from the server
 - handles exit when disconnecting

# Team Members Responsibilities
## James
 - Ability to Shift+Enter to allow multiple lines of text
 - Output message when a user leaves the chat
 - Emoji shortcuts for users
 - Documentation and ReadMe.md file
## Josh
 - Added a text box for input and a send button to the GUI
 - Client function to take input via GUI and send it to the server
 - tkinter window to display title as name and port number of client
 - Display messages in the chat box and automatically scroll to the most recent message
 - Display a message when a user joins the chat
 - URL to clickable links
 - Remove the client's name from their messages and instead highlight them in green
## Both
 - Getting starter code working and the original tkinter client to open as well as getting the server to work
 - If the server is terminated abruptly clients terminate gracefully
 - Tested on multiple machines
 - Used our Git repository to add updates and changes to our code

### Git Repository: (make public?)
https://github.com/JoshuaVink/ChatClientAndServer
