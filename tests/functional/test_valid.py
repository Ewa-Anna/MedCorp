from library.valid import isProperMail, isProperTelephone

def test_isProperMail():
    valid_email = "test@example.com"
    invalid_email1 = "testexample.com"
    invalid_email2 = "testtest"
    assert isProperMail(valid_email) is True
    assert isProperMail(invalid_email1) is False
    assert isProperMail(invalid_email2) is False


def test_isProperTelephone():
    valid_phone = 123456789
    invalid_phone1 = "abc" # not numeric
    invalid_phone2 = 1234567 # too short
    assert isProperTelephone(valid_phone) is True
    assert isProperTelephone(invalid_phone1) is False
    assert isProperTelephone(invalid_phone2) is False