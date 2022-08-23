# libreriass necesarias para ejecutar el codigo
from credentials import *
from acitoolkit.acitoolkit import *

# Iniciando sesion en  el sandbox
session = Session(URL, LOGIN, PASSWORD)
session.login()

#codigo necesario para la creacion de tenant y VRF
tenant_name = "Tenant_de_telefonica"
tenant = Tenant(tenant_name)
vrf = Context("Example_VRF", tenant)

# relacion dominio de bridge y VRF
bridge_domain = BridgeDomain("Example_BD", tenant)
bridge_domain.add_context(vrf)

