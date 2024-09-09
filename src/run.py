
from src.utils.path_setups import path_setups


def run():
    path_setups()
    from main import main
    main()


if __name__ == '__main__':
    run()
