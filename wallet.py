from Crypto.PublicKey import RSA  # Generates public and private keys
from Crypto.Signature import PKCS1_v1_5  # Special algorithm that generate signatures
from Crypto.Hash import SHA256
import Crypto.Random  # Generates Random number
import binascii  # Converts binary to ascii and the other way around


class Wallet:
    def __init__(self, node_id):
        # No automatic generates keys
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        # Unpacked tuple
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key is not None and self.private_key is not None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('ERROR:       save_keys       Saving wallet file failed.')
                return False

    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]  # -1 because the character \n when we write the file wallet.txt above
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print('ERROR:       load_keys       Loading wallet file failed.')
            return False

    def generate_keys(self):
        # generate(key_length-it must be a multiple of 256, and no smaller than 1024, +function)
        # Crypto.Random.new().read generates a new random value
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        # should be work together private_key and public key. It only works like that
        # because return the publickey() belongs to private_key
        public_key = private_key.publickey()
        # Tuple - binascii=converts to ascii - hexlify=Hex_representation -
        # exportKey_format=binary or PEM encoding LECTURES:
        # https://www.ietf.org/rfc/rfc1421.txt AND https://www.ietf.org/rfc/rfc1423.txt
        # The field transfers an originator's certificate as a numeric quantity,
        # comprised of the certificate's DER encoding, represented in the
        # header field with the encoding mechanism
        # exportKey(format='DER')) = Generates Hexadecimal representation
        # decode('ascii') turn hex into ascii
        # exportKey(format='DER')).decode('ascii') = return a string representation
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_transaction(self, sender, recipient, amount):
        # private_key is used for signing
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_transaction(transaction):
        # If is MINING sender, we don't have to validate, because MINING does't have a valid signature.
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))
