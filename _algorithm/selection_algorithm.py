from database.mongo_driver.mongodb_driver import MongoDBDriver
from constants import *
from database.cv_interface import *


class SelectionAlgorithm:
    def __init__(self, ):
        pass

    def get_selection(self, data_user):
        db_driver = MongoDBDriver(USERS_DB.DB, USERS_DB.COLLECTION)
        all_users = []
        for user in db_driver.find_all():
            all_users.append(user)

        all_users_new = []
        main_user_department = set(data_user.department)
        main_user_favorite_coffee = set(data_user.coffee_type)
        for user in all_users:
            user = CVInterface.from_dict(user)
            if user.id == data_user.id:
                continue
            user_department = set(user.department)
            user_favorite_coffee = set(user.coffee_type)

            cnt_department = len(main_user_department & user_department) * 10
            cnt_favorite_coffee = len(main_user_favorite_coffee & user_favorite_coffee) * 5
            all_users_new.append([user, cnt_department + cnt_favorite_coffee])

        if all_users:
            all_users_new.sort(key=lambda x: x[1], reverse=True)
        all_users = all_users_new
        if all_users:
            cnt_res = [[]]
            last = all_users[0][1]
            for user in all_users:
                if user[1] != last:
                    last = user[1]
                    res = [user, user[0].rating]
                    cnt_res.append([res])
                else:
                    cnt_res[-1].append([user, user[0].rating])

            res = []
            for cnt in cnt_res:
                cnt.sort(key= lambda x: x[1], reverse=True)
                for user in cnt:
                    res.append(user[0][0])
            return res
        else:
            return []





    # def add_in_department_index(self, id, department):
    #     pass
    #
    # def add_in_favorite_coffee_index(self, id, favorite_coffee):
    #     pass

