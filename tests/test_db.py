from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
        new_user = User(
            username='Paulo',
            email='paulo.arruda@masterboi.com',
            password='senha123',
        )
        session.add(new_user)
        session.commit()

        result = session.scalar(
            select(User).where(User.email == 'paulo.arruda@masterboi.com')
        )

        assert result.username == 'Paulo'
