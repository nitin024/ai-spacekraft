from pydantic import BaseModel

class Place(BaseModel):
    name: str
    rating: float
    distance: float
    type: str
    score: float = 0.0