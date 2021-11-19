#!./venv/bin/python
from cryptography.hazmat.primitives._serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat

from cryptography.hazmat.primitives.asymmetric import rsa

KEY_SIZE_IN_BITS = 512


class App:

    def encrypt(self):
        # name = input('Insert your name for the key pair be generated: ')
        name = 'eduardo'

        self._generate_key_pair(name)

        # file_path = input('Insert the full path of the file to be encrypted(Ex: /path/to/file.txt): ')
        file_path = '/home/eduardothums/Downloads/file.txt'
        self._encrypt_file(file_path)

    def decrypt(self):
        pass

    @staticmethod
    def _generate_key_pair(name: str):
        print(f'Generating key pair for {name}')

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=KEY_SIZE_IN_BITS
        )

        private_bytes = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )

        with open(f'{name}.pr', 'wb') as file:
            file.write(private_bytes)

        public_key = private_key.public_key()

        public_bytes = public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        with open(f'{name}.pu', 'wb') as file:
            file.write(public_bytes)

    def _encrypt_file(self, file_path):
        pass


if __name__ == '__main__':
    print('How you wanna use the CLI?')
    print('E - Encrypt something')
    print('D - Decrypt something')

    step = input()

    if step not in ['E', 'D']:
        print('Invalid action! Exiting...')
        exit(1)

    app = App()

    if step == 'E':
        print('===ENCRYPT===')
        app.encrypt()

    else:
        print('===DECRYPT===')
        app.decrypt()
