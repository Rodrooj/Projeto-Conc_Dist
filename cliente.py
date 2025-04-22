import socket
import sys

# Modo de uso:
#   Inicie o servidor, depois rode as solicitacoes do cliente utilizando o endereco do servidor e os assentos desejados
#   Ex.: python3 cliente.py 127.0.0.1 15 21 31       

if len(sys.argv) < 3:
    print("Uso: python cliente.py <host> <assento1> [<assento2> ...]")
    sys.exit(1)

# O primeiro argumento é o endereço do servidor (ex: localhost)
HOST = sys.argv[1]

# Os demais argumentos são os números dos assentos
assentos = sys.argv[2:]

mensagem = ','.join(assentos) + '\n'

PORT = 8080

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            # Tenta se conectar ao servidor
            sock.connect((HOST, PORT))
        except ConnectionRefusedError:
            print(f"Não foi possível conectar a {HOST}:{PORT}")
            sys.exit(1)

        # Envia a mensagem com os assentos desejados
        sock.sendall(mensagem.encode('utf-8'))

        # Recebe a resposta do servidor
        resposta = sock.recv(1024).decode('utf-8').strip()

        # Mostra a resposta linha por linha
        for linha in resposta.split('\n'):
            print(linha)

if __name__ == '__main__':
    main()
