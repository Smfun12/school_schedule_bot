from model import User, Group
from SheetsProcessor import fetch_user_with_groups

def find_user_by_id(id, users):
    for user in users:
        if str(user.id) == str(id):
            return user
    return None

def user_is_in_group(user_id, group_id, users):
    user = find_user_by_id(user_id, users)
    if user is None:
        raise Exception('User not found')
    return str(group_id) == str(user.group)
    
    
def find_user_by_username(username, users):
    for user in users:
        if user.username == username:
            return user

def is_admin(id, admin_ids):
    return str(id) in admin_ids

def user_in_group(group, user):
    return str(user.group) == str(group.id)

def fetch_data():
    ids, usernames, fetch_groups = fetch_user_with_groups()
    users_copy = []
    new_groups = [Group(1, '01/03 15:00-17:00', 'link', 25, []), Group(2, '02/03 10:00-12:00', 'link', 30, [])]

    for i in range(0, len(ids)):
        if ids[i] == '':
            continue
        user = User(ids[i], usernames[i],'',fetch_groups[i])
        users_copy.append(user)
        for el in new_groups:
            if user_in_group(el, user):
                el.users.append(user)
                el.available_place -= 1
                break
    return new_groups, users_copy

