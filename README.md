# Fitness App - Back End

This is the repository for the back end of the Fitness app. See https://martijnroo.github.io/fitness-back-end/ for information on how to use this API.


## Installing the backend locally for development

The Backend uses Python 2.7.x and Flask for providing the API to store data to a database.
Please follow the next installation steps in order to get it working nicely in a local environmnet.

1. Clone the repository to your PC
    Clone the repository with `git clone <repo.url>`

2. Install virtual environment for Python
    This helps the Python environment to stay clean and avoid package version collisions

    - if you don't have Python 2.7.x installed, please do install it and add it to PATH
    - install PIP (Python package manager)
    - install virtualenvironment package with pip (pip install virtualenv)
    - create your virtualenvironment somewhere **preferably outside** the project folder not to commit it to git.
        - for example `cd ..` -> `mkdir venv` -> `virtualenv venv`
        - now you can activate it with `source venv/Scripts/activate` in Windows (use ./activate in *NIX)
        - there should be (venv) reading in front of the command line cursor. This means that you are now using a project-specific virtual environment
        - install the required packages specified in a given .txt file by running **`pip install -r requirements.txt`**
    - You are done! Hooray!

3. Create the database on first use
    - `python db_create.py`

4. Run the app
    - run the development server **`python run.py`**

5. If everything works as it should, the development server should give you a local address for the API


## Using the API

1. The API can be queried from the endpoints by using a web browser (for GET requests)
    - try http://localhost:5000/user/1
    - it should return an error in JSON format. This means that the database is still empty.

2. Create a new user via the API with a HTTP POST request.
    - for this I'd recommend using a helper app postman https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en
    - in Postman create a POST request with a parameter (form-data) Key:name, Value:Jonathan
    - if successful, the API returns success and the ID of the created user
    - now go fetch the user data in JSON format from http://localhost:5000/user/1 - it works!


## API endpoints

This page specifies how to use the API from the front-end/Android app: https://martijnroo.github.io/fitness-back-end/.

To edit that page, follow these steps:

1. Clone the repository again, but in a different folder. For example: `git clone <repo.url> github-pages`

2. Go into the repository directory: `cd githup-pages`

3.  Checkout a special branch containing the GitHub pages website `git checkout gh-pages` Now, only the website files are visible in the github-pages directory and you can edit the files (**especially `index.md`**).

5. Use Jekyll to preview your changes before pushing them. Info on installing and using Jekyll [can be found here](https://help.github.com/articles/using-jekyll-with-pages/).

6. Commit and push your changes to the gh-pages branch with `git push origin gh-pages`. After that, the changed website shows up at https://martijnroo.github.io/fitness-back-end/.

**Note:** GitHub pages and the `index.md` file use Markdown as a markup language. Please [check this page](https://guides.github.com/features/mastering-markdown/#examples) explaining Markdown if you haven't used it before.
