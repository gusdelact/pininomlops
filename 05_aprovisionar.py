import boto3
import os
import time


print(os.environ)
#crear repositorio de imagen de contenedores - Elastic Container Registry

print("Creando Registro de Imagen del contenedor")
ecr_cliente = client = boto3.client('ecr')

client.create_repository(repositoryName=os.environ['ECR_REPO_NAME'])

#esperar 30 segundos

#crear cluster de Elastic Container Service

ecs_cliente = boto3.client('ecs')

#crear defincion de Tarea
print("Creando Definicion de Tarea de ECS")

task_name = 'task{}'.format(os.environ['ECR_REPO_NAME'])
ecs_cliente.register_task_definition( 
     family=task_name,
     cpu ='256',
     memory = '512',
     requiresCompatibilities= ['FARGATE'],
     runtimePlatform = {'cpuArchitecture': 'X86_64', 'operatingSystemFamily': 'LINUX'},
     networkMode = 'awsvpc' ,
     executionRoleArn = 'arn:aws:iam::{}:role/ecsTaskExecutionRole'.format(os.environ['ACCOUNT_NUMBER']),
     containerDefinitions=[
         { 
            'name': 'dummylinear',
            'image': '{}.dkr.ecr.{}.amazonaws.com/{}'.format(os.environ['ACCOUNT_NUMBER'],os.environ ['AWS_DEFAULT_REGION'],os.environ['ECR_REPO_NAME']) ,
            'portMappings': [{'containerPort': 5000, 'hostPort': 5000, 'protocol': 'tcp', 'name': 'dummylinear-5000-tcp',
                              'appProtocol': 'http'}] ,
         }
     ] ,
    
 )
 
#esperar 30 segundos
time.sleep(30)
#Crear servicio
print("Creando Servicio de ECS")
service_name = os.environ['SERVICE_NAME']
ecs_cliente.create_service(cluster='dummylinear',
                           serviceName=service_name,
                           taskDefinition='arn:aws:ecs:{}:{}:task-definition/{}:1'.format(os.environ ['AWS_DEFAULT_REGION'],os.environ['ACCOUNT_NUMBER'],task_name),
                           launchType ='FARGATE',
                           desiredCount=1,
                           networkConfiguration= {
                               'awsvpcConfiguration': {
                                  'assignPublicIp' : 'ENABLED',
                                  'securityGroups': ['sg-025066ab05b7439d2'],
                                  'subnets': ['subnet-0d5bef679df57ba9e',
                                               'subnet-02efe5c7251ec5212',
                                               'subnet-02acd8f884e171a3c',
                                               'subnet-08c84ad9ae30a370d',
                                               'subnet-0615686222a56563b',
                                               'subnet-01c5e49442af85ab1'],
                                }   
                            }
                          )
                          

#mostrar definciones de tare y servicios en JSON
#ecs_cliente.describe_task_definition( taskDefinition='tskdummylinear2') 

#ecs_cliente.describe_services(cluster='dummylinear',services=["svcdummylinear"])