class Space:
    def __init__(self, id, name, description, price, user_id, available_from=None, available_to=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.user_id = user_id
        self.available_from = available_from
        self.available_to = available_to

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Space({self.id}, {self.name}, {self.description}, {self.price}, {self.user_id}, {self.available_from}, {self.available_to})"