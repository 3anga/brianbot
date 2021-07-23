import sqlite3


class Database:
    def __init__(self, **kw):
        self.db = kw['db']
        self.connection = sqlite3.connect(kw['db'],
                                          isolation_level=None,
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()
    
    def __str__(self):
        return f"<Database '{self.db}'>"
    
    def profileExists(self, DISCORDID = None):
        if self.getProfile(DISCORDID) is None: return False
        return True
    
    def getProfile(self, DISCORDID = None):
        with self.connection:
            PROFILE = self.cursor.execute(f"SELECT * FROM profiles WHERE discordId={DISCORDID}").fetchone()
        if PROFILE is None: return None
        return {
            'discordId': PROFILE[0],
            'hashSource': PROFILE[1],
            'vkId': PROFILE[2],
            'msgCount': PROFILE[3],
            'level': PROFILE[4],
            'isPatriot': PROFILE[5],
            'isMilitary': PROFILE[6],
            'isBanned': PROFILE[7],
            'warns': PROFILE[8],
            'dateCreated': str(PROFILE[9])
        }
    
    def updateProfile(self, DISCORDID = None, NEWDATA = None):
        if self.profileExists(DISCORDID) is True:
            set_ = ''
            lastValue = list(NEWDATA.values())[-1]
            for key, value in NEWDATA.items():
                set_ += f"{key}={value}"
                if value != lastValue: set_ += ","
            with self.connection:
                return self.cursor.execute(f"UPDATE profiles SET {set_} WHERE discordId={DISCORDID}")
        else:
            return None
    
    def createProfile(self, **kw):
        if self.profileExists(kw['discordId']) is False:
            values = ''
            lastValue = list(kw.values())[-1]
            for key, value in kw.items():
                values += "?"
                if value != lastValue: values += ","
            with self.connection:
                return self.cursor.execute(f"INSERT INTO profiles ({','.join(list(kw.keys()))}) VALUES ({values})", tuple(kw.values()))
        else: return None