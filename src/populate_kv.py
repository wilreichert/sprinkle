import consul
import yaml

with open("bootstrap.yaml", 'r') as stream:
  try:
    bootstrap_data = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)

c = consul.Consul()

for user in bootstrap_data['users']:
  for k,v in user.items():
    print ('sprinkle/users/' + user['username'] + '/' + k + ' = ' + v)
    c.kv.put('sprinkle/users/' + user['username'] + '/' + k, v)
