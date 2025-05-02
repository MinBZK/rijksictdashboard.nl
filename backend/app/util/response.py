import io
from pathlib import Path

import pandas as pd
from fastapi.responses import StreamingResponse


def df_as_excel_to_stream(df: pd.DataFrame, filename: str):
    stream = io.BytesIO()
    df.to_excel(stream, index=False, engine="openpyxl")  # type: ignore
    return get_file_stream_response(stream, filename=filename)


def get_file_stream_response(stream: io.BytesIO, filename: str):
    extension = Path(filename).suffix

    content_type_mapping = {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".ods": "application/vnd.oasis.opendocument.spreadsheet",
    }

    content_type = content_type_mapping.get(extension, None)
    if content_type is None:
        raise NotImplementedError(f"No content-type defined for {extension}")

    response = StreamingResponse(iter([stream.getvalue()]))
    response.headers["Content-Encoding"] = "UTF-8"
    response.headers["Content-type"] = f"{content_type}; charset=UTF-8"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response
