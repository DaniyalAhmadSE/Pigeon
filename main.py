from cli import Cli
from core.api import Api


def main():
    cli = Cli(Api())
    cli.run()


if __name__ == "__main__":
    main()
