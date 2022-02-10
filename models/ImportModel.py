from factory.database import Database


class Imports:
    def __init__(self):
        self.db = Database()
        self.collection_name = 'Imports'

    def create(self, data):
        res = self.db.insert(data, self.collection_name)
        return res

    def find(self, data, sort=None):  # find all
        return self.db.find(data, self.collection_name, None, sort)

    def find_by_id(self, _id):
        return self.db.find_by_id(_id, self.collection_name)

    def update(self, _id, data):
        # self.validator.validate(data, self.fields, self.update_required_fields, self.update_optional_fields)
        return self.db.update(_id, data, self.collection_name)
    
    def update_one(self, _id, data):
        return self.db.update_one(_id, data, self.collection_name)

    def upsert(self, _id, user):
        return self.db.upsert(_id, user, self.collection_name)

    def push(self, criteria, upd):
        return self.db.push(criteria, upd, self.collection_name)

    def delete(self, _id):
        return self.db.delete(_id, self.collection_name)

    def count(self):
        return self.db.count(self.collection_name)
