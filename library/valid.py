def isProperMail(email):
    return "@" in email


def isProperTelephone(telephone):
    return str(telephone).isnumeric() and len(str(telephone)) == 9
