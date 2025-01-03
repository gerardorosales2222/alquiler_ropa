# Alquiler de prendas

A continuación se explican los pasos necesarios para configurar el entorno y ejecutar este proyecto en tu PC.

## Requisitos previos

- Python 3.x
- pip
- virtualenv

## Configuración del entorno

1. Clona el repositorio:

    ```bash
    git clone https://github.com/gerardorosales2222/alquiler_ropa.git

    cd tu-repositorio
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

## Migraciones de la base de datos

Aplica las migraciones de la base de datos:

```bash
python manage.py migrate