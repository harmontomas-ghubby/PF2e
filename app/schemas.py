from pydantic import BaseModel, Field


class WeightedEntry(BaseModel):
    text: str
    weight: int = 1


class OracleTable(BaseModel):
    name: str
    entries: list[WeightedEntry] = Field(default_factory=list)


class OracleCategory(BaseModel):
    category: str
    tables: list[OracleTable] = Field(default_factory=list)
