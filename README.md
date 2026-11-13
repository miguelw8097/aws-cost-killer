# AWS Cost Killer

Script de automatización serverless para optimizar costes de infraestructura en AWS. Detiene de forma automática las instancias EC2 de desarrollo que quedan encendidas fuera del horario laboral.

## Arquitectura

El proyecto utiliza una arquitectura basada en eventos (event-driven) compuesta por los siguientes servicios:

- **Amazon EventBridge** : Disparador programado (cron) que inicia la ejecución.
- **AWS Lambda**         : Entorno de ejecución de código (Python 3.15 + Boto3).
- **Amazon EC2**         : Instancias de cómputo objetivo.
- **AWS IAM**            : Gestión de accesos y seguridad.

## Lógica de ejecución

1. EventBridge invoca la función Lambda de lunes a viernes a las 19:00 (hora local).
2. El script de Python se autentica y conecta a la API de EC2 mediante el SDK Boto3.
3. Se filtran las instancias de la región que cumplen simultáneamente dos condiciones:
   - Estado: `running`
   - Etiqueta (Tag): `Entorno = Desarrollo`
4. Se envía la orden de apagado (`StopInstances`) exclusivamente a los recursos detectados.

## Despliegue

1. Crea una función en AWS Lambda utilizando el runtime de Python 3.12.
2. Sube el código del archivo `lambda_function.py`.
3. En la configuración general de Lambda, ajusta el Timeout a 15 segundos y la memoria a 256 MB para optimizar el tiempo de ejecución.
4. Crea una regla en Amazon EventBridge (tipo Schedule) con la siguiente expresión cron: `cron(0 19 ? * MON-FRI *)`.
5. Asigna la función Lambda como Target de la regla de EventBridge.

## Configuración de IAM (Mínimo Privilegio)

Por motivos de seguridad, la función no debe ejecutarse con privilegios de administrador. Asigna al rol de ejecución de Lambda la siguiente política JSON, que limita el alcance estrictamente a las acciones de lectura y apagado:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        }
    ]
}
