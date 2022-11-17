import socket
import logging


class Server:
    def __init__(self):
        self.Host = '127.0.0.1'
        self.Port = 1026

        self.client = None
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

                    if 'get_strings' not in answer:
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
                for j in self.strings_to_edit():
                    self.client.send(j.encode('utf-8'))
                return 'get_strings'
            else:
                return msg
        else:
            return 'Empty request'

    @staticmethod
    def initial_message():
        return 'You can edit given strings, total string amount is 5'

    @staticmethod
    def strings_to_edit():
        return ['Hello World!\n', 'Goodbye Space!\n', 'I like pasta\n', 'Please enter your name\n', 'My name is Roman\n']

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
