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
        self.run_server()

    def run_server(self):
        self.connect()
        self.sock.listen(1)
        print('Waiting for client :', self.sock.getblocking())

        try:
            self.client, addr = self.sock.accept()
            print('Connected to:', addr)
            self.client.send(self.initial_message().encode('utf-8'))
            print('Listening to the client...')

            while True:
                client_msg = self.client.recv(256).decode('utf-8')
                print('Client\'s message :', client_msg)

                try:
                    answer = str(self.handle_client_msg(client_msg))
                    if 'stop' in answer:
                        answer += self.final_message()
                        self.client.send(answer.encode('utf-8'))
                        break

                    self.client.send(answer.encode('utf-8'))

                except Exception as exp:
                    print('Exception:', exp)
                    break

        except Exception as exp:
            print('Exception', exp)
            self.client.send('stop'.encode('utf-8'))

        finally:
            try:
                self.client.close()
            except Exception as exp:
                print('Exception', exp)
                print('Connection ended.')

    def connect(self):
        try:
            self.sock.bind((self.Host, self.Port))
        except OSError:
            print("Host is used.")
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
        pattern = re.compile(r"([0-4])\:(\d*)\-\>(\w{0,30})")
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
                return f'Exception: {exp}'
        else:
            print('Wrong string index')
            return 'Wrong string index'

        return self.strings_to_edit

    @staticmethod
    def initial_message():
        return 'You can edit given strings, total string amount is 5'

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
