import boto3
import csv
import mysql.connector

hostDB = "172.31.88.133"
portDB = 8005
userDB = "root"
passwordDB = "utec"
databaseDB = "bd_api_employees"

ficheroUpload = "data.csv"
nombreBucket = "brissethsurquislla"

print("Conectando a MySQL")

conexion = mysql.connector.connect(
    host=hostDB,
    port=portDB,
    user=userDB,
    password=passwordDB,
    database=databaseDB
)

cursor = conexion.cursor()

cursor.execute("SELECT * FROM employees")

registros = cursor.fetchall()
columnas = [columna[0] for columna in cursor.description]

print("Registros obtenidos:", len(registros))

with open(ficheroUpload, "w", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(columnas)
    writer.writerows(registros)

print("Archivo CSV generado correctamente")

cursor.close()
conexion.close()

print("Subiendo archivo a S3...")

s3 = boto3.client("s3")

response = s3.upload_file(
    ficheroUpload,
    nombreBucket,
    ficheroUpload
)

print(response)
print("Ingesta completada")
