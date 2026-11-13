import boto3

def lambda_handler(event, context):
#Inicio el cliente de ec2 para comunicarme con el servicio
    ec2 = boto3.client('ec2')

#Definir filtros: buscar etiqueta 'Entorno=Desarrollo' y estado 'running'
    filtros = [
        {
            'Name': 'tag:Entorno',
            'Values': ['Desarrollo']
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }
    ]
#Ejecutar la busqueda aplicando los filtros y crear una lista vacia para guardar los IDs de las maquinas
    respuesta = ec2.describe_instances(Filters=filtros)
    instancias_a_apagar = []

#Extraer los ID de las maquinas de la respuesta
    for reserva in respuesta['Reservations']:
        for instancia in reserva['Instances']:
            instancias_a_apagar.append(instancia['InstanceId'])
            
#Si la lista tiene máquinas, apagarlas. Si no, solo avisar de que no hay nada que hacer
    if instancias_a_apagar:
        print(f"Detectadas instancias para apagar: {instancias_a_apagar}")
        ec2.stop_instances(InstanceIds=instancias_a_apagar)
        return f"Completado: Se han mandado apagar {len(instancias_a_apagar)} instancias."
    else:
        print("No hay ninguna maquina de Desarrollo encendida en este momento.")
        return "No se han tomado acciones."