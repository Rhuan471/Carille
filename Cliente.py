import socket

# Como vamos testar no mesmo computador, usamos localhost (127.0.0.1)
IP_SERVIDOR = '127.0.0.1' 
PORTA = 8000

# Cria o socket do cliente
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Tenta conectar ao servidor
    tcp.connect((IP_SERVIDOR, PORTA))
    print("Conectado ao servidor! Digite algo ou digite 'SAIR' para encerrar.")

    while True:
        # Pega a entrada de dados do usuário
        mensagem = input("Você: ")
        
        if not mensagem: # Evita enviar mensagens vazias
            continue

        # Codifica o texto para bytes e envia
        tcp.sendall(mensagem.encode('utf-8'))

        # Fica aguardando a resposta do servidor em tempo real
        resposta_bytes = tcp.recv(1024)
        
        if not resposta_bytes:
            print("O servidor fechou a conexão.")
            break

        # Imprime a resposta processada pelo servidor
        print(f"Servidor respondeu: {resposta_bytes.decode('utf-8')}")

        # Se o comando foi SAIR, quebra o loop no cliente também
        if mensagem.upper() == 'SAIR':
            break

except Exception as e:
    print(f"Não foi possível conectar ou houve um erro: {e}")
finally:
    tcp.close()
