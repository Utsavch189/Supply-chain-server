from django.core.mail import send_mail

def otp_mail(email,name,otp):
    subject=f'U-HUB OTP verification'
    body=f'{name} Your Reset Password OTP is {otp}'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)


def middle_otp_mail(email,otp):
    subject=f'U-HUB OTP verification'
    body=f'Your Verification OTP is {otp}'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def passwordUpdate_mail(email,name):
    subject='U-HUB Reset Password'
    body=f'{name} Your Password is successfully updated'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)


def approve_mail(email,name):
    subject='U-HUB Approval'
    body=f'{name} Your request is successfully approved, now you can login with your registered email and password'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def removeUser_mail(email,name):   
    subject='U-HUB Removal'
    body=f'{name} Sorry! You are removed from U-HUB'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)

def Reapprove_mail(email,name):
    subject='U-HUB Reapproval'
    body=f'{name} Your are ReApproved, now you can login with your registered email and password'
    mail_sender = 'utsavpokemon9000chatterjee@gmail.com'
    send_mail(subject, body, mail_sender, [email], fail_silently=False)