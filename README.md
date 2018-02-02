# Reddit Delete

Reddit-Delete is a python script to delete old reddit post and comments, but you still want to keep your account.
It scans your content in specific subreddits.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The scripts require python 3, and the following third party libraries:

* Praw
* Tendo
* Fire

### Installing

You can automatically install all the required package by using [pipenv](http://pipenv.readthedocs.io/en/latest/):

```bash
pipenv install
```

Or you can install manually the required libraries:

```bash
pip3 install praw
pip3 install fire
pip3 install tendo
```

### Executing

The main script is [delete_content.py](delete_content.py) and you can easily execute either with pipenv or just with python.

Pipenv:

```bash
pipenv run python delete_content.py --subreddits [aww,hardcoreaww] --days-old 400
```

Just Python:

```bash
python delete_content.py --subreddits [aww,hardcoreaww] --days-old 400
```

## Built With

* [Praw](https://github.com/praw-dev/praw/) - For simple access to Reddit's API.
* [Tendo](https://github.com/pycontribs/tendo) - Single Instance to prevent your script from running in parallel.
* [Fire](https://github.com/google/python-fire) - For command line argument parsing

## Authors

* **Charalampos Gkikas** - *Initial work* - [hargikas](https://github.com/hargikas)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* The meteo.gr free use of web-cameras, and anyone who publices their meteo footage.