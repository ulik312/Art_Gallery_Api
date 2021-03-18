from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}/'
    message = f"""
        Thank you for signing up.
        Please, activate your account. 
        Activation link: {activation_url}     
    """
    send_mail(
        'Activate your account',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )


@shared_task
def send_activation_codee(email, activation_code):
    activation_url = f'{activation_code}'
    message = f"""

        Your code: {activation_url}
"""
    send_mail(
        'Forgot Password',
        message,
        'test@test.com',
        [email, ],
        fail_silently=False
    )
