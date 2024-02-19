from django.contrib.auth.models import User
from saswat_cust_app.models import UserOtp, UserDetails
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import secrets
import string

def generate_session_id():
    # Generate a random string of alphanumeric characters
    alphabet = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(alphabet) for i in range(32))
    return session_id

class MobileNumberAuthentication(BaseAuthentication):
    def authenticate(self, request):
        mobile_no = request.data.get('mobile_no')

        if mobile_no:
            # Find user by mobile number
            try:
                user = UserDetails.objects.get(mobile_no=mobile_no)
                # Generate session ID (you can use any method to generate a unique ID)
                session_id = generate_session_id()
                return (user, session_id)
            except UserDetails.DoesNotExist:
                raise AuthenticationFailed('User not found')
        else:
            return None

    def authenticate_header(self, request):
        return 'Session'
