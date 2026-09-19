from pydantic import BaseModel


class DashaPeriodOut(BaseModel):
    planet: str
    start: str
    end: str


class AntardashaOut(DashaPeriodOut):
    pass


class MahadashaOut(DashaPeriodOut):
    antardashas: list[AntardashaOut]


class DashaResponse(BaseModel):
    mahadasha_sequence: list[MahadashaOut]
    current_mahadasha: DashaPeriodOut | None
    current_antardasha: DashaPeriodOut | None
    current_pratyantardasha: DashaPeriodOut | None
    current_pratyantardasha_sequence: list[DashaPeriodOut]
