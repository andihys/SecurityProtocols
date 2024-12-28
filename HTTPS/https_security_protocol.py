import os
import ssl
import socket
from threading import Thread
from multiprocessing import Process

def start_secure_http_server(host, port, certfile, keyfile):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Secure HTTP Server started at https://{host}:{port}")

    with context.wrap_socket(server_socket, server_side=True) as secure_socket:
        while True:
            client_conn, client_addr = secure_socket.accept()
            print(f"Connection from {client_addr}")
            Thread(target=handle_client, args=(client_conn,)).start()

def handle_client(conn):
    try:
        data = conn.recv(1024).decode('utf-8')
        print(f"Received request:\n{data}")

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nSecure Hello World!"
        conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        conn.close()

class SecureHTTPClient:
    def __init__(self, server_host, server_port, cafile):
        self.server_host = server_host
        self.server_port = server_port
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cafile=cafile)

    def send_request(self):
        with socket.create_connection((self.server_host, self.server_port)) as sock:
            with self.context.wrap_socket(sock, server_hostname=self.server_host) as secure_socket:
                request = (
                    f"GET / HTTP/1.1\r\n"
                    f"Host: {self.server_host}\r\n"
                    "Connection: close\r\n\r\n"
                )
                secure_socket.sendall(request.encode('utf-8'))
                response = secure_socket.recv(4096).decode('utf-8')
                print("Response from server:")
                print(response)


if __name__ == "__main__":

    # Generate self-signed certificate (example only, use a valid certificate in production)
    certfile = "server.crt"
    keyfile = "server.key"
    cafile = "server.crt"

    if not os.path.exists(certfile) or not os.path.exists(keyfile):
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import hashes
        import datetime

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Example Inc"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        cert = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.datetime.utcnow())
            .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
            .sign(private_key, hashes.SHA256())
        )

        # Save key and certificate
        with open(certfile, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        with open(keyfile, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption()
                )
            )

    # Start server in a separate process
    server_process = Process(target=start_secure_http_server, args=("localhost", 8443, certfile, keyfile))
    server_process.start()

    # Start client to connect to the server
    client = SecureHTTPClient(server_host="localhost", server_port=8443, cafile=cafile)
    client.send_request()

    # Terminate server after demonstration
    server_process.terminate()
