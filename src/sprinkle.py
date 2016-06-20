import kvdata
import service

kvdata.bulkload('bootstrap.yaml')

'''
users = kvdata.usernames()
print(users)

admin = kvdata.User('admin')
print(admin.email())

groups = kvdata.groupnames()
print(groups)

dev = kvdata.Group('developers')
print(dev.users())
'''

services = service.services()
