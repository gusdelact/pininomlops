import boto3
import os


#cambiar las llaves de acceso y region
os.environ['AWS_ACCESS_KEY_ID']= 'XXXXX'
os.environ['AWS_SECRET_ACCESS_KEY']= 'XXXXX'
os.environ ['AWS_DEFAULT_REGION']=  'region'



#crear repositorio de imagen de contenedores - Elastic Container Registry
ecr_cliente = client = boto3.client('ecr')

client.create_repository(repositoryName='dummylinear')

#crear cluster de Elastic Container Service

ecs_cliente = boto3.client('ecs')

#crear defincion de Tarea
ecs_cliente.register_task_definition( 
     family='tskdummylinear2',
     cpu ='256',
     memory = '512',
     requiresCompatibilities= ['FARGATE'],
     runtimePlatform = {'cpuArchitecture': 'X86_64', 'operatingSystemFamily': 'LINUX'},
     networkMode = 'awsvpc' ,
     executionRoleArn = 'arn:aws:iam::740327929864:role/ecsTaskExecutionRole',
     containerDefinitions=[
         { 
            'name': 'dummylinear',
            'image': '740327929864.dkr.ecr.us-east-1.amazonaws.com/dummylinear',
            'portMappings': [{'containerPort': 5000, 'hostPort': 5000, 'protocol': 'tcp', 'name': 'dummylinear-5000-tcp',
                              'appProtocol': 'http'}] ,
         }
     ] ,
    
 )
 
#Crear servicio
ecs_cliente.create_service(cluster='dummylinear',
                           serviceName='svcdummylinear2',
                           taskDefinition='arn:aws:ecs:us-east-1:740327929864:task-definition/tskdummylinear:1',
                           launchType ='FARGATE',
                           desiredCount=1,
                           networkConfiguration= {
                               'awsvpcConfiguration': {
                                  'assignPublicIp' : 'ENABLED',
                                  'securityGroups': ['sg-08ec75aa8b8f7c45b'],
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
ecs_cliente.describe_task_definition( taskDefinition='tskdummylinear2') 

ecs_cliente.describe_services(cluster='dummylinear',services=["svcdummylinear"])