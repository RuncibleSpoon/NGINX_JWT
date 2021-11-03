from jwcrypto import jwt, jwk, jws
# Generate a key
#key2 = jwk.JWK(generate='oct', size=256)
# Keys
keyJson = '{"k":"2o5lO5Zbyvkf6QwzbHZaFc9FMFX4YyRTefgOkQHWzhM","kty":"oct"}'
key2Json = '{"k":"YqIkB4M-wAHeD_lvOiAviMbr8Pn0hec70OByYGBi3xY","kty":"oct"}'
key = jwk.JWK.from_json(keyJson)
key2 = jwk.JWK.from_json(key2Json)
print("###################################")
print("Key 1 is :", key.export())
print("Key 2 is: ", key2.export())
# Generate and sign a token containing the claims
# This works 
print("###################################")
Token = jwt.JWT(header={"alg": "HS256", "typ":"JWS"}, claims={"sub": "123456790", "dest": "saffi","admin": True	, "exp": 1698531606 , "nbf": 1603923606 })
Token.make_signed_token(key)
print("Sign")
signed_Token = Token.serialize(compact=True)
print("Signed Token is: ", signed_Token)

# Encrypt the token. - use key2
# This does not work with my nginx setyo 

Etoken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512", "typ": "JWE"}, claims=signed_Token )
Etoken.make_encrypted_token(key2)
print("Signed Encrypted token is: ", Etoken.serialize(compact=True))

#Decrypt the token
#This decrypts the token ok, and presents the correct claims
ET = jwt.JWT(key=key2, jwt=Etoken.serialize())
print("Decrypted token is: " , ET.serialize())
# Extract the claims
ST = jwt.JWT(key=key, jwt=ET.claims)
print("###################################")
print("Decrypt")
print("Decrypted Claim is: ", ST.claims, "with Headers: ", ST.header)


#
# Try creating a simple encrypted token (not signed)
# This also works
eToken = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512", "typ": "JWE" }, claims={"sub": "123456790", "dest": "saffi","admin": "true", "exp": 1698531606, "nbf": 1603923606 })
eToken.make_encrypted_token(key)
print("###################################")
print("Encrypt")
print ("Simple encrypted token is: ", eToken.serialize())

