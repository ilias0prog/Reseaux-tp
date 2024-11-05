import socket
from urllib.parse import urlparse


# Echo client program

HOST = 'enseignement.be'
PORT = 80

# Construire une requête HTTP GET
request = "GET /index.php HTTP/1.1\r\n"
request += f"Host: {HOST}\r\n"
request += "User-Agent: PythonClient/1.0\r\n"
request += "Accept: text/html\r\n"
request += "Connection: close\r\n\r\n"  # Ligne vide pour terminer l'en-tête

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(request.encode())  # Envoyer la requête HTTP encodée en bytes    
    data = s.recv(1024)
print('Received', repr(data))


url = "http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html"


def get_http(url: str):
    parsed_url = urlparse(url)
    
    path = parsed_url.path if parsed_url.path else '/'
    HOST = parsed_url.hostname
    PORT = 80
    
    # Créer un socket et établir la connexion
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))  # Connexion au serveur
        request = f"GET {path} HTTP/1.1\r\n" \
                  f"Host: {HOST}\r\n" \
                  f"User-Agent: Python/3.9\r\n" \
                  f"Connection: close\r\n\r\n"
                  
        s.sendall(request.encode())

        response = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            response += chunk
            
    # Séparer les headers et le body
    headers, body = response.split(b"\r\n\r\n", 1)
    
    dico = {}
    dico["headers"] = headers.decode()
    
    # Extraire la ligne de statut
    status_line = headers.split(b"\r\n")[0]  # Correctement obtenir la ligne de statut
    dico["status_line"] = status_line.decode()

    # Extraire le code de statut
    status_code = status_line.split(b" ")[1]  # Correctement obtenir le code de statut
    dico["status_code"] = status_code.decode()
    dico["body"] = body.decode()
    
    return dico

# Appel de la fonction pour récupérer les informations
d = get_http(url)

# Afficher les résultats
print("Status line:", d["status_line"])
print("Status code:", d["status_code"])
print("Headers:\n", d["headers"])
print("Body:\n", d["body"])
