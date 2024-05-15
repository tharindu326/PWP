from database_models import UserProfile, db


def add_user(name, facial_data):
    """
    Adds a new user to the database.
    Args:
        name (str): The name of the user.
        facial_data (bytes): The facial data of the user.
    Returns:
        int: The ID of the newly created user.
    """
    new_user = UserProfile(name=name, facial_data=facial_data)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id


def get_users_by_name(user_name):
    """
    Retrieves users from the database by name.
    Args:
        user_name (str): The name of the users to retrieve.
    Returns:
        list: A list of UserProfile objects matching the specified name.
    """
    return UserProfile.query.filter_by(name=user_name).all()


def get_user_profile(user_id):
    """
    Retrieves a user's profile from the database by user ID.
    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        UserProfile: The UserProfile object corresponding to the specified user ID, or None if not found.
    """
    return UserProfile.query.get(user_id)


def update_user_facial_data(user_id, new_facial_data):
    """
    Updates the facial data of an existing user.
    Args:
        user_id (int): The ID of the user to update.
        new_facial_data (bytes): The new facial data to assign to the user.
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    user = UserProfile.query.get(user_id)
    if user:
        user.facial_data = new_facial_data
        db.session.commit()
        return True
    return False


def delete_user_profile(user_id):
    """
    Deletes a user's profile from the database by user ID.
    Args:
        user_id (int): The ID of the user to delete.
    Returns:
        bool: True if the deletion was successful, False otherwise.
    """
    user = UserProfile.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


def update_user_name(user_id, new_name):
    """
    Updates the name of an existing user.
    Args:
        user_id (int): The ID of the user to update.
        new_name (str): The new name to assign to the user.
    Returns:
        bool: True if the update was successful, False otherwise.
    """
    user = UserProfile.query.get(user_id)
    if user:
        user.name = new_name
        db.session.commit()
        return True
    return False

