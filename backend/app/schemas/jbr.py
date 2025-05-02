import datetime

from pydantic import BaseModel


class ProjectSamenvattingCore(BaseModel):
    ActiviteitId: str
    Ministerie: str
    Naam: str
    StartDatum: datetime.date | None
    MinisterieNaam: str
    DoorlooptijdActueel: float | None
    SchattingTotaleKostenHuidigJaar: float
    SchattingEinddatumActueel: datetime.date | None

    # The attributes below are added to this schema because of a mistake in the frontend.
    # The frontend uses this schena/type to define the available filters.
    # This is a mistake on the frontend side, but the easiest fix is to add it here.
    HeeftAcICTAdvies: str
    SoortICTActiviteit: str | None
    MaatschappelijkeBaat: str | None


class ProjectSamenvattingAttributen(BaseModel):
    ProjectStatus: str | None

    # Attributes
    HeeftAcICTAdvies: str
    Onderwerp: str | None
    Dienstverlening: str | None
    MaatschappelijkeBaat: str | None
    Ontwikkelwijze: str | None

    # Metrics
    SchattingEinddatumInitieel: datetime.date | None
    SchattingEinddatumActueel: datetime.date | None
    SchattingTotaleKostenInitieel: float | None
    SchattingTotaleKostenVorigJaar: float | None
    OverigeKostenDaadwerkelijk: float | None
    InternPersoneelDaadwerkelijk: float | None
    ExternPersoneelDaadwerkelijk: float | None
    UitbesteedWerkDaadwerkelijk: float | None
    InbesteedWerkDaadwerkelijk: float | None
    DataverbindingenDaadwerkelijk: float | None
    StandaardsoftwareDaadwerkelijk: float | None
    HardwareDaadwerkelijk: float | None
    HardwareSoftwareDaadwerkelijk: float | None
    OverigMaterieelDaadwerkelijk: float | None
    OverigeKostenActueel: float | None
    InternPersoneelActueel: float | None
    ExternPersoneelActueel: float | None
    UitbesteedWerkActueel: float | None
    InbesteedWerkActueel: float | None
    DataverbindingenActueel: float | None
    StandaardsoftwareActueel: float | None
    HardwareActueel: float | None
    HardwareSoftwareActueel: float | None
    OverigMaterieelActueel: float | None

    OverigeKostenInitieel: float | None
    InternPersoneelInitieel: float | None
    ExternPersoneelInitieel: float | None
    UitbesteedWerkInitieel: float | None
    InbesteedWerkInitieel: float | None
    DataverbindingenInitieel: float | None
    StandaardsoftwareInitieel: float | None
    HardwareInitieel: float | None
    HardwareSoftwareInitieel: float | None
    OverigMaterieelInitieel: float | None

    CumulatieveKostenHuidigJaar: float | None
    CumulatieveKostenVorigJaar: float | None
    PrognoseToekomstigeKosten: float
    ActiefInJbrJaar: bool
    SoortICTActiviteit: str | None
    RedenenHerijkingen: str
    AantalBaten: int
    Ontwikkelpartijen: str
    AantalBehaaldeMijlpalen: int
    StartJaar: int | None
    EindJaar: int | None
    AantalAcICTAdviezen: int

    VerschilEindatumInitieelActueelInJaren: float | None
    DoorlooptijdInitieel: float | None
    VerschilDoorlooptijdPct: float


class ProjectSamenvattingJBR(ProjectSamenvattingAttributen, ProjectSamenvattingCore):
    pass


class ProjectToelichtingenJBR(BaseModel):
    Naam: str
    Peildatum: datetime.date | None
    Ministerie: str
    Projectstatus: str
    Ontwikkelmethode: str
    Aanleiding: str
    KostenEnUitgaven: list[dict]
    Doorlooptijd: dict
    Ontwikkelpartijen: list[dict]
    Herijkingen: list[dict]
    Mijlpalen: list[dict]
    Kwaliteitstoetsen: list[dict]
    TweedeKamerStukken: list[dict]


class ProjectJBR(BaseModel):
    project_summary_jbr: ProjectSamenvattingJBR
    jbr_jaar: int
    toelichtingen: ProjectToelichtingenJBR
