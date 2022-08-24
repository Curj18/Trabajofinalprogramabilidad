# libreriass necesarias para ejecutar el codigo
from credentials import *
from acitoolkit.acitoolkit import *

# Iniciando sesion en  el sandbox
from credentials import URL, LOGIN, PASSWORD

session = Session(URL, LOGIN, PASSWORD)
session.login()

#codigo necesario para la creacion de tenant y VRF
tenant_name = "Tenant_de_telefonica"
tenant = Tenant(tenant_name)
vrf = Context("Example_VRF", tenant)

# relacion dominio de bridge y VRF
bridge_domain = BridgeDomain("Example_BD", tenant)
bridge_domain.add_context(vrf)

# creacion de subnet publica y asignar gateway
subnet = Subnet("Example_Subnet", bridge_domain)
subnet.set_scope("public")
subnet.set_addr("192.168.0.1/24")

# filtrado HTTP y entry
filter_http = Filter("http", tenant)
filter_entry_tcp80 = FilterEntry("tcp-80", filter_http, etherT="ip", prot="tcp", dFromPort="http", dToPort="http")

# filtrado SQL y entry
filter_sql = Filter("sql", tenant)
filter_entry_tcp1433 = FilterEntry("tcp-1433", filter_sql, etherT="ip", prot="tcp", dFromPort="1433", dToPort="1433")

# "contrato" web asociado a HTTP
contract_web = Contract("web", tenant)
contract_subject_http = ContractSubject("http", contract_web)
contract_subject_http.add_filter(filter_http)

# "contrato" database asociado a SQl
contract_database = Contract("database", tenant)
contract_subject_sql = ContractSubject("sql", contract_database)
contract_subject_sql.add_filter(filter_sql)

# perfil app
app_profile = AppProfile("Example_App", tenant)

#web epg y asociarla a bridge domain y contratos
epg_web = EPG("Web", app_profile)
epg_web.add_bd(bridge_domain)
epg_web.provide(contract_web)
epg_web.consume(contract_database)

# creando database epg and asociarla a bridge domain and "contratos"
epg_database = EPG("Database", app_profile)
epg_database.add_bd(bridge_domain)
epg_database.provide(contract_database)

# lista de tenants solo si es necesario
tenant_list = Tenant.get(session)

#mostrar lista de todos los tenant solo si es necesario
tenant_list
for tn in tenant_list:
    print(tn.name)

# imprimir url y configuracion en json
print("\n{}\n\n{}".format(tenant.get_url(), tenant.get_json()))

# print configuracion en json
import json
print(json.dumps(tenant.get_json(), sort_keys=True, indent=2, separators=(',',':')))

# push configuracion a la apic
resp = session.push_to_apic(tenant.get_url(), data=tenant.get_json())

# test solicitud de configuracion solo si hay equivocaciones
if resp.ok:
     print("\n{}: {}\n\n{} is ready for use".format(resp.status_code, resp.reason, tenant.name))
else:
     print("\n{}: {}\n\n{} was not created!\n\n Error: {}".format(resp.status_code, resp.reason, subnet.name, resp.content))

# re-revision ala tenant list
new_tenant_list = Tenant.get(session)
for tn in new_tenant_list:
    print(tn.name)

#chekear la app list en el nuevo tenant
app_list = AppProfile.get(session, tenant)
for app in app_list:
    print(app.name)

# chekear la lista epg en la nueva app
epg_list = EPG.get(session, app_profile, tenant)
for epg in epg_list:
    print(epg.name)

# salir del print
exit()