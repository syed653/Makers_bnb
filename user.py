class User:
    def __init__(self, username, password, id=None):
        self.id = id
        self.username = username
        self.password = password

    # This tells Python how to compare two Artists. 
    # Without this, Python only checks if they are the same object in memory. 
    # With this, it checks if their data (like name and genre) matches.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # This controls what you see when you print(artist).
    # Instead of seeing a confusing code like <Artist object at 0x102...>, 
    # you'll see the actual ID, Name, and Genre, which is much more useful to us humans
    def __repr__(self):
        return f"User({self.id}, {self.username}, {self.password})"