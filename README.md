# Alquiler de prendas

A continuación se explican los pasos necesarios para configurar el entorno y ejecutar este proyecto en tu PC.

## Requisitos previos

- [Python 3.12.8](https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe)
- pip
- virtualenv

## Configuración del entorno

1. Clona el repositorio:

    ```bash
    git clone https://github.com/gerardorosales2222/alquiler_ropa.git

    cd alquiler_ropa
    ```

2. Crea un entorno virtual:

    ```bash
    python -m venv venv
    ```

3. Activa el entorno virtual:

    - En Windows:

    ```bash
    venv\Scripts\activate
    ```

    - En macOS y Linux:

    ```bash
    source venv/bin/activate
    ```

4. Instala las dependencias:

    ```bash
    pip install -r requirements.txt
    ```
    

> ### A tener en cuenta para el futuro: 
> Cada vez que añadas o actualices una dependencia en tu entorno virtual, puedes ejecutar:
>```bash
>pip freeze > requirements.txt 
>```
>Esto sirve para actualizar el archivo requirements.txt con la lista completa y actualizada de las dependencias del proyecto.
Actualizar el requirements.txt después de instalar o actualizar paquetes, para asegurarte de que el archivo siempre refleje el estado actual del entorno.

## Migraciones de la base de datos

Aplica las migraciones de la base de datos:

```bash
python manage.py migrate
