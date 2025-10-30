from argparse import ArgumentParser

from models.user import UserModel
from schemas.user import UserRegisterSchema


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-e", "--email", type=str, required=True, help="Email address of the user"
    )
    parser.add_argument(
        "-p", "--password", type=str, required=True, help="Password of the user"
    )
    parser.add_argument(
        "--phone", type=str, required=True, help="Phone number of the user"
    )
    parser.add_argument(
        "--is_admin", type=bool, action="store_true", help="User is admin or not"
    )

    return parser.parse_args()


def main():
    args = get_args()
    user_register = UserRegisterSchema(
        email=args.email,
        password=args.password,
        phone=args.phone,
    )
    user = UserModel(**user_register.model_dump(exclude=["password"]))
    user.set_password(user_register.password.get_secret_value())
    if args.is_admin:
        user.is_admin = True
    is_ok, errors = user.create()
    assert is_ok, errors


if __name__ == "__main__":
    main()
