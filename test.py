from jpake import JPAKE

secret2 = "1235"
secret = "1234"
alice = JPAKE(secret=secret, signer_id=b"alice")
bob = JPAKE(secret=secret, signer_id=b"bob")

alice.process_one(bob.one())
bob.process_one(alice.one())

print(bob.two())

# alice.process_one(bob.one())
# bob.process_one(alice.one())

# alice.process_two(bob.two())
# bob.process_two(alice.two())

#print(alice.K)
#print(bob.K)
#print(eve.k)