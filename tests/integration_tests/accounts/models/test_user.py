from pytest import mark

from raiseexception.accounts.models import User
from tests.factories import UserFactory

password_params = (
    ('test password', 'O2dmIBHo97eOO72wy0appi/JPQhxmew+hGJHlYv0ic4='),
    (
        # OWASP ASVS V2.1
        ')?,R)@RW?A!DT-cpS?Ft_#[vib-fEN*zHMJEnUq_)Lz#tgFL7:KT{[D6u&B*#_dR',
        '0hzC83Pm062omy8dF9Uhn1kbtkALdvNriy6rRXB7rQI='
    ),
    ('salt$passwor1', 'GkjXFa5m4ENJ2ZY+/u+06wLjRxE5gEwxkmkenVP5qzE='),
    ('unknown$salt$passwor1', 'SMjga2wEIe2EQqMRBJjDH1duG3g+p3cJiBuU6mbRik4='),

)


@mark.parametrize('password, hashed_password', password_params)
@mark.asyncio
async def test_create_user(password, hashed_password, db_connection, mocker):
    random_mock = mocker.patch('raiseexception.utils.crypto.get_random_string')
    salt = 'HjIQUM3X9KUAnlmGxDKGjdzGy8wPrFsK'
    random_mock.return_value = salt
    user = await UserFactory.create(password=password)
    user_fetched = await User.get(username=user.username)

    assert user_fetched.username == user.username
    assert user_fetched.email == user.email
    assert user_fetched.password == f'{salt}${hashed_password}'


@mark.asyncio
async def test_compare_just_created_user(db_connection, mocker):
    random_mock = mocker.patch('raiseexception.utils.crypto.get_random_string')
    salt = 'HjIQUM3X9KUAnlmGxDKGjdzGy8wPrFsK'
    random_mock.return_value = salt
    user = await UserFactory.create()
    hashed_password = 'O2dmIBHo97eOO72wy0appi/JPQhxmew+hGJHlYv0ic4='

    assert user.password == f'{salt}${hashed_password}'
