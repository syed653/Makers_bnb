from user import User

class UserRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection


    def create(self, user):
        char = ["!", "@", "$", "%", "&"]
        if len(user.password) <=7:
            return "password must at leaset 8 characters long and have one special character: ! @ $ % &"
        elif any ((c in char) for c in user.password):
            self._connection.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                [user.username.lower(), user.password]
                )
            return None
        else:
            return "password must at leaset 8 characters long and have one special character: ! @ $ % &"



    # def create(self, user):
    #     self._connection.execute(
    #         'INSERT INTO users (username, password) VALUES (%s, %s)',
    #         [user.username, user.password]
    #         )
        
    #     return None
    
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
            'SELECT * FROM users WHERE username = %s', [username.lower()])

        if not rows:          # no match → empty list
            return None

        row = rows[0]
        return User(row["username"], row["password"], row["id"])

    # Find a user by their id
    def find(self, user_id):
        rows = self._connection.execute(
            'SELECT * FROM users WHERE id = %s', [user_id]
        )
        row = rows[0]
        return User(username=row["username"], password=row["password"], id=row["id"])