import socket
import logging


class Client:
    def __init__(self):
        self.Host = '127.0.0.1'
        self.Port = 1026

        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.getLogger("Client")
        logging.basicConfig(filename="client_log.log",
                            level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

        self.run_client()

    def run_client(self):
        logging.info("Client socket created")
        try:
            self.client_sock.connect((self.Host, self.Port))
            logging.info(f'Connected to a server {self.Host}')
            init_msg = self.client_sock.recv(441).decode('utf-8')
            print(init_msg)

            while True:
                message = input('\ntype smt:\n')
                self.client_sock.send(message.encode('utf-8'))
                logging.info(f'Sent request: {message}')

                data = self.client_sock.recv(256).decode('utf-8')
                logging.info(f'Received answer: {data}')

                if 'get_strings' in message or '=' in message and 'Exception' not in data:
                    strings_list = [x for x in data.strip('[]').split(', ')]
                    print('Answer:')
                    for i, value in enumerate(strings_list):
                        value = value.replace('\'', '')
                        print(f'{i})', value.strip())
                else:
                    print('Answer:\n', data)

                if 'stop' in data:
                    logging.info(f'Connection closed.')
                    self.client_sock.close()
                    break

            print('Connection closed.')
        except Exception as exp:
            print('Exception :', exp)
            logging.exception(f"Exception: {exp}. The server may be down.")


def main():
    Client()


if __name__ == "__main__":
    main()
