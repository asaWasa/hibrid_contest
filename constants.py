class USERS_DB:
    DB = 'coffee_users'
    COLLECTION = 'users'

class DB_FIELDS:
    ID = 'id'
    TG_ID = 'tg_id'
    TG_IS_BOT = 'tg_is_bot'
    TG_FIRST_NAME = 'tg_first_name'
    TG_USERNAME = 'tg_username'
    TG_LANGUAGE_CODE = 'tg_language_code'
    REAL_NAME = 'real_name'
    FAVORITE_COFFEE = 'favorite_coffee'
    WORK_DEPARTMENT = 'work_department'
    FAMILY_STATUS = 'family_status'
    GENDER = 'gender'
    PREFERRED_GENDER = 'preferred_gender'
    ABOUT = 'about'
    REGISTER_DATE = 'register_date'
    INTERESTS = 'interests'
    RATING = 'rating'


class INTERESTS:
    pass


class DEPARTMENT:
    MARKETING = 0
    FINANCE = 1
    DEV_AND_TESTING = 2
    MEDIA_BAYER = 3
    SALES = 4
    PARTNER_RELATIONS = 5
    MEDIA = 6
    ADMINISTRATIVE_STAFF = 7

    @classmethod
    def in_values(cls, id):
        if id in [DEPARTMENT.MARKETING, DEPARTMENT.FINANCE, DEPARTMENT.DEV_AND_TESTING,
                     DEPARTMENT.MEDIA_BAYER, DEPARTMENT.SALES, DEPARTMENT.PARTNER_RELATIONS, DEPARTMENT.MEDIA, DEPARTMENT.ADMINISTRATIVE_STAFF]:
            return True
        else:
            return False


class COFFEE:
    RISTRETTO = 0
    ESPRESSO = 1
    AMERICANO = 2
    DOUBLE_ESPRESSO = 3
    KAPUCINO = 4
    LATTE = 5
    KAKAO = 6
    MARSHMELLO = 7

    @classmethod
    def in_values(cls, _id):
        if _id in [COFFEE.RISTRETTO, COFFEE.ESPRESSO, COFFEE.AMERICANO, COFFEE.DOUBLE_ESPRESSO, COFFEE.KAPUCINO,
                   COFFEE.LATTE, COFFEE.KAKAO, COFFEE.MARSHMELLO]:
            return True
        else:
            return False
