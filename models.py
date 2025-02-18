class User:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age
        
    @staticmethod
    def from_db_row(row):
        return User(row[0], row[1], row[2])
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }