import yaml

import consulate

userbase = 'sprinkle/users/'
groupbase = 'sprinkle/groups/'
c = consulate.Session()


class User:

  username = ''
  default_name = username
  default_domain = '@example.com'
  default_password = 'password'
  default_type = 'human'

  def __init__(self, username):
    self.username = username
    userdata = c.kv.get(userbase + username + '/username')
    if userdata == None:
      print(username + ' not found')

  def username(self):
    return self.username

  def name(self):
    return c.kv.get(userbase + self.username + '/name')

  def email(self):
    return c.kv.get(userbase + self.username + '/email')

  def password(self):
    return c.kv.get(userbase + self.username + '/password')

  def private_ssh_key(self):
    return c.kv.get(userbase + self.username + '/private_ssh_key')

  def public_ssh_key(self):
    return c.kv.get(userbase + self.username + '/public_ssh_key')

  def type(self):
    return c.kv.get(userbase + self.username + '/type')


def bulkload(data):
  with open(data, 'r') as stream:
    try:
      bootstrap_data = yaml.load(stream)
    except yaml.YAMLError as exc:
      print(exc)

  print('Loading users...')
  for user in bootstrap_data['users']:
    for k, v in user.items():
      c.kv.set(userbase + user['username'] + '/' + k, v)

  print('Loading groups...')
  for group in bootstrap_data['groups']:
    for k, v in group.items():
      c.kv.set(groupbase + group['name'] + '/' + k, v)


def usernames():
  usernames = []
  userdata = c.kv.find(userbase)

  for k in userdata.keys():
    if 'username' in k:
      usernames.append(userdata[k])
  return usernames


def users():
  users = []
  for username in usernames():
    users.append(User(username))
  return users
