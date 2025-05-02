import os
import zipfile
from io import BytesIO

from app.controllers import ProjectCollection
from app.models import ProjectViewMetWaardes
from app.util.dfs_to_excel import dict_to_spreadsheet


def get_file_from_jbr(p: ProjectViewMetWaardes) -> tuple[BytesIO, str]:
    file_object = dict_to_spreadsheet(
        data_dict=p.calculated_attributes.toelichting,
        file_type="excel",
    )
    corrected_project_name = (
        f"{p.Naam[:40]}".replace("/", "_")
        .replace("&", "_")
        .replace(":", "_")
        .replace(".", "_")
    )

    filename = f"{corrected_project_name}.xlsx"
    return file_object, filename


def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_jbr_files(year: int):
    output_dir = "app/scripts/output"
    ensure_directory_exists(output_dir)

    zip_buffer = BytesIO()
    jbr = ProjectCollection(year=year)
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for p in jbr.projecten_filtered:
            file_object, filename = get_file_from_jbr(p)
            zip_file.writestr(filename, file_object.getvalue())

    with open(f"{output_dir}/jbr_toelichtingen_{year}.zip", "wb") as f:
        f.write(zip_buffer.getvalue())


if __name__ == "__main__":
    get_jbr_files(year=2023)
