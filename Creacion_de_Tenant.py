# libreriass necesarias para ejecutar el codigo
from credentials import *
from acitoolkit.acitoolkit import *

# Iniciando sesion en  el sandbox
session = Session(URL, LOGIN, PASSWORD)
session.login()

