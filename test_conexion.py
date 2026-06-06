"""
Script de prueba de conexión con Aiven MySQL.
Ejecutar: poetry run python test_conexion.py
"""
import os
import sys
from dotenv import load_dotenv
import pymysql

load_dotenv()

PASS = os.getenv("AIVEN_PASSWORD", "")
HOST = os.getenv("AIVEN_HOST", "xpmovies-db-elvinarmando-45ad.l.aivencloud.com")
PORT = int(os.getenv("AIVEN_PORT", "25616"))
USER = os.getenv("AIVEN_USER", "avnadmin")
DB   = os.getenv("AIVEN_DATABASE", "defaultdb")

print(f"Host:     {HOST}:{PORT}")
print(f"User:     {USER}")
print(f"Database: {DB}")
print(f"Host:     {HOST}:{PORT}")
print(f"User:     {USER}")
print(f"Database: {DB}")
print(f"Password: {'OK - cargada' if PASS else 'ERROR - VACIA, revisa el archivo .env'}")

if not PASS:
    print("\nERROR: La contrasena no se cargo desde .env")
    sys.exit(1)

print("\nConectando a Aiven...")
try:
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASS,
        database=DB,
        ssl={"ssl_disabled": False},
        connect_timeout=15,
    )
    cur = conn.cursor()

    # Prueba basica
    cur.execute("SELECT 1")
    print(f"SELECT 1: {cur.fetchone()}")

    # Ver version de MySQL
    cur.execute("SELECT VERSION()")
    version = cur.fetchone()
    print(f"MySQL version: {version[0]}")

    # Ver tablas existentes
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    if tables:
        print(f"Tablas en '{DB}': {[t[0] for t in tables]}")
    else:
        print(f"La base de datos '{DB}' esta vacia (sin tablas aun).")

    conn.close()
    print("\n[OK] CONEXION EXITOSA CON AIVEN MYSQL")

except pymysql.err.OperationalError as e:
    print(f"\n❌ Error de conexión: {e}")
    print("Verifica que el host, puerto y contraseña sean correctos.")
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error inesperado: {type(e).__name__}: {e}")
    sys.exit(1)
