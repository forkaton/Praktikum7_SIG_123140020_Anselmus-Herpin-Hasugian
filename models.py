from pydantic import BaseModel

class FasilitasBase(BaseModel):
    nama: str
    longitude: float
    latitude: float

class FasilitasCreate(FasilitasBase):
    pass