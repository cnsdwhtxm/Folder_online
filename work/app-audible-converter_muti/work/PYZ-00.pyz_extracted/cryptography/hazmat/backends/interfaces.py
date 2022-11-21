# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cryptography\hazmat\backends\interfaces.py
import abc, typing
if typing.TYPE_CHECKING:
    from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.base import Certificate, CertificateBuilder, CertificateRevocationList, CertificateRevocationListBuilder, CertificateSigningRequest, CertificateSigningRequestBuilder, RevokedCertificate, RevokedCertificateBuilder
    from cryptography.x509.name import Name

class CipherBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def cipher_supported(self, cipher, mode):
        """
        Return True if the given cipher and mode are supported.
        """
        pass

    @abc.abstractmethod
    def create_symmetric_encryption_ctx(self, cipher, mode):
        """
        Get a CipherContext that can be used for encryption.
        """
        pass

    @abc.abstractmethod
    def create_symmetric_decryption_ctx(self, cipher, mode):
        """
        Get a CipherContext that can be used for decryption.
        """
        pass


class HashBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def hash_supported(self, algorithm):
        """
        Return True if the hash algorithm is supported by this backend.
        """
        pass

    @abc.abstractmethod
    def create_hash_ctx(self, algorithm):
        """
        Create a HashContext for calculating a message digest.
        """
        pass


class HMACBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def hmac_supported(self, algorithm):
        """
        Return True if the hash algorithm is supported for HMAC by this
        backend.
        """
        pass

    @abc.abstractmethod
    def create_hmac_ctx(self, key, algorithm):
        """
        Create a context for calculating a message authentication code.
        """
        pass


class CMACBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def cmac_algorithm_supported(self, algorithm):
        """
        Returns True if the block cipher is supported for CMAC by this backend
        """
        pass

    @abc.abstractmethod
    def create_cmac_ctx(self, algorithm):
        """
        Create a context for calculating a message authentication code.
        """
        pass


class PBKDF2HMACBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def pbkdf2_hmac_supported(self, algorithm):
        """
        Return True if the hash algorithm is supported for PBKDF2 by this
        backend.
        """
        pass

    @abc.abstractmethod
    def derive_pbkdf2_hmac(self, algorithm, length, salt, iterations, key_material):
        """
        Return length bytes derived from provided PBKDF2 parameters.
        """
        pass


class RSABackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_rsa_private_key(self, public_exponent, key_size):
        """
        Generate an RSAPrivateKey instance with public_exponent and a modulus
        of key_size bits.
        """
        pass

    @abc.abstractmethod
    def rsa_padding_supported(self, padding):
        """
        Returns True if the backend supports the given padding options.
        """
        pass

    @abc.abstractmethod
    def generate_rsa_parameters_supported(self, public_exponent, key_size):
        """
        Returns True if the backend supports the given parameters for key
        generation.
        """
        pass

    @abc.abstractmethod
    def load_rsa_private_numbers(self, numbers):
        """
        Returns an RSAPrivateKey provider.
        """
        pass

    @abc.abstractmethod
    def load_rsa_public_numbers(self, numbers):
        """
        Returns an RSAPublicKey provider.
        """
        pass


class DSABackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_dsa_parameters(self, key_size):
        """
        Generate a DSAParameters instance with a modulus of key_size bits.
        """
        pass

    @abc.abstractmethod
    def generate_dsa_private_key(self, parameters):
        """
        Generate a DSAPrivateKey instance with parameters as a DSAParameters
        object.
        """
        pass

    @abc.abstractmethod
    def generate_dsa_private_key_and_parameters(self, key_size):
        """
        Generate a DSAPrivateKey instance using key size only.
        """
        pass

    @abc.abstractmethod
    def dsa_hash_supported(self, algorithm):
        """
        Return True if the hash algorithm is supported by the backend for DSA.
        """
        pass

    @abc.abstractmethod
    def dsa_parameters_supported(self, p, q, g):
        """
        Return True if the parameters are supported by the backend for DSA.
        """
        pass

    @abc.abstractmethod
    def load_dsa_private_numbers(self, numbers):
        """
        Returns a DSAPrivateKey provider.
        """
        pass

    @abc.abstractmethod
    def load_dsa_public_numbers(self, numbers):
        """
        Returns a DSAPublicKey provider.
        """
        pass

    @abc.abstractmethod
    def load_dsa_parameter_numbers(self, numbers):
        """
        Returns a DSAParameters provider.
        """
        pass


class EllipticCurveBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def elliptic_curve_signature_algorithm_supported(self, signature_algorithm, curve):
        """
        Returns True if the backend supports the named elliptic curve with the
        specified signature algorithm.
        """
        pass

    @abc.abstractmethod
    def elliptic_curve_supported(self, curve):
        """
        Returns True if the backend supports the named elliptic curve.
        """
        pass

    @abc.abstractmethod
    def generate_elliptic_curve_private_key(self, curve):
        """
        Return an object conforming to the EllipticCurvePrivateKey interface.
        """
        pass

    @abc.abstractmethod
    def load_elliptic_curve_public_numbers(self, numbers):
        """
        Return an EllipticCurvePublicKey provider using the given numbers.
        """
        pass

    @abc.abstractmethod
    def load_elliptic_curve_private_numbers(self, numbers):
        """
        Return an EllipticCurvePrivateKey provider using the given numbers.
        """
        pass

    @abc.abstractmethod
    def elliptic_curve_exchange_algorithm_supported(self, algorithm, curve):
        """
        Returns whether the exchange algorithm is supported by this backend.
        """
        pass

    @abc.abstractmethod
    def derive_elliptic_curve_private_key(self, private_value, curve):
        """
        Compute the private key given the private value and curve.
        """
        pass


class PEMSerializationBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_pem_private_key(self, data, password):
        """
        Loads a private key from PEM encoded data, using the provided password
        if the data is encrypted.
        """
        pass

    @abc.abstractmethod
    def load_pem_public_key(self, data):
        """
        Loads a public key from PEM encoded data.
        """
        pass

    @abc.abstractmethod
    def load_pem_parameters(self, data):
        """
        Load encryption parameters from PEM encoded data.
        """
        pass


class DERSerializationBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_der_private_key(self, data, password):
        """
        Loads a private key from DER encoded data. Uses the provided password
        if the data is encrypted.
        """
        pass

    @abc.abstractmethod
    def load_der_public_key(self, data):
        """
        Loads a public key from DER encoded data.
        """
        pass

    @abc.abstractmethod
    def load_der_parameters(self, data):
        """
        Load encryption parameters from DER encoded data.
        """
        pass


class X509Backend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def create_x509_csr(self, builder: 'CertificateSigningRequestBuilder', private_key: 'PRIVATE_KEY_TYPES', algorithm: typing.Optional['hashes.HashAlgorithm']) -> 'CertificateSigningRequest':
        """
        Create and sign an X.509 CSR from a CSR builder object.
        """
        pass

    @abc.abstractmethod
    def create_x509_certificate(self, builder: 'CertificateBuilder', private_key: 'PRIVATE_KEY_TYPES', algorithm: typing.Optional['hashes.HashAlgorithm']) -> 'Certificate':
        """
        Create and sign an X.509 certificate from a CertificateBuilder object.
        """
        pass

    @abc.abstractmethod
    def create_x509_crl(self, builder: 'CertificateRevocationListBuilder', private_key: 'PRIVATE_KEY_TYPES', algorithm: typing.Optional['hashes.HashAlgorithm']) -> 'CertificateRevocationList':
        """
        Create and sign an X.509 CertificateRevocationList from a
        CertificateRevocationListBuilder object.
        """
        pass

    @abc.abstractmethod
    def create_x509_revoked_certificate(self, builder: 'RevokedCertificateBuilder') -> 'RevokedCertificate':
        """
        Create a RevokedCertificate object from a RevokedCertificateBuilder
        object.
        """
        pass

    @abc.abstractmethod
    def x509_name_bytes(self, name: 'Name') -> bytes:
        """
        Compute the DER encoded bytes of an X509 Name object.
        """
        pass


class DHBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def generate_dh_parameters(self, generator, key_size):
        """
        Generate a DHParameters instance with a modulus of key_size bits.
        Using the given generator. Often 2 or 5.
        """
        pass

    @abc.abstractmethod
    def generate_dh_private_key(self, parameters):
        """
        Generate a DHPrivateKey instance with parameters as a DHParameters
        object.
        """
        pass

    @abc.abstractmethod
    def generate_dh_private_key_and_parameters(self, generator, key_size):
        """
        Generate a DHPrivateKey instance using key size only.
        Using the given generator. Often 2 or 5.
        """
        pass

    @abc.abstractmethod
    def load_dh_private_numbers(self, numbers):
        """
        Load a DHPrivateKey from DHPrivateNumbers
        """
        pass

    @abc.abstractmethod
    def load_dh_public_numbers(self, numbers):
        """
        Load a DHPublicKey from DHPublicNumbers.
        """
        pass

    @abc.abstractmethod
    def load_dh_parameter_numbers(self, numbers):
        """
        Load DHParameters from DHParameterNumbers.
        """
        pass

    @abc.abstractmethod
    def dh_parameters_supported(self, p, g, q=None):
        """
        Returns whether the backend supports DH with these parameter values.
        """
        pass

    @abc.abstractmethod
    def dh_x942_serialization_supported(self):
        """
        Returns True if the backend supports the serialization of DH objects
        with subgroup order (q).
        """
        pass


class ScryptBackend(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def derive_scrypt(self, key_material, salt, length, n, r, p):
        """
        Return bytes derived from provided Scrypt parameters.
        """
        pass

    @abc.abstractmethod
    def scrypt_supported(self):
        """
        Return True if Scrypt is supported.
        """
        pass


class Backend(CipherBackend, CMACBackend, DERSerializationBackend, DHBackend, DSABackend, EllipticCurveBackend, HashBackend, HMACBackend, PBKDF2HMACBackend, RSABackend, PEMSerializationBackend, ScryptBackend, X509Backend, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def load_pem_pkcs7_certificates(self, data):
        """
        Returns a list of x509.Certificate
        """
        pass

    @abc.abstractmethod
    def load_der_pkcs7_certificates(self, data):
        """
        Returns a list of x509.Certificate
        """
        pass

    @abc.abstractmethod
    def pkcs7_sign(self, builder, encoding, options):
        """
        Returns bytes
        """
        pass

    @abc.abstractmethod
    def load_key_and_certificates_from_pkcs12(self, data, password):
        """
        Returns a tuple of (key, cert, [certs])
        """
        pass

    @abc.abstractmethod
    def serialize_key_and_certificates_to_pkcs12(self, name, key, cert, cas, encryption_algorithm):
        """
        Returns bytes
        """
        pass