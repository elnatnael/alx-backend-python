from itertools import islice
stream_users_module = __import__('0-stream_users')
stream_users = stream_users_module.stream_users  # get the function from the module

for user in islice(stream_users(), 6):
    print(user)

