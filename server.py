# Import required modules
import socket
import threading
import secrets
from tkinter import E
import el_gamal
import RSA

# Import new PQC algorithms
from pqc_algorithms import kyber
from pqc_algorithms import dilithium
from pqc_algorithms import falcon
from pqc_algorithms import saber
from pqc_algorithms import newhope
from pqc_algorithms import frodo
from pqc_algorithms import ntru_encrypt
from pqc_algorithms import ntruprime
from pqc_algorithms import classic_mceliece
from pqc_algorithms import bike
from pqc_algorithms import hqc
from pqc_algorithms import rainbow
from pqc_algorithms import sphincsplus
from pqc_algorithms import csidh
from pqc_algorithms import picnic

#HOST = '192.168.1.8'
HOST = '127.0.0.1'
PORT = 1234 # to 65535
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users

    
#Function to choose which security method to use
def chooseMethod():
    lst = [
        "DES",
        "ELGAMAL",
        "RSA",
        "CRYSTALS-Kyber",
        "CRYSTALS-Dilithium",
        "Falcon",
        "SABER",
        "NewHope",
        "FrodoKEM",
        "NTRUEncrypt",
        "NTRUPrime",
        "Classic McEliece",
        "BIKE",
        "HQC",
        "Rainbow",
        "SPHINCS+",
        "CSIDH",
        "Picnic"
    ]
    print("---------Welcome to our secure chat")
    print("1- DES (Data encryption standard)")
    print("2- ElGamal encryption system")
    print("3- RSA (Rivest–Shamir–Adleman)")
    print("4- CRYSTALS-Kyber (Post-Quantum KEM)")
    print("5- CRYSTALS-Dilithium (Post-Quantum Signature)")
    print("6- Falcon (Post-Quantum Signature)")
    print("7- SABER (Post-Quantum KEM)")
    print("8- NewHope (Post-Quantum KEM)")
    print("9- FrodoKEM (Post-Quantum KEM)")
    print("10- NTRUEncrypt (Post-Quantum Encryption)")
    print("11- NTRUPrime (Post-Quantum KEM)")
    print("12- Classic McEliece (Post-Quantum KEM)")
    print("13- BIKE (Post-Quantum KEM)")
    print("14- HQC (Post-Quantum KEM)")
    print("15- Rainbow (Post-Quantum Signature)")
    print("16- SPHINCS+ (Post-Quantum Signature)")
    print("17- CSIDH (Post-Quantum Key Exchange)")
    print("18- Picnic (Post-Quantum Signature)")
    num = input("Choose the encryption system: ")
    print(lst[int(num)-1] + " mode has been started")
    return num

def getMethod():
    return flagmethod
   
# Function to listen for upcoming messages from a client
def listen_for_messages(client, username,key,elgamapublickey,rsa_string):

    while 1:

        message = client.recv(2048).decode('utf-8')
        print("RECV : ",message)
        if message != '':
            ####### send
            final_msg = username + '~' + message + '~' + key + "~" +flagmethod+"~"+elgamapublickey+"~"+rsa_string
            send_messages_to_all(final_msg)
            print("rsaaaaaaa:   ",final_msg)

        else:
            print(f"The message send from client {username} is empty")


# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())
    print("SEND : ", message.encode() )

# Function to send any new message to all the clients that
# are currently connected to this server
    #####here
def send_messages_to_all(message):
    
    for user in active_clients:
        
        # Start the security phase using message then pass the message to client
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client,key):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        print("RECV : ",username)
        if username != '':
            active_clients.append((username, client,key))
            # generate session key
            key = secrets.token_hex(8).upper()

            rsa_string = ""
            elgamalpublickey = ""

            # Handle key generation based on chosen method
            if flagmethod == "1":  # DES
                pass  # DES handled elsewhere

            elif flagmethod == "2":  # ElGamal
                string_ints = [str(x) for x in ElgamalKey]
                elgamalpublickey = ",".join(string_ints)
                print("elgamal public key", elgamalpublickey)

            elif flagmethod == "3":  # RSA
                n, E, D = RSA.calc()
                print("public and private key parameters: ")
                print("n: ", n)
                print("E: ", E)
                print("D: ", D)
                rsa_string += str(n) + "," + str(E) + "," + str(D) + ","

            elif flagmethod == "4":  # CRYSTALS-Kyber
                public_key, secret_key = kyber.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "5":  # CRYSTALS-Dilithium
                public_key, secret_key = dilithium.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "6":  # Falcon
                public_key, secret_key = falcon.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "7":  # SABER
                public_key, secret_key = saber.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "8":  # NewHope
                public_key, secret_key = newhope.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "9":  # FrodoKEM
                public_key, secret_key = frodo.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "10":  # NTRUEncrypt
                public_key, secret_key = ntru_encrypt.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "11":  # NTRUPrime
                public_key, secret_key = ntruprime.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "12":  # Classic McEliece
                public_key, secret_key = classic_mceliece.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "13":  # BIKE
                public_key, secret_key = bike.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "14":  # HQC
                public_key, secret_key = hqc.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "15":  # Rainbow
                public_key, secret_key = rainbow.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "16":  # SPHINCS+
                public_key, secret_key = sphincsplus.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "17":  # CSIDH
                public_key, secret_key = csidh.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            elif flagmethod == "18":  # Picnic
                public_key, secret_key = picnic.generate_keys()
                rsa_string = public_key.hex()
                elgamalpublickey = secret_key.hex()

            else:
                print("Unknown encryption method selected")





            #########send
            prompt_message = "SERVER~" + f"{username} added to the chat~" + key + "~" +flagmethod +"~" + elgamalpublickey +"~"+rsa_string 
            send_messages_to_all(prompt_message)
            
            print("Sessison key successfully generated for " + f"{username } ==>",key)

            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, key,elgamalpublickey,rsa_string, )).start()


# Main function
def main():
    global ElgamalKey
    ElgamalKey = el_gamal.generate_public_key()
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #choose method
    global flagmethod
    flagmethod = chooseMethod()

    # Creating a try catch block
    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    
    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        key = ""
        threading.Thread(target=client_handler, args=(client,key, )).start()


if __name__ == '__main__':
    main()