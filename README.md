# cdslab_cmodels_api

cmodels API repo

## Setup

Make sure you have installed the required python version (see Pipfile)

1. Clone this repository

    ```bash
    $ git clone https://github.com/fenfisdi/cdslab_cmodels_api
    $ cd cdslab_cmodels_api
    ```

2. Install pipenv

    ```bash
    $ pip3 install pipenv
    ```

3. Create virtual environment, and install packages (including developer packages) within the environment

    ```bash
    $ pipenv install --dev
    ```

4. Start virtual environment session

    ```bash
    $ pipenv shell
    ```

    NOTE: if you want to close the session just execute ``$ exit``

5. Create your ``cdslab_cmodels_api/.env`` file with appropiate ``HOST`` and ``PORT`` variables defined.

6. Run the uvicorn server via the ``cdslab_cmodels_api/main.py`` file

    ```bash
    $ python main.py
    ```

7. Enjoy...
