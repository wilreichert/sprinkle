import consulate
import gitlab
import jenkins

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
    print('initialize')

  def create_groups(self):
    print('create_groups')

  def create_users(self):
    print('create_users')


class GitLab(Service):

  def __init__(self, name):
    Service.__init__(self, name)

    url, user, password = Service.access(self)
    server = gitlab.Gitlab(url, email=user, password=password)
    server.auth()
    print('connected to gitlab')


class Jenkins(Service):

  def __init__(self, name):
    Service.__init__(self, name)

    url, user, password = Service.access(self)
    server = jenkins.Jenkins(url, username=user, password=password)
    print('connected to jenkins version ' + server.get_version())


def servicenames():
  servicenames = []
  data = c.kv.find(servicebase)

  for k in data.keys():
    if 'name' in k:
      servicenames.append(data[k])
  return servicenames


def services():
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
