class BotObject:
    def __init__(self, groups, users, admin_telegram_ids, writeName):
        self.groups = groups
        self.users = users
        self.admin_telegram_ids = admin_telegram_ids
        self.writeName = writeName



class User: 
    def __init__(self, id, username, description='description', group=None):
        self.id = id
        self.username = username
        self.description = description
        self.group = group

    def __str__(self):
        return 'Користувач:' + str(self.id) + ',' + self.username + ','+ self.description + ', групи=' + str(self.group)


 
class Group:
 
    def __init__(self, id, description, link, available_place=0, users=[]):
        self.id = id
        self.description = str(id) + '.Група:' + description
        self.link = link
        self.available_place = available_place
        self.users = users
        
    def addUser(self, userId):
        self.users.append(userId)
        
    def remains(self):
        return self.available_place;
        
    def contains(self, userId):
        if user in self.usersId:
            return True
        else:
            return False
            
    def __str__(self):
        return 'Група:' + str(self.users) + ', к-сть вільних місць=' + str(self.available_place)
