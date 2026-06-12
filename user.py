import hashlib

class User:
    def __init__(self, username, password, role="member"):
        self.username = username
        self.password = self.hash_password(password)
        self.role = role

    def hash_password(self,password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self,password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        return {
            "username":self.username,
            "password":self.password,
            "role":self.role
        }
