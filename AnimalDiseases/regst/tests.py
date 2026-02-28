from django.test import TestCase
from .views import RegisterView

# Create your tests here.
register = RegisterView()

class PasswordValidatorTests(TestCase):
    def test_valid_password(self):
        passwords = ('erFEFkjEF_435', 'JuuihUuiewo.838', '+879JHui7769+')
        for p in passwords:
            self.assertEqual(register._pass_validation(p), True)


    def test_invalid_password(self):
        passwords = ('$Hell!!!#', '^%$#^&*^&*', '!@#$%^^%$#@!', '[!@#$%^&()~`<>?/{}')
        for p in passwords:
            self.assertEqual(register._pass_validation(p), False)


class UsernameTests(TestCase):
    def test_valid_username(self):
        names = ('Dendy_999', 'Alex765', 'wasdeqzxc')
        for name in names:
            self.assertEqual(register._username_validation(name), True)


    def test_invalid_username(self):
        names = ('!Dendy!', '+!Hell##enn!+', '+@!@+')
        for name in names:
            self.assertEqual(register._username_validation(name), False)



