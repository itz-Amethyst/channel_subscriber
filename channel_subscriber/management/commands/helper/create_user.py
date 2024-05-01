from core.models import User


def create_author_generate_user(username):
    # create a new user
    new_email = "new_user@example.com"
    new_password = "password123"

    user = User.objects.filter(username = username).first()

    # create user if wasn't in db
    if not user :
        user = User.objects.create_user(
            username = username ,
            email = new_email ,
            password = new_password
        )
        print(f"User '{username}' created successfully.")

        return user
    else:
        return user