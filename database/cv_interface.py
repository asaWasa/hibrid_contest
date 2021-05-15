from constants import *

class CVInterface:
    def __init__(self, id, tg_id, tg_is_bot, tg_first_name, tg_username,
                 tg_language_code, real_name, favorite_coffee, work_department,
                 family_status, gender, preferred_gender, about, register_date, interests=[], rating=5.0):
        self.id = id
        self.tg_id = tg_id
        self.tg_is_bot = tg_is_bot
        self.tg_first_name = tg_first_name
        self.tg_username = tg_username
        self.tg_language_code = tg_language_code
        self.real_name = real_name
        self.favorite_coffee = favorite_coffee
        self.work_department = work_department
        self.family_status = family_status
        self.gender = gender
        self.preferred_gender = preferred_gender
        self.about = about
        self.register_date = register_date
        self.interests = interests
        self.rating = rating

    def to_dict(self):
        res = dict()
        res[DB_FIELDS.ID] = self.id
        res[DB_FIELDS.TG_ID] = self.tg_id
        res[DB_FIELDS.TG_IS_BOT] = self.tg_is_bot
        res[DB_FIELDS.TG_FIRST_NAME] = self.tg_first_name
        res[DB_FIELDS.TG_USERNAME] = self.tg_username
        res[DB_FIELDS.TG_LANGUAGE_CODE] = self.tg_language_code
        res[DB_FIELDS.REAL_NAME] = self.real_name
        res[DB_FIELDS.FAVORITE_COFFEE] = self.favorite_coffee
        res[DB_FIELDS.WORK_DEPARTMENT] = self.work_department
        res[DB_FIELDS.FAMILY_STATUS] = self.family_status
        res[DB_FIELDS.GENDER] = self.gender
        res[DB_FIELDS.PREFERRED_GENDER] = self.preferred_gender
        res[DB_FIELDS.ABOUT] = self.about
        res[DB_FIELDS.REGISTER_DATE] = self.register_date
        res[DB_FIELDS.INTERESTS] = self.interests
        res[DB_FIELDS.RATING] = self.rating
        return res

    @classmethod
    def from_dict(cls, data_dict):
        id = data_dict[DB_FIELDS.ID]
        tg_id = data_dict[DB_FIELDS.TG_ID]
        tg_is_bot = data_dict[DB_FIELDS.TG_IS_BOT]
        tg_first_name = data_dict[DB_FIELDS.TG_FIRST_NAME]
        tg_username = data_dict[DB_FIELDS.TG_USERNAME]
        tg_language_code = data_dict[DB_FIELDS.TG_LANGUAGE_CODE]
        real_name = data_dict[DB_FIELDS.REAL_NAME]
        favorite_coffee = data_dict[DB_FIELDS.FAVORITE_COFFEE]
        work_department = data_dict[DB_FIELDS.WORK_DEPARTMENT]
        family_status = data_dict[DB_FIELDS.FAMILY_STATUS]
        gender = data_dict[DB_FIELDS.GENDER]
        preferred_gender = data_dict[DB_FIELDS.PREFERRED_GENDER]
        about = data_dict[DB_FIELDS.ABOUT]
        register_date = data_dict[DB_FIELDS.REGISTER_DATE]
        interests = data_dict[DB_FIELDS.INTERESTS]
        rating = data_dict[DB_FIELDS.RATING]
        return cls(id, tg_id, tg_is_bot, tg_first_name, tg_username,
                 tg_language_code, real_name, favorite_coffee, work_department,
                 family_status, gender, preferred_gender, about, register_date, interests, rating)
