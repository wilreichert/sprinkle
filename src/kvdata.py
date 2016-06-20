import yaml

import consulate

userbase = 'sprinkle/users/'
groupbase = 'sprinkle/groups/'
servicebase = 'sprinkle/services/'
c = consulate.Session()


class User:

  username = ''
  default_name = username
  default_domain = '@example.com'
  default_password = 'password'
  default_type = 'human'

  def __init__(self, username):
    self.username = username
    data = c.kv.get(userbase + username + '/username')
    if data == None:
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


class Group:
  name = ''

  def __init__(self, name):
    self.name = name
    data = c.kv.get(groupbase + name + '/name')
    if data == None:
      print(name + ' not found')

  def name(self):
    return self.name

  def users(self):
    return c.kv.get(groupbase + self.name + '/users').split(' ')


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
    c.kv.set(groupbase + group['name'] + '/name', group['name'])
    c.kv.set(groupbase + group['name'] + '/users', ' '.join(group['users']))

  print('Loading services...')
  for service in bootstrap_data['services']:
    for k, v in service.items():
      c.kv.set(servicebase + service['name'] + '/' + k, v)


def usernames():
  usernames = []
  data = c.kv.find(userbase)

  for k in data.keys():
    if 'username' in k:
      usernames.append(data[k])
  return usernames


def users():
  users = []
  for username in usernames():
    users.append(User(username))
  return users


def groupnames():
  groupnames = []
  data = c.kv.find(groupbase)

  for k in data.keys():
    if 'name' in k:
      groupnames.append(data[k])
  return groupnames


def groups():
  groups = []
  for groupname in groupnames():
    groups.append(Group(groupname))
  return groups
