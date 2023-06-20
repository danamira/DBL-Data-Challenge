from config.env import checkAccess



if not checkAccess():
    quit("Error in reading the environment file. Make sure you've renamed .env.example to .env and changed the configuration values properly.")



print("All works fine!")

