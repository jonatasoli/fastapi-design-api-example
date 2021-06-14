import enum


class GLOBAL_ERRORS(enum.Enum):
    GE001 = "Unexpected Error"

    def __str__(self) -> str:
        return self.name
