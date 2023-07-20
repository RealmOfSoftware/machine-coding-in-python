class InvalidBill(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AlreadyExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DoesNotExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
