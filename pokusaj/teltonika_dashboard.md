teltonika_dashboard/
│
├─ teltonika_client.py
├─ device_database.py
├─ teltonika_devices.db
│
├─ main.py
├─ templates/
│   └─ devices.html
└─ static/
    └─ styles.css
pip install fastapi uvicorn jinja2 python-multipart
pip install fastapi uvicorn requests jinja2
uvicorn main:app --reload