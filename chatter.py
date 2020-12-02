import subprocess as sub
from threading import Thread
from my_socket import MySocket
from public_key import PublicKey
import logging
logging.basicConfig(filename="chatter.log", level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class Chatter:
    def __init__(self, name):
        self._name = name
        self.__socket = self._set_socket_connection()
        self.__pki = self._set_keys()

    def _set_socket_connection(self):
        logging.info("Usuario %s: Sesión iniciada." % self._name)
        try:
            return MySocket(self)
        except Exception as error:
            logging.info("Usuario %s: Error al tratar de crear socket.\nTraceback:\n %s." % error)
    
    def _set_keys(self):
        logging.info("Usuario %s: Iniciando generación de llaves." % self._name)
        try:
            return PublicKey(self._name)
        except Exception as error:
            logging.info("Usuario %s: Error al tratar de crear llaves.\nTraceback:\n %s." % error)

    def _get_public_key(self):
        return self.__pki.share_public_key()

    def get_public_key(self):
        return self._get_public_key()

    def add_key(self, credentials):
        credentials = credentials.decode().split(":")
        logging.info("Usuario %s: Ingresando llave pública de %s." % (self._name, credentials[0]))
        credentials = {credentials[0]:credentials[1]}
        self.__pki.add_public_key(credentials)

    def cipher_message(self, message):
        cipher_message = self.__pki.cipher_message(message)
        if cipher_message:
            return cipher_message
        else:
            print("E: Ha ocurrido un error con la llave publica. Vuelva a intentarlo.")

    def decipher_message(self, data):
        decipher_message = self.__pki.decipher_message(data)
        if decipher_message:
            return decipher_message
        else:
            print("E: Ha ocurrido un error con la llave privada. Vuelva a intentarlo.")

    def online(self):
        # connection = Thread(target=self.__socket.set_connection, daemon=True)
        self.__socket.set_connection()
        # connection.start()
        # connection.join()

    def search(self, port=None):
        host = self.__socket.get_host()
        if port:
            logging.info("Usuario %s: Buscando contacto." % self._name)
            search = sub.getoutput("netstat -an | grep %s:%s*" % (host, port))
            if not search:
                print("El usuario que intenta conectar ya se ha desconectado.")
        else:
            logging.info("Usuario %s: Buscando contactos." % self._name)
            port = self.__socket.get_port()
            search = sub.getoutput("netstat -an | grep %s:%s*" % (host, port))
            print("Usuarios conectados:")
            print(" - %s" % "\n - ".join((port.split(":")[1].split(" ")[0] for port in search.split("\n"))))

    def connect(self, port):
        self.search(port)
        logging.info("Usuario %s: Conectando con %s." % (self._name, port))
        self.__socket.get_connection(port)




if __name__ == "__main__":
    print("¡Bienvenido!")
    nickname = input("Ingrese su nombre de usuario: ")
    user = Chatter(nickname)
    # user.online()
    connection = Thread(target=user.online, daemon=True)
    connection.start()
    # def menu():
    while True:
        print("Acciones:\n  1) Conectarse.\n  2) Buscar contactos.\n  3) Salir.")
        action = input("¿Que accion desea realizar? ")
        if action == '1':
            user.online()
        elif action == '2':
            user.search()
            response = input("¿Desea conectar con alguno de los usuarios? (Y/n) ")
            if response == 'Y':
                port = input("Indique el puerto con el que desea comunicarse: ")
                user.connect(port)
        elif action == '3':
            print("¡Adiós!")
            break
        else:
            print("No ha seleccionado una accion valida. Intente otra vez.")
