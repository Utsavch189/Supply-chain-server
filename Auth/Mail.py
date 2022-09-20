from django.core.mail import send_mail

def otp_mail(email,name,otp):
    subject=f'OTP verification'
    body=f'{name} Your Reset Password OTP is {otp}'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def passwordUpdate_mail(email,name):
    subject='Successful!'
    body=f'{name} Your Password is successfully updated'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)


def approve_mail(email,name):
    subject='Approved by Admin'
    body=f'{name} Your request is successfully approved, now you can login with your registered email and password'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def removeUser_mail(email,name):
    subject='Removed by Admin'
    body=f'{name} Sorry! You are removed from E-app'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def Reapprove_mail(email,name):
    subject='ReApproved by Admin'
    body=f'{name} Your are ReApproved, now you can login with your registered email and password'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)