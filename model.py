class User: 
    def __init__(self, id, username, groups=[]):
        self.id = id
        self.username = username
        self.groups = groups

    def __str__(self):
        return 'Користувач:' + self.username + ', групи=' + str(self.groups)


 
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
        return self.available_place - len(self.users);
        
    def contains(self, userId):
        if user in self.usersId:
            return True
        else:
            return False
            
    def __str__(self):
        return 'Група:' + str(self.users) + ', к-сть вільних місць=' + str(self.available_place)
