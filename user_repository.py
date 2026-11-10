from user import User

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all artists
    def create(self, user):
        self._connection.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            [user.username, user.password]
            )
        
        return None
    
    # def find_by_username(self, username):
    #     user_details = self._connection.execute(
    #         'SELECT * FROM users WHERE username = %s', [username]
    #     )[0]

    #     return User(
    #         user_details["username"],
    #         user_details["password"],
    #         user_details["id"]
    #     )

    def find_by_username(self, username):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE username = %s', [username])

        if not rows:          # no match → empty list
            return None

        row = rows[0]
        return User(row["username"], row["password"], row["id"])