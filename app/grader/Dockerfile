## We're using this Dockerfile as a sandbox to run a grading system for our students input
## Use a slim Python image for security
FROM python:3.10-slim
## We're giving minimal python installation with very few packages so they can't do anything too extreme

## Add a non-root user for safety
RUN useradd -m student
## The reason why we're doing this is because if we create a new user inside the container,
## that user will not be the root user who has all the privileges.

## Set working directory
WORKDIR /home/student
## Now we change the directory to the user we just created

## Switch to non-root user
USER student
## Now that we're in the user's directory, let's also switch the new user as well.

## Set permissions tightly
RUN chmod 700 /home/student
## Now let's also change the permissions of students to only have ACCESS to /home/student

## This will start a simple python shell by default
CMD ["python3"]
## This just launches python at the start

### Tested this file, and it seems to work:
### >>> import getpass
### >>> print(getpass.getuser())
### student

## Build the image first: docker build -t safe-python-grader .

### ran this code: docker run --rm -it safe-python-grader