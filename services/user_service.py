from PWP.database_models import UserProfile, db


def add_user(name, facial_data):
    new_user = UserProfile(name=name, facial_data=facial_data)
    db.session.add(new_user)
    db.session.commit()


def get_user_profile(user_id):
    return UserProfile.query.get(user_id)


def update_user_facial_data(user_id, new_facial_data):
    user = UserProfile.query.get(user_id)
    if user:
        user.facial_data = new_facial_data
        db.session.commit()
        return True
    return False


def delete_user_profile(user_id):
    user = UserProfile.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


if __name__ == "__main__":
    add_user("Tharindu", b"sample_facial_data")
    # Fetch and print user profile
    user = get_user_profile(1)
    print(f"User: {user.name}")
    # Update user facial data
    update_user_facial_data(1, b"new_facial_data")
    # Delete a user profile
    delete_user_profile(1)
