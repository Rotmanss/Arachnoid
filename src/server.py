import socket
import logging
import re


class Server:
    def __init__(self):
        self.Host = '127.0.0.1'
        self.Port = 1026

        self.client = None
        self.strings_to_edit = \
            ['Hello World!', 'Goodbye Space!', 'I like pasta', 'Please enter your name', 'My name is Anton']

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.getLogger("Server")
        logging.basicConfig(filename="server_log.log", level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

        self.run_server()

    def run_server(self):
        logging.info("Server was run")
        self.connect()
        self.sock.listen(1)
        print('Waiting for client :', self.sock.getblocking())

        try:
            self.client, addr = self.sock.accept()
            print('Connected to a client:', addr)
            logging.info(f'Connected to a client {addr}')
            self.client.send(self.initial_message().encode('utf-8'))
            logging.info("Sent info")
            print('Listening to the client...')
            logging.info('Listening to the client')

            while True:
                client_msg = self.client.recv(256).decode('utf-8')
                print('Client\'s message :', client_msg)
                logging.info(f'Client\'s message: {client_msg}')

                try:
                    answer = str(self.handle_client_msg(client_msg))
                    if 'stop' in answer:
                        answer += self.final_message()
                        self.client.send(answer.encode('utf-8'))
                        logging.info(f'Send answer: {answer}')

                        logging.info("Stop marker founded.")
                        logging.info("Connection closed.")
                        logging.info("\n" + "-" * 30 + "\n")
                        break

                    self.client.send(answer.encode('utf-8'))
                    logging.info(f'Sent answer: {answer}')

                except Exception as exp:
                    print('Exception:', exp)
                    logging.warning(f'Exception: {exp}')
                    break

        except Exception as exp:
            print('Exception', exp)
            logging.info("Error. Connection closed.")
            self.client.send('stop'.encode('utf-8'))

        finally:
            try:
                self.client.close()
            except Exception as exp:
                print('Exception', exp)
                logging.warning(f'Exception: {exp}')
                print('Connection ended.')
                logging.info("Server stopped!\n" + "-" * 30 + "\n")

    def connect(self):
        try:
            self.sock.bind((self.Host, self.Port))
        except OSError:
            print("Host is used.")
            logging.warning('Host is used.')
            exit()

    def handle_client_msg(self, msg):
        if len(msg) > 0:
            if msg.lower() == 'stop':
                return 'stop\n'
            elif msg.lower() == 'who':
                return self.who()
            elif msg.lower() == 'get_strings':
                return self.strings_to_edit
            elif msg[0] == '=':
                return self.parse_request(msg[1:])
            else:
                return 'This command is not supported!'
        else:
            return 'Empty request'

    def parse_request(self, msg):
        pattern = re.compile(r"([0-4])\s*\:\s*(\d*)\s*\-\>\s*(\w{0,30})")
        it = re.match(pattern, msg)
        if it:
            pure_msg = it.group(0, 1, 2, 3)

            str_index = int(pure_msg[1])
            char_pos = int(pure_msg[2])
            char = pure_msg[3]

            try:
                current = list(self.strings_to_edit[str_index])
                current[char_pos] = char
                self.strings_to_edit[str_index] = "".join(current)
            except Exception as exp:
                print('Exception:', exp)
                logging.warning(f'Exception: {exp}')
                return f'Exception: {exp}'
        else:
            print('Exception : Wrong string index or incorrect expression')
            logging.warning(f'Exception : Wrong string index or incorrect expression')
            return 'Exception : Wrong string index or incorrect expression'

        return self.strings_to_edit

    @staticmethod
    def initial_message():
        return "Write a command from the list below, this will be sent to the server.\n" \
               "Command list:\n\t" \
               "1)'who' : returns information about author.\n\t" \
               "2)'get_strings' : returns strings for editing, to edit string use command '3)'\n\t" \
               "3)'=string index : char index in selected string -> your char(s)' : it changes selected string\n\t" \
               "P.S: You can add <= 30 chars, everything above 30 will be ignored!\n\t" \
               "Example: =0:9->G\n\t" \
               "4)'stop' : stops the session"

    @staticmethod
    def final_message():
        return 'You have just ended this program!'

    @staticmethod
    def who():
        return 'Pevny Roman, K25, V1, \'String editor\''


def main():
    Server()


if __name__ == "__main__":
    main()
