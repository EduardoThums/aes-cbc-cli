#!./venv/bin/python
from os import getcwd, path
from time import sleep
from typing import Union

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

PRIVATE_KEY_EXT = 'pr'
PUBLIC_KEY_EXT = 'pu'
RSA_KEY_SIZE_IN_BITES = 2048
AES_KEY_SIZE_IN_BYTES = 16  # 128 bits


def write_file_as_binary(file_path: str, data: bytes):
    _write_file(file_path, 'wb', data)


def write_file_as_plain(file_path: str, data: str):
    _write_file(file_path, 'w', data)


def _write_file(file_path: str, mode: str, data: Union[bytes, str]):
    with open(file_path, mode) as file:
        file.write(data)


class Encryptor:

    @staticmethod
    def generate_key_pair():
        name = input('Insert your name for the key pair be generated: ')
        # name = 'eduardo'

        print(f'Generating key pair for {name}...')
        sleep(0.5)

        key = RSA.generate(RSA_KEY_SIZE_IN_BITES)

        private_key = key.export_key()
        private_key_name = f'{name}.{PRIVATE_KEY_EXT}'
        write_file_as_binary(f'./src/{private_key_name}', private_key)

        public_key = key.publickey().export_key()
        public_key_name = f'{name}.{PUBLIC_KEY_EXT}'
        write_file_as_binary(f'./src/{public_key_name}', public_key)

        print(f'Private key generated at {getcwd()}/src/{private_key_name}')
        print(f'Public key generated at {getcwd()}/src/{public_key_name}')

    @staticmethod
    def encrypt_symmetric():
        file_path = input('Insert the full file path of the plain file to encrypt it: ')
        # file_path = '/home/eduardo/work/aes-cbc-cli/src/x.txt'

        if not path.exists(file_path):
            print('The given file path does not exist! Returning...')
            return

        key = get_random_bytes(AES_KEY_SIZE_IN_BYTES)
        iv = get_random_bytes(AES_KEY_SIZE_IN_BYTES)

        write_file_as_plain(f'./src/k.txt', key.hex().upper())
        write_file_as_plain(f'./src/iv.txt', iv.hex().upper())

        print(f'Symmetric key generated at {getcwd()}/src/k.txt')
        print(f'Initialization vector generated at {getcwd()}/src/iv.txt')

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)

        with open(file_path, 'rb') as plain:
            data = cipher.encrypt(pad(plain.read(), AES.block_size))

            write_file_as_binary('./src/y.txt', data)

        print(f'Plain text file encrypted at {getcwd()}/src/y.txt')

    @staticmethod
    def encrypt_asymmetric():
        pu_file_path = input('Insert the full file path of the public key used to encrypt it: ')
        # pu_file_path = '/home/eduardo/work/aes-cbc-cli/src/eduardo.pu'

        if not path.exists(pu_file_path):
            print('The given file path does not exist! Returning...')
            return

        file_path = input('Insert the full file path of the file to encrypt it: ')
        # file_path = '/home/eduardo/work/aes-cbc-cli/src/k.txt'

        if not path.exists(file_path):
            print('The given file path does not exist! Returning...')
            return

        public_key = RSA.import_key(open(pu_file_path).read())
        cipher = PKCS1_OAEP.new(public_key)

        with open(file_path, 'rb') as plain:
            data = cipher.encrypt(plain.read())

            og_file_name, ext = path.splitext(file_path)
            enc_file_name = f'{og_file_name}-encrypted{ext}'
            print(f'File encrypted at {enc_file_name}')

            write_file_as_binary(enc_file_name, data)

        # Decrypt
        # private_key = RSA.import_key(open('/home/eduardo/work/aes-cbc-cli/src/eduardo.pr').read())
        # cipher = PKCS1_OAEP.new(private_key)
        #
        # with open('/home/eduardo/work/aes-cbc-cli/src/k-enc.txt', 'rb') as file:
        #     data = cipher.decrypt(file.read())
        #     write_file_as_binary('/home/eduardo/work/aes-cbc-cli/src/message.txt', data)


class Decrypter:

    @staticmethod
    def decrypt_symmetric():
        pass

    @staticmethod
    def decrypt_asymmetric():
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
                self.display_decrypt_menu()

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

            encryptor = Encryptor()

            if choice == 1:
                encryptor.generate_key_pair()

            elif choice == 2:
                encryptor.encrypt_symmetric()

            elif choice == 3:
                encryptor.encrypt_asymmetric()

            elif choice == 5:
                self.exit_with_success()

    def display_decrypt_menu(self):
        choice = None

        while choice != 3:
            print('\n::::::::::::::::::::')
            print('::: DECRYPT MENU :::')
            print('::::::::::::::::::::\n')
            print('1 - Decrypt plain text file (symmetric mode)')
            print('2 - Decrypt file (asymmetric mode)')
            print('3 - Back to main menu')
            print('4 - Exit')

            try:
                choice = int(input('>>> '))

            except ValueError:
                self.show_invalid_entry()
                continue

            if choice not in [1, 2, 3, 4]:
                self.show_unknown_entry()
                continue

            decrypter = Decrypter()

            if choice == 1:
                decrypter.decrypt_symmetric()

            elif choice == 2:
                decrypter.decrypt_asymmetric()

            elif choice == 4:
                self.exit_with_success()

    @staticmethod
    def exit_with_error(message: str):
        print(f'{message}! Exiting...')
        exit(1)

    @staticmethod
    def exit_with_success():
        print('Exiting...')
        sleep(0.5)
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
