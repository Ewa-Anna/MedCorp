from datetime import datetime


def isProperMail(email):
    return "@" in email


def isProperTelephone(telephone):
    return str(telephone).isnumeric() and len(str(telephone)) == 9


def calculate_age(birthdate):
    today = datetime.now()
    age = today.year - birthdate.year - \
        ((today.month, today.day) < (birthdate.month, birthdate.day))
    months = (today.month - birthdate.month) % 12
    return age, months
