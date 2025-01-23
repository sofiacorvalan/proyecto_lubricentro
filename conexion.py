import mysql.connector 

class CConexion: 

   def ConexionBaseDeDatos():
      try:
         conexion = mysql.connector.connect(user='root',
                                            password='SOFIApaola1997',
                                            host='127.0.0.1',
                                            database='lubricentrodb',
                                            port='3306')
         print("Conexión correcta.")
         return conexion
      except mysql.connector.Error as error:
         print("Error al conectarte a la Base de Datos {}".format(error)) 
         return conexion

   ConexionBaseDeDatos()