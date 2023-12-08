# Instructions
# 1)The first thing to do is to clone the repository:
$ git clone https://github.com/AlenaIsialionak/Graduation-project
$ cd Graduation-project
# 2)Create a virtual environment to install dependencies in and activate it:
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
# 3)Then install the dependencies:
$ pip install -r requirements.txt

# Once pip has finished downloading the dependencies:
$ python manage.py runserver

#Docker
```bash
# Create the Docker image
docker build -t django_img .
# Run the Docker container from image 
docker run -p 8000:8000 --name django_container django_img
```

## Usage example:

```bash
# Service endpoint: http://localhost:8000
