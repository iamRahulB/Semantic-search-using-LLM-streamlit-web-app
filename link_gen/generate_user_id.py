import random
import string

class UserId:
    def __init__(self) -> None:
        pass

    def generate_user_id(self):

        chars=string.ascii_letters + string.digits

        user_id=''.join(random.choice(chars) for _ in range(10))

        print("current user session ID ::::::::::::::::::::::::: ",user_id,"\n")

        return user_id
    
