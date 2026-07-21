from assistant.core.controller import ApplicationController


def main() -> None:
    controller = ApplicationController()
    controller.run()


if __name__ == "__main__":
    main()