from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    drop_table: bool = True
