from assistant.core.controller import ApplicationController


def main() -> None:
    app = ApplicationController()

    app.start()

    # Future modules will run here.

    app.stop()


if __name__ == "__main__":
    main()