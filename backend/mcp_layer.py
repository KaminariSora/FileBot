import os
# import datetime
from pathlib import Path

def search_files(context, path: str):
    search_dir = Path(path)
    file_type = context.get("type")
    filename = context.get("filename")

    print(f"[DEBUG] Searching with - filename: '{filename}', type: '{file_type}'")
    
    results = []

    for file_path in search_dir.rglob("*"):
        if not file_path.is_file():
            continue

        # Filter by file type
        if file_type and not file_path.name.lower().endswith(file_type.lower()):
            continue

        # Filter by filename (partial match) - ถ้าไม่มี filename ก็ไม่ต้องกรอง
        if filename and filename.lower() not in file_path.name.lower():
            continue

        results.append({
            "name": file_path.name,
            "path": str(file_path),
        })
    
    print(f"[DEBUG] Found {len(results)} files")
    return results


def open_file(filepath: str):
    """เปิดไฟล์ด้วย application เริ่มต้น"""
    try:
        file_path = Path(filepath)
        if not file_path.exists():
            raise FileNotFoundError(f"ไม่พบไฟล์: {filepath}")
        
        # Windows
        if os.name == 'nt':
            os.startfile(filepath)
        # macOS
        elif os.name == 'posix' and os.uname().sysname == 'Darwin':
            os.system(f'open "{filepath}"')
        # Linux
        else:
            os.system(f'xdg-open "{filepath}"')
            
        return {"success": True, "message": f"เปิดไฟล์ {file_path.name} เรียบร้อยแล้ว"}
    except Exception as e:
        return {"success": False, "message": f"เกิดข้อผิดพลาด: {str(e)}"}