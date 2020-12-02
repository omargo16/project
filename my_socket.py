import socket
from threading import Thread
import subprocess as sub
import logging

_logger = logging.getLogger(__name__)


class MySocket:
    def __init__(self, user):
        self._name = user._name
        self.__user = user
        self.__host = "127.0.0.1"
        self.__port = 408


    def _set_port(self):
        _logger.info("Usuario %s: Buscando puerto disponible para conexión." % self._name)
        for port in range(40800,40900):
            is_bussy = sub.getoutput("netstat -an | grep %s" % port)
            if not is_bussy:
                _logger.info("Usuario %s: Puerto %s encontrado." % (self._name, port))
                return port

    def _set_connection(self):
        _logger.info("Usuario %s: Estableciendo la conexión socket." % self._name)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
                self.__port = self._set_port()
                skt.bind((self.__host, self.__port))
                skt.listen()
                _logger.info("Usuario %s: Sesión establecida, esperando comunicación." % self._name)
                print("Conexión establecida, esperando comunicación.")
                conn, addr = skt.accept()
                chat = Thread(target=self._start_chat, args=(conn, addr))
                chat.start()
        except Exception as error:
            _logger.error("Usuario %s: Error al tratar de conectar socket\nTraceback:\n %s." % (self._name, error))
            print("Ha ocurrido un error. Vuelva a intentarlo.\nTraceback:\n%s" % error)

    def set_connection(self):
        self._set_connection()

    def _get_host(self):
        return self.__host

    def get_host(self):
        return self._get_host()

    def _get_port(self):
        return self.__port

    def get_port(self):
        return self._get_port()

    def _get_connection(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
            try:
                skt.connect((self.__host, int(port)))
            except ConnectionError as error:
                _logger.error("Usuario %s: Error al tratar de conectar con puerto %s.\nTraceback:\n %s." % (port, error))
            else:
                _logger.info("Usuario %s: Conectado con puerto %s." % (self._name, port))
                self_credentials = ("%s:%s" % (self.__user._name, self.__user.get_public_key()))
                skt.send(self_credentials.encode())
                _logger.info("Usuario %s: Ha realizado enviado credenciales a %s." % (self._name, port))
                credentials = skt.recv(1024)
                _logger.info("Usuario %s: Ha realizado recibido credenciales de %s." % (self._name, port))
                self.__user.add_key(credentials)
                friend = credentials.decode().split(":")[0]
                _logger.info("Usuario %s: Ha realizado intercambio de llaves con %s." % (self._name, friend))
                print("Tiene una comunicacion con: %s. Si desea abandonar la conversacion esciba EXIT." % friend)
                while True:
                    message = input("%s: " % self._name)
                    if message != 'EXIT':
                            _logger.info("Usuario %s: Ha escrito un mensaje." % (self._name))
                            skt.sendall(self.__user.cipher_message("%s:%s" % (friend, message)))
                            _logger.info("Usuario %s: Ha enviado un mensaje a %s." % (self._name, friend))
                            data = skt.recv(1024)
                            if data == b'EXIT':
                                print("%s: Ha finalizado la conversación." % friend)
                                break
                            else:
                                print("%s: %s" % (friend, self.__user.decipher_message(data)))
                    else:
                        _logger.info("Usuario %s: Ha dejado la conversación." % self._name)
                        print("Has finalizado la conversación.")
                        skt.sendall(message.encode())
                        break
    
    def get_connection(self, port):
        self._get_connection(port)
    
    def _start_chat(self, connection, address):
        with connection:
            credentials = connection.recv(1024)
            _logger.info("Usuario %s: Ha realizado recibido credenciales de %s." % (self._name, address[1]))
            self.__user.add_key(credentials)
            self_credentials = ("%s:%s" % (self.__user._name, self.__user.get_public_key()))
            connection.send(self_credentials.encode())
            _logger.info("Usuario %s: Ha realizado enviado credenciales a %s." % (self._name, address[1]))
            friend = credentials.decode().split(":")[0]
            _logger.info("Usuario %s: Ha realizado intercambio de llaves con %s." % (self._name, friend))
            print("Tiene una comunicacion con: %s. Si desea abandonar la conversacion esciba EXIT." % friend)
            while True:
                data = connection.recv(1024)
                if data == b'EXIT':
                    print("%s: Ha finalizado la conversación." % friend)
                    break
                else:
                    print("%s: %s" % (friend, self.__user.decipher_message(data)))
                    message = input("%s: " % self._name)
                    if message != 'EXIT':
                        _logger.info("Usuario %s: Ha escrito un mensaje." % (self._name))
                        connection.sendall(self.__user.cipher_message("%s:%s" % (friend, message)))
                        _logger.info("Usuario %s: Ha enviado un mensaje a %s." % (self._name, friend))
                    else:
                        _logger.info("Usuario %s: Ha dejado la conversación." % self._name)
                        print("Has finalizado la conversación.")
                        connection.sendall(message.encode())
                        break