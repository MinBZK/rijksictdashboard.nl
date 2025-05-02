import app.services as services
from app.services.ict_kosten import kosten_sources


def get_years() -> list[int]:
    return list(kosten_sources.keys())


def get_ict_kosten(ministerie: str | None):
    years = get_years()
    result = {}

    for year in years:
        kv_data = services.get_ict_kosten(
            stelsel="kas-verplichtingenstelsel", year=year, ministerie=ministerie
        )
        bl_data = services.get_ict_kosten(
            stelsel="baten-lastenstelsel", year=year, ministerie=ministerie
        )

        ministeries = list(
            set(kv_data["available_ministeries"] + bl_data["available_ministeries"])
        )

        ministeries.sort()

        result[year] = {
            "graph_data_kv": kv_data["chart_data"],
            "kosten_kasverplichtingenstelsel": kv_data["table_data"],
            "graph_data_bl": bl_data["chart_data"],
            "kosten_batenlastenstelsel": bl_data["table_data"],
            "available_ministeries": ministeries,
        }

    return result
