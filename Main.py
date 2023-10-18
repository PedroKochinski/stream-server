import Client
import Message
import Server

#create a menu
def menu():
    print("1. Start stream")
    print("2. Join stream")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice

#main function
def main():
    #create a message object
    message = Message.Message()
    
    #create a server object
    server = Server.Server(2001)
    
    #create a client object
    client = Client.Client(2001)
    
    #create a menu
    choice = menu()
    
    #start stream
    if choice == "1":
        #send a message to the server
        while True:
            server.sendMessage(message, "127.0.0.1", 2001)
        
        #close the client and server
        client.close()
        server.close()
        
    #join stream
    elif choice == "2":
        #send a message to the server
        client.sendMessage(message, '', 1234)
        
        #receive a message from the server
        server.receiveMessage()
        
        #close the client and server
        client.close()
        server.close()
        
    #exit
    elif choice == "3":
        print("Exiting...")
        exit()
        
    #invalid choice
    else:
        print("Invalid choice. Try again.")
        main()

if __name__ == "__main__":
    main()