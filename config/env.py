from dotenv import load_dotenv, dotenv_values


def checkAccess():
    return load_dotenv('../.env')


def getConfig(key):
    if (not load_dotenv('.env')):
        quit(
            "Error in reading the environment file. Make sure you've renamed .env.example to .env and changed the configuration values properly.")
    return dotenv_values('.env')[key]
