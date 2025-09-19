
def get_user_role(request):
    if request.user.is_authenticated:
        user_role = request.user.role
        if user_role ==None:
            user_role='nan'
    else:
        user_role ='nan'
    return {'user_role':str(user_role)}