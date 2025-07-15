import os
# import datetime
from pathlib import Path

def search_files(context):
    search_dir = Path(r"D:\\Working\\C_work\\Coding\\FileBot\\TestData")
    file_type = context.get("type")
    # modified_within_days = context.get("modified_within_days") or 7  # ป้องกัน None

    results = []
    # now = datetime.datetime.now()

    for path in search_dir.rglob("*"):
        if not path.is_file():
            continue

        if file_type and not path.name.endswith(file_type):
            continue

        # modified_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        # if (now - modified_time).days > modified_within_days:
        #     continue

        results.append({
            "name": path.name,
            "path": str(path),
            # "modified": modified_time.strftime("%Y-%m-%d %H:%M"),
        })

    return results


def open_file(filepath: str):
    try:
        os.startfile(filepath)  # Windows only
    except Exception as e:
        print(f"Error opening file: {e}")
