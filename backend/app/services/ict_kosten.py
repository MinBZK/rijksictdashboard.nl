from enum import Enum
from typing import Literal, TypedDict, cast

import pandas as pd
from sqlalchemy import select

from app.database.database import engine
from app.models import Ministerie


class FieldNames(str, Enum):
    CATEGORIE = "categorie"
    KOSTENPOST = "kostenpost"
    KOSTEN = "kosten"
    MINISTERIE = "ministerie"
    MINISTERIE_AFKORTING = "ministerie_afkorting"


Stelsels = Literal["kas-verplichtingenstelsel", "baten-lastenstelsel"]


class IctKosten(TypedDict):
    kostenpost: str
    ministerie: str
    kostencategorie: str
    waarde: float


class IctKostenDefinition(TypedDict):
    file: str
    column_mapping: dict[str, FieldNames]


class ChartdataPoint:
    x: str
    y: str
    label: str


class IctKostenData(TypedDict):
    table_data: list[IctKosten]
    chart_data: list[ChartdataPoint]
    available_ministeries: list[str]


kosten_sources: dict[int, dict[Stelsels, IctKostenDefinition]] = {
    2021: {
        "kas-verplichtingenstelsel": {
            "file": "kas-verplichtingenstelsel-2021.xlsx",
            "column_mapping": {
                "2021": FieldNames.KOSTENPOST,
                "kas-verplichtingenstelsel": FieldNames.CATEGORIE,
            },
        },
        "baten-lastenstelsel": {
            "file": "baten-lastenstelsel-2021.xlsx",
            "column_mapping": {
                "baten-lastenstelsel": FieldNames.CATEGORIE,
                "2021": FieldNames.KOSTENPOST,
            },
        },
    },
    2022: {
        "kas-verplichtingenstelsel": {
            "file": "kas-verplichtingenstelsel-2022.xlsx",
            "column_mapping": {
                "2022": FieldNames.KOSTENPOST,
                "kas-verplichtingenstelsel": FieldNames.CATEGORIE,
            },
        },
        "baten-lastenstelsel": {
            "file": "baten-lastenstelsel-2022.xlsx",
            "column_mapping": {
                "baten-lastenstelsel": FieldNames.CATEGORIE,
                "2022": FieldNames.KOSTENPOST,
            },
        },
    },
    2023: {
        "kas-verplichtingenstelsel": {
            "file": "kas-verplichtingenstelsel-2023.xlsx",
            "column_mapping": {
                "2023": FieldNames.KOSTENPOST,
                "kas-verplichtingenstelsel": FieldNames.CATEGORIE,
            },
        },
        "baten-lastenstelsel": {
            "file": "baten-lastenstelsel-2023.xlsx",
            "column_mapping": {
                "baten-lastenstelsel": FieldNames.CATEGORIE,
                "2023": FieldNames.KOSTENPOST,
            },
        },
    },
}


def get_ict_kosten(
    stelsel: Stelsels, year: int, ministerie: str | None
) -> IctKostenData:
    file = kosten_sources.get(year, {}).get(stelsel, {}).get("file", None)
    column_mapping = (
        kosten_sources.get(year, {}).get(stelsel, {}).get("column_mapping", None)
    )

    df = pd.read_excel(f"app/assets/{file}").rename(columns=column_mapping)

    ministerie_df = pd.read_sql(sql=select(Ministerie), con=engine.connect()).rename(
        columns={
            "Naam": FieldNames.MINISTERIE.value,
            "Afkorting": FieldNames.MINISTERIE_AFKORTING.value,
        }
    )

    ministerie_afkortingen = list(df.columns)[2:]

    df_melted = (
        df.melt(
            value_vars=ministerie_afkortingen,
            id_vars=[FieldNames.KOSTENPOST.value, FieldNames.CATEGORIE.value],
            value_name=FieldNames.KOSTEN.value,
            var_name=FieldNames.MINISTERIE.value,
        )
        .rename(
            columns={FieldNames.MINISTERIE.value: FieldNames.MINISTERIE_AFKORTING.value}
        )
        .merge(
            ministerie_df[
                [FieldNames.MINISTERIE.value, FieldNames.MINISTERIE_AFKORTING.value]
            ],
            left_on=FieldNames.MINISTERIE_AFKORTING.value,
            right_on=FieldNames.MINISTERIE_AFKORTING.value,
        )
    )

    if ministerie:
        df_melted_and_filtered: pd.DataFrame = df_melted.loc[
            df_melted[FieldNames.MINISTERIE.value] == ministerie
        ]
    else:
        df_melted_and_filtered: pd.DataFrame = df_melted

    aggregation_columns = (
        [FieldNames.MINISTERIE_AFKORTING.value, FieldNames.CATEGORIE.value]
        if ministerie is None
        else [
            FieldNames.MINISTERIE.value,
            FieldNames.CATEGORIE.value,
            FieldNames.KOSTENPOST.value,
        ]
    )

    chart_mapping = (
        {
            FieldNames.MINISTERIE_AFKORTING.value: "x",
            FieldNames.KOSTEN.value: "y",
            FieldNames.CATEGORIE.value: "label",
        }
        if ministerie is None
        else {
            FieldNames.CATEGORIE.value: "x",
            FieldNames.KOSTEN.value: "y",
            FieldNames.KOSTENPOST.value: "label",
        }
    )

    chart_data = cast(
        list[ChartdataPoint],
        (
            df_melted_and_filtered.groupby(aggregation_columns)[FieldNames.KOSTEN.value]
            .sum()
            .reset_index()
            .rename(columns=chart_mapping)
            .to_dict(orient="records")
        ),
    )

    table_data = cast(list[IctKosten], df_melted_and_filtered.to_dict(orient="records"))

    return {
        "table_data": table_data,
        "chart_data": chart_data,
        "available_ministeries": list(df_melted[FieldNames.MINISTERIE].unique()),
    }
