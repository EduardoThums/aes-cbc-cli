#!./venv/bin/python
from cryptography.hazmat.primitives._serialization import Encoding, PrivateFormat, NoEncryption, PublicFormat

from cryptography.hazmat.primitives.asymmetric import rsa
from time import sleep
from os import getcwd

KEY_SIZE_IN_BITS = 512


class Encrypter:

    # def generate_(self):
    # name = input('Insert your name for the key pair be generated: ')
    # name = 'eduardo'

    # self._generate_key_pair(name)

    # # file_path = input('Insert the full path of the file to be encrypted(Ex: /path/to/file.txt): ')
    # file_path = '/home/eduardothums/Downloads/file.txt'
    # self._encrypt_file(file_path)

    @staticmethod
    def generate_key_pair():
        # name = input('Insert your name for the key pair be generated: ')
        name = 'eduardo'
        print(f'Generating key pair for {name}...')
        sleep(1)

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=KEY_SIZE_IN_BITS
        )

        private_bytes = private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )

        with open(f'./src/{name}.pr', 'wb') as file:
            file.write(private_bytes)

        public_key = private_key.public_key()

        public_bytes = public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )

        with open(f'./src/{name}.pu', 'wb') as file:
            file.write(public_bytes)

        print(f'Private key generated at {getcwd()}/{name}.pr')
        print(f'Public key generated at {getcwd()}/{name}.pr')

    def _encrypt_file(self, file_path):
        pass


class Menu:

    def display_main(self):
        print('Welcome to the AES CBC CLI!')

        choice = None

        while choice != 3:
            print('\n:::::::::::::::::')
            print('::: MAIN MENU :::')
            print(':::::::::::::::::\n')
            print('1 - Encryption')
            print('2 - Decryption')
            print('3 - Exit')

            try:
                choice = int(input('>>> '))

            except ValueError:
                self.exit_with_error('Invalid entry')

            if choice not in [1, 2, 3]:
                self.exit_with_error('Unknown menu entry')

            if choice == 1:
                self.display_encrypt_menu()

            elif choice == 2:
                print('Decrpyt')

            else:
                self.exit_with_success()

    def display_encrypt_menu(self):
        choice = None

        while choice != 4:
            print('\n::::::::::::::::::::')
            print('::: ENCRYPT MENU :::')
            print('::::::::::::::::::::\n')
            print('1 - Generate key pair')
            print('2 - Encrypt plain text file (symmetric mode)')
            print('3 - Encrypt file (asymmetric mode)')
            print('4 - Back to main menu')
            print('5 - Exit')

            try:
                choice = int(input('>>> '))

            except ValueError:
                self.show_invalid_entry()
                continue

            if choice not in [1, 2, 3, 4, 5]:
                self.show_unknown_entry()
                continue

            encrypter = Encrypter()

            if choice == 1:
                encrypter.generate_key_pair()

            elif choice == 2:
                print('encrpy plain text file')

            elif choice == 3:
                print('encrpy file')

            elif choice == 5:
                self.exit_with_success()

    @staticmethod
    def exit_with_error(message: str):
        print(f'{message}! Exiting...')
        exit(1)

    @staticmethod
    def exit_with_success():
        print('Exiting...')
        sleep(1)
        exit(0)

    @staticmethod
    def show_invalid_entry():
        print('Invalid entry! Returning...')

    @staticmethod
    def show_unknown_entry():
        print('Unknown entry! Returning...')


if __name__ == '__main__':
    menu = Menu()

    menu.display_main()
