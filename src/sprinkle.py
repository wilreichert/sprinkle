import kvdata

kvdata.bulkload('bootstrap.yaml')

users = kvdata.usernames()
print(users)

admin = kvdata.User('admin')
admin.email()
