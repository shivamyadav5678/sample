import socket
import threading

HOST = '127.0.0.1'
PORT = 5001
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users

# Function to listen for messages from a client
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                # Forward message to all clients
                print(f"Message from {username}: {message}")
                send_messages_to_all(f"{username}~{message}")
            else:
                print(f"Empty message received from {username}")
                remove_client(username, client)
                break
        except Exception as e:
            print(f"Error receiving message from {username}: {e}")
            remove_client(username, client)
            break

# Function to send a message to a single client
def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to a client: {e}")

# Function to send a new message to all clients
def send_messages_to_all(message):
    for username, client in active_clients:
        send_message_to_client(client, message)

# Function to handle a client connection
def client_handler(client):
    while True:
        try:
            username = client.recv(2048).decode('utf-8').strip()
            if username:
                active_clients.append((username, client))
                print(f"{username} joined the chat")
                send_messages_to_all(f"SERVER~{username} has joined the chat")
                threading.Thread(target=listen_for_messages, args=(client, username)).start()
                break
            else:
                print("Empty username received from a client")
                send_message_to_client(client, "SERVER~Username cannot be empty")
                remove_client(None, client)
                break
        except Exception as e:
            print(f"Error handling client connection: {e}")
            remove_client(None, client)
            break

# Function to remove a client from the active clients list
def remove_client(username, client):
    global active_clients
    if username:
        active_clients = [(u, c) for u, c in active_clients if c != client]
        print(f"{username} disconnected")
        send_messages_to_all(f"SERVER~{username} has left the chat")
    try:
        client.close()
    except:
        pass

# Main function to start the server
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Server running on {HOST}:{PORT}")
    except Exception as e:
        print(f"Error binding to {HOST}:{PORT}: {e}")
        return

    server.listen(LISTENER_LIMIT)
    print(f"Server listening with a limit of {LISTENER_LIMIT} connections")

    while True:
        try:
            client, address = server.accept()
            print(f"New connection: {address[0]}:{address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()
        except Exception as e:
            print(f"Error accepting new client: {e}")
            break

if __name__ == '__main__':
    main()
