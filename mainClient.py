import Client

#create a menu
def menu():
    print("1. Join stream")
    print("2. Exit")
    choice = input("Enter your choice: ")
    return choice

#main function
def main():
    serverIP = "127.0.0.1"
    serverPort = 4501
    #create a client object
    client = Client.Client(serverPort)
    
    #create a menu
    choice = menu()
    
    #join stream
    if choice == "1":
        #send a message to the server
        msgDict = {
        "message": "Request to connect",
        "code": 1,
        "id": 1
        }

        #send a message to the server
        print("sending message...")
        client.sendMessage(msgDict, serverIP, serverPort)
        print("waiting for response...")
        client.receiveMessage()
        
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