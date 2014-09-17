from django.db import IntegrityError
from pine.models import Users, Phones


def create_friendship(user, target_phone_number):
    # get or create target phone record
    target_phone_id = Phones.objects.filter(phone_number=target_phone_number)
    if target_phone_id.exists():
        target_phone = Phones.objects.get(phone_number=target_phone_number)
        if user.phone.id == target_phone.id:
            return
    else:
        target_phone = Phones.objects.create(phone_number=target_phone_number)

    # check for performance.
    # If does not need to compute it return
    if user.friend_phones.filter(id=target_phone.id).exists():
        return

    # todo: code is fuck. Need to research django source or report django community.
    # add target phone to friends phones
    try:
        user.friend_phones.add(target_phone)
    except IntegrityError as err:
        raise err

    # check for performance.
    # If target is no pine user it return
    target_user_query = Users.objects.filter(phone=target_phone.id)
    target_user = None

    if target_user_query.exists():
        target_user = target_user_query[0]
    else:
        return

    # configure friends, following
    has_user_target_phone = target_user.friend_phones.filter(id=user.phone.id).exists()
    if has_user_target_phone:
        user.friends.add(target_user)
    else:
        user.followings.add(target_user)