# ✈️ DBL Data Challenge Year One
## 🏖️ About
This is the public repository of our project for the course DBL Data Challenge of the program of Data Science of TU Eindhoven.
Here you can find the code used to store, organize, extract and analyze information from the given data. The goal is to gain insights in airline data. 

## ⚙️ Getting Started
1. Clone the repository on your machine using `git clone` command. Use `git pull` to fetch the latest updates.
2. In the root directory of the project rename `.env.example` to `.env`. This can be done by the bash command `mv .env.example .env`. Make sure you update the database credentials in `.env` with the correct credentials of the database engine on your machine. Try `nano .env` for this.
3. Make sure all of the dependencies of the projects are satisfied. Use `pip install -r requirements.txt` to install the dependencies.
4. Once in project's root directory, try `python main.py make:tables` in order to create the table used for storing tweets.
5. Use the `dataFiles` variable in `main.py` to configure the JSON files which their content needs to inserted to the database.
6. Once the `dataFiles` variable is properly set, run `python main.py insert:tweets` in order to append the tweets to the database.

## Next steps


1. Run the `word_clustering.ipynb` notebook to create the categories in the database.
2. All the graphs can be found in `FINAL VISUALISATIONS.ipynb` notebook.