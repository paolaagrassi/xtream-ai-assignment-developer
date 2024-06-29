from pydantic import BaseModel


def validate_data_has_no_zero_values(data: BaseModel) -> None:
    for value in data:
        if 0 in value:
            raise ValueError(f"{value[0]} must have value grather than 0.")