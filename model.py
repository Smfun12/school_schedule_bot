 
class Group:
 
    def __init__(self, date, time, link, available_place=0, usersId=[]):
        self.date = date
        self.time = time
        self.link = link
        self.available_place = available_place
        self.usesrId = usersId
        
    def addUser(self, userId):
        usersId.append(userId)
        
    def contains(self, userId):
        if user in self.usersId:
            return True
        else:
            return False
            
    def __str__(self):
        return 'Години:' + self.time + ', к-сть вільних місць=' + str(self.available_place)