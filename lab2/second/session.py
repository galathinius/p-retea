import transfer as tr
from encription import encrypt, decrypt, create_keys, get_key_from_string

class Connection:
    def __init__(self, keys):
        self.priv_key = keys
        self.pub_key = keys.publickey()
        self.partner_key = None
        self.handler = None

def start_sever(host, port):
    # create public key
    server = Connection(create_keys())

    server_handler = tr.server_socket(host, port)
    server.handler = server_handler

    # listening for connections
    tr.recv(server_handler) 

    # send public key
    key_string = server.pub_key.exportKey("PEM").decode('utf-8')
    tr.send(server_handler, key_string)

    # receive client pub key
    client_key_string = tr.recv(server_handler).encode('utf-8')
    client_key = get_key_from_string(client_key_string)
    server.partner_key = client_key

    return server

def connect_to(host, port):
    # create client public key
    client = Connection(create_keys())

    proto_handler = tr.socket()
    client.handler = proto_handler

    # connect to server
    tr.connect_to(proto_handler, host, port)

    # receive server public key
    server_key_string = tr.recv(proto_handler).encode('utf-8')
    server_key = get_key_from_string(server_key_string)
    
    client.partner_key = server_key

    # send to server client's public key
    key_string = client.pub_key.exportKey("PEM").decode('utf-8')
    tr.send(proto_handler, key_string)
    return client


def send(mess, conn):
    # encript message with received public key
    encripted = encrypt(mess, conn.partner_key)
    # send message encoded
    tr.send(conn.handler, encripted)
    

def recv(conn):
    # receive mesage encoded
    mess = tr.recv(conn.handler)
    # decode message with private key
    decripted = decrypt(mess, conn.priv_key)
    # return decoded message
    return decripted

def close(conn):
    # close connection
    tr.close(conn.handler)
    pass