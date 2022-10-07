import rsa

publicKey, privateKey = rsa.newkeys(512)


def encryption(strr):
    return rsa.encrypt(strr.encode(),
						publicKey)

def decryption(strr):
    return rsa.decrypt(strr, privateKey).decode()