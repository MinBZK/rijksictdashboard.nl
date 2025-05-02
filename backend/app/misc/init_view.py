import os

from sqlalchemy import text

from app.middleware import get_db

views = [
    {"view_name": "vProjectAgg", "file": "v_project_agg.sql"},
    {"view_name": "vProjectIndicator", "file": "v_project_indicator.sql"},
]


def init_view():
    for v in views:
        view_name = v["view_name"]
        dump_filepath = os.path.abspath(f"app/queries/{v['file']}")
        with open(dump_filepath) as f:
            query = f.read()
            create_view_query = f"""create view "{view_name}" as ({query})"""
            drop_view_query = f"""
                drop view if exists "{view_name}"
            """
            db = next(get_db())
            db.execute(text(drop_view_query))
            db.execute(text(create_view_query))
            db.commit()


if __name__ == "__main__":
    init_view()
