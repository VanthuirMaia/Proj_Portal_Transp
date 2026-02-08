from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'vanthuir',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'portal_transparencia_pipeline',
    default_args=default_args,
    description='Pipeline completo com containers isolados',
    schedule_interval='@weekly',
    start_date=datetime(2026, 2, 5),
    catchup=False,
    tags=['dados_publicos', 'docker'],
) as dag:

    ingestao = DockerOperator(
        task_id='ingestao_api',
        image='portal-transp-ingestion:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='D:/02-Projetos dados/Proj_Portal_Transp/data', target='/app/data', type='bind'),
        ],
    )

    transformacao = DockerOperator(
        task_id='transformacao_parquet',
        image='portal-transp-transformation:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='D:/02-Projetos dados/Proj_Portal_Transp/data', target='/app/data', type='bind'),
        ],
    )

    carga = DockerOperator(
        task_id='carga_duckdb',
        image='portal-transp-load:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='D:/02-Projetos dados/Proj_Portal_Transp/data', target='/app/data', type='bind'),
        ],
    )

    dbt_run = DockerOperator(
        task_id='dbt_run',
        image='portal-transp-dbt:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        mounts=[
            Mount(source='D:/02-Projetos dados/Proj_Portal_Transp/data', target='/app/data', type='bind'),
        ],
    )

    dbt_test = DockerOperator(
        task_id='dbt_test',
        image='portal-transp-dbt:latest',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        command='dbt test',
        mounts=[
            Mount(source='D:/02-Projetos dados/Proj_Portal_Transp/data', target='/app/data', type='bind'),
        ],
    )

    ingestao >> transformacao >> carga >> dbt_run >> dbt_test