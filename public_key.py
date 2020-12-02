from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
import logging

_logger = logging.getLogger(__name__)


class PublicKey:
    def __init__(self, name):
        self._name = name
        self._keys_holder = {}
        self.__private_key = generate_eth_key()
        self.__public_key = self._generate_public_key()


    def _generate_public_key(self):
        """
            Función utilizada para generar la llave pública.
        """
        public_key = self.__private_key.public_key.to_hex()
        _logger.info("Usuario %s: Llave pública y privada creadas." % self._name)
        return public_key

    def _share_public_key(self):
        return self.__public_key

    def share_public_key(self):
        return self._share_public_key()

    def add_public_key(self, credentials):
        self._keys_holder.update(credentials)
        _logger.info("Usuario %s: Llave pública agregada con éxito." % self._name)

    def cipher_message(self, message):
        _logger.info("Usuario %s: Está cifrando un mensaje." % self._name)
        friend = message.split(":")[0]
        if friend in self._keys_holder:
            _logger.info("Usuario %s: Llave pública de %s en el llavero personal." % (self._name, friend))
            cypher_messagge = encrypt(self._keys_holder.get(friend), message.split(":")[1].encode())
            _logger.info("Usuario %s: Mensaje cifrado: %s" % (self._name, cypher_messagge))
            return cypher_messagge
        else:
            _logger.error("Usuario %s: Llave pública de %s no está en el llavero personal." % (self._name, friend))
            return False

    def decipher_message(self, data):
        _logger.info("Usuario %s: Está decifrando un mensaje." % self._name)
        decypher_messagge = decrypt(self.__private_key.to_hex(), data)
        _logger.info("Usuario %s: Mensaje decifrado." % self._name)
        return decypher_messagge.decode()
