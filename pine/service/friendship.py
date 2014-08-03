from pine.models import Users, Phones


def create_friendship(user, target_phone_number):
    print(1)
    # get or create target phone record
    target_phone_id = Phones.objects.filter(phone_number=target_phone_number)
    target_phone = None
    if target_phone_id.exists():
        target_phone = Phones.objects.get(phone_number=target_phone_number)
    else:
        target_phone = Phones.objects.create(phone_number=target_phone_number)
    print(2)
    # check for performance.
    # If does not need to compute it return
    if user.friend_phones.filter(phone_number=target_phone_number).exists():
        return
    print(3)
    # add target phone to friends phones
    user.friend_phones.add(target_phone)

    # check for performance.
    # If target is no pine user it return
    target_user_query = Users.objects.filter(phone=target_phone)
    target_user = None
    if target_user_query.exists():
        target_user = target_user_query[0]
    else:
        return
    print(4)
    # configure friends, following
    has_user_target_phone = target_user.friend_phones.filter(id=user.id).exists()
    if has_user_target_phone:
        user.friends.add(target_user)
    else:
        user.followings.add(target_user)