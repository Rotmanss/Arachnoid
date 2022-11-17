import socket
import logging


class Client:
    def __init__(self):
        self.Host = '127.0.0.1'
        self.Port = 1026

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run_client()

    def run_client(self):
        try:
            self.client_sock.connect((self.Host, self.Port))
            init_msg = self.client_sock.recv(256).decode('utf-8')
            print(init_msg + '\n')

            while True:
                message = input('type smt:\n')
                self.client_sock.send(message.encode('utf-8'))

                data = self.client_sock.recv(256).decode('utf-8')
                print('Answer:\n', data)
                # if 'get_strings' in message:
                #     string_quantity = int(init_msg[-1])
                #     for j in range(string_quantity):
                #         data = self.client_sock.recv(256).decode('utf-8')
                #         print(data)
                #     print()

                if 'stop' in data:
                    logging.info(f'Connection closed.')
                    self.client_sock.close()
                    break

            print('Connection closed.')
        except Exception as exp:
            print('Exception :', exp)


def main():
    Client()


if __name__ == "__main__":
    main()
