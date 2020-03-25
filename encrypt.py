#!/usr/bin/env python3
"""
usage: encrypt.py [-h] [-i INPUT] [-o OUTPUT] [-e] [-g]
                  [--public-key PUBLIC_KEY] [--private-key PRIVATE_KEY]

Creates encrypted secrets file which can be committed to repo or can be used
in CI/CD.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path to be encrypted
  -o OUTPUT, --output OUTPUT
                        Output file path
  -e, --use-env         Use environment variable
  -g, --generate        Generate random strong Public key and Private key
  --public-key PUBLIC_KEY
                        Public key of 16 character
  --private-key PRIVATE_KEY
                        Private key which can be of 16, 24, 32 character
"""

import sys
import os
import random
import string

import argparse
from Crypto.Cipher import AES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT_FILE = 'secrets.json'
DEFAULT_OUTPUT_FILE = '.secrets_dump'


def get_random_password(size):
    """
    Generates a random password

    :param size: max length of password
    :return: A random password
    """
    return "".join([random.choice(string.digits + string.ascii_letters) for _ in range(size)])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Creates encrypted secrets file which can be '
                    'committed to repo or can be used in CI/CD.'
    )

    # Input file
    parser.add_argument(
        '-i', '--input',
        default=DEFAULT_INPUT_FILE,
        help='Input file path to be encrypted'
    )

    # Output file
    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT_FILE,
        help='Output file path'
    )

    # Use environment variables for key
    parser.add_argument(
        '-e', '--use-env',
        default=False,
        action='store_true',
        help='Use environment variable'
    )

    # Generate Public and private key
    parser.add_argument(
        '-g', '--generate',
        default=False,
        action='store_true',
        help='Generate random strong Public key and Private key'
    )

    # Public key
    parser.add_argument(
        '--public-key',
        default=None,
        help='Public key of 16 character'
    )

    # Private key
    parser.add_argument(
        '--private-key',
        default=None,
        help='Private key which can be of 16, 24, 32 character'
    )

    args = parser.parse_args()

    input_file_name = args.input
    output_file_name = args.output

    generate = args.generate
    use_env = args.use_env

    private_key = args.private_key
    public_key = args.public_key

    if generate and use_env:
        print('Can\'t use both -g/--generate and -e/--use-env at same')
        sys.exit(1)

    if not private_key:
        if generate:
            private_key = get_random_password(32)
            print('=' * 100)
            print('PRIVATE KEY:', private_key)
            print('=' * 100)
        elif use_env:
            private_key = os.environ['DJANGO_CONFIG_PRIVATE_KEY']
        else:
            print('Private key is required, if not provided use -g/-generate or -e/--use-env.')
            sys.exit(1)

    if not public_key:
        if generate:
            public_key = get_random_password(16)
            print('=' * 100)
            print('PUBLIC KEY:', public_key)
            print('=' * 100)
        elif use_env:
            public_key = os.environ['DJANGO_CONFIG_PUBLIC_KEY']
        else:
            print('Public key is required, if not provided use -g/-generate or -e/--use-env.')
            sys.exit(1)

    input_file_path = os.path.join(BASE_DIR, input_file_name)
    output_file_path = os.path.join(BASE_DIR, output_file_name)

    with open(input_file_path, 'r') as input_file:
        input_file_content = input_file.read()

        obj = AES.new(private_key, AES.MODE_CFB, public_key)
        cipher_text = obj.encrypt(input_file_content)

        output_file = open(output_file_path, 'wb+')
        output_file.write(cipher_text)

        print(f'Encrypted {input_file_name} -> {output_file_name}')
