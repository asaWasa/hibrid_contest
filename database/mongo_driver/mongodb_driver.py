from database.db_driver_interface import DbDriverInterface
from pymongo import MongoClient

class MongoDBDriver(DbDriverInterface):
    def __init__(self, db_name, col_name, index='id'):
        super().__init__(db_name, col_name)
        self._index = index
        self.__connect_database()

    def __connect_database(self):
        self.client = MongoClient(connectTimeoutMS=300000, serverSelectionTimeoutMS = 300000)
        self.db = self.client[self._db_name]
        self.collection = self.db[self._col_name]
        if self._index is not None:
            self.collection.create_index(self._index)

    def find_records(self, index, values):
        res = []
        for value in values:
            self.__prepare()
            res.append(self.find_one(index, value))
        return res

    def find_list_ids(self, list_ids, index):
        self.__prepare()
        start = 0
        while True:
            try:
                for id in list_ids[start:]:
                    start += 1
                    yield self.collection.find_one({index: id})
                break
            except:
                self.__prepare()

    def push(self, data=None):
        try:
            self.__prepare()
            self.collection.insert_one(data)
        except Exception as e:
            pass

    def update_one(self, item=None):
        try:
            self.__prepare()
            item_id = item['tg_id']
            self.collection.update_one({'tg_id': item_id}, {'$set': item}, upsert=True)
        except Exception as e:
            print(e)

    def find_one(self, key, value):
        self.__prepare()
        return self.collection.find_one({key: value})

    def find(self, key, value):
        self.__prepare()
        return self.collection.find({key: value})

    def get_last_item(self, param='id'):
        self.__prepare()
        return dict(list(self.collection.find().sort(param, -1).limit(1))[0])

    def push_list(self, data_list=None):
        self.__prepare()
        self.collection.insert_many(data_list)

    def push_if_not_exists(self, data, index, value):
        self.__prepare()
        if not self.is_in(index, value):
            self.push(data)

    def pop(self, index=None, value=None):
        try:
            self.__prepare()
            if index is None:
                result = self.collection.find_one_and_delete({})
            else:
                result = self.collection.find_one_and_delete({index: value})
            return result
        except:
            pass

    def is_in(self, index=None, value=None):
        self.__prepare()
        return self.collection.find_one({index: value}) is not None

    def is_empty(self):
        self.__prepare()
        return self.collection.find_one({}) is None

    def clear_collection(self):
        self.db.drop_collection(self._col_name)
        self.restart()

    def restart(self):
        self.__connect_database()

    def count(self):
        self.__prepare()
        count_documents = self.collection.count({})
        return count_documents

    def find_all(self):
        self.__prepare()
        current_pos = 0
        while True:
            try:
                all_docs = self.collection.find(no_cursor_timeout=True).skip(current_pos)
                for doc in all_docs:
                    current_pos += 1
                    yield doc
                break
            except:
                self.__prepare()
    # def find(self, request=dict(), limit=0, skip=0):
    #     self.__prepare()
    #     return self.collection.find(request, no_cursor_timeout=True).skip(skip).limit(limit)

    def search_fields(self, name, value):
        self.__prepare()
        return list(self.collection.find({name: value}))

    def __prepare(self):
        try:
            self.client.server_info()
        except:
            self.restart()
