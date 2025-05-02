import pandas as pd

from app.controllers.ministerie import get_many
from app.schemas.kwiv import ChartdataPoint, KWIVData
from app.types.misc import KwivJaar


def get_ministeries():
    ministeries = get_many()
    return ministeries


async def get_kwiv_data(ministerie: str | None, jaar: KwivJaar, category: str | None):
    # Read KWIV data
    file_name = "kwiv_data_transformed.csv"
    df: pd.DataFrame = pd.read_csv(f"app/assets/{file_name}", dtype={"Categorie": str})

    df = df.loc[df["Jaar"] == jaar.value]

    categorie_mapping = {
        "1.1": "1.1 Architectuur",
        "1.2": "1.2 Informatieplanning",
        "1.3": "1.3 Sourcing management",
        "2.1": "2.1 Ontwikkelen",
        "2.2": "2.2 Testen",
        "3.1": "3.1 Onderhoud",
        "3.2": "3.2 Support",
        "3.3": "3.3 Service delivery",
        "4.1": "4.1 Informatiebeveiliging",
        "4.2": "4.2 Leveranciersmanagement",
        "4.3": "4.3 Informatieanalyse",
        "4.4": "4.4 Informatie educatie",
        "4.5": "4.5 Agile (SAFe) eigenaars",
        "5.1": "5.1 Project-, programma- en portfoliomanagement",
        "5.2": "5.2 Agile (SAFe) facilitators",
        "5.3": "5.3 Informatiestrategie",
        "5.4": "5.4 Control",
    }
    df["Categorie label"] = df["Categorie"].apply(
        lambda x: (
            categorie_mapping.get(x, "Categorie onbekend")
            if pd.notna(x)
            else "Categorie onbekend"
        )
    )

    # Replace incorrect spelled ministeries in the df
    mapping = {"J&V": "JENV", "I&W": "IENW", "EZK": "EZK/LNV"}
    df["Ministerie"] = df["Ministerie"].replace(mapping)

    # Create unique list of ministeries in de df and check if they are valid ministeries
    available_ministeries: list[str] = list(df["Ministerie"].unique().astype(str))
    available_categories: list[str] = list(df["Categorie label"].unique().astype(str))

    if category is not None:
        df = df.loc[df["Categorie label"] == category]

    if ministerie:
        df = df.loc[df["Ministerie"] == ministerie]
    else:
        df = df.groupby(["Ministerie", "Soort"])["Waarde"].sum().reset_index()

    kwiv_datapoints = df.to_dict(orient="records")

    chartdatapoints = [
        ChartdataPoint(
            x=row["Categorie label"] if ministerie else row["Ministerie"],
            y=round(row["Waarde"]),
            label=row["Soort"],
        )
        for row in kwiv_datapoints
    ]

    return KWIVData(
        datapoints=chartdatapoints,
        available_ministeries=available_ministeries,
        available_categories=available_categories,
    )
