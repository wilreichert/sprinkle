import consulate
import gitlab
import jenkins
import kvdata

c = consulate.Session()
servicebase = 'sprinkle/services/'


class Service:

  name = ''
  server = None

  def __init__(self, name):
    self.name = name

  def access(self):
    url = c.kv.get(servicebase + self.name + '/url')
    user = c.kv.get(servicebase + self.name + '/admin')
    password = c.kv.get(servicebase + self.name + '/password')
    return url, user, password

  def initialize(self):
    print('<<< initialize ' + self.name + ' >>>')

  def auth():
    print('<<< authenticate ' + self.name + ' >>>')

  def create_users(self):
    print('<<< create_users ' + self.name + ' >>>')

  def create_groups(self):
    print('<<< create_groups ' + self.name + ' >>>')


class GitLab(Service):

  def __init__(self, name):
    Service.__init__(self, name)

  def auth(self):
    url, user, password = Service.access(self)
    self.server = gitlab.Gitlab(url, email=user, password=password)
    self.server.auth()
    print('Connected to gitlab')

  def create_users(self):
    for user in kvdata.users():
      print("Creating " + user.username)
      data = {'email': user.email(), 'username': user.username,
              'name': user.name(), 'password': user.password()}
      try:
        user = self.server.users.create(data)
        '''print(user)'''
      except gitlab.exceptions.GitlabCreateError as exc:
        print('User already exists')

  def create_groups(self):
    for group in kvdata.groups():
      try:
        print("Creating " + group.name)
        self.server.groups.create({'name': group.name, 'path': group.name})
      except gitlab.exceptions.GitlabCreateError as exc:
        print('Group already exists')


class Jenkins(Service):

  def __init__(self, name):
    Service.__init__(self, name)

  def auth(self):
    url, user, password = Service.access(self)
    server = jenkins.Jenkins(url, username=user, password=password)
    print('Connected to jenkins version ' + server.get_version())


def servicenames():
  servicenames = []
  data = c.kv.find(servicebase)

  for k in data.keys():
    if 'name' in k:
      servicenames.append(data[k])
  return servicenames


def services():
  print('Creating service objects')
  services = []
  for servicename in servicenames():
    type = c.kv.get(servicebase + servicename + '/type')
    if type == 'gitlab':
      services.append(GitLab(servicename))
    elif type == 'jenkins':
      services.append(Jenkins(servicename))
    else:
      print('Unknown service type ' + type)

  return services
