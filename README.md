## NoteTakingAssessment Documentation

NoteTakingAssessment is an assessment project designed for a company's internal evaluation process. This project involves note-taking features and runs on a Dockerized environment using a Python backend and PostgreSQL as the database.

## Prerequisites
Before running the project, ensure that you have the following tools and packages installed:

1) Docker and Docker Compose: Docker is used for containerizing the application and PostgreSQL database, while 2)Docker Compose orchestrates the multiple services required for the project.

2) Python (latest version): The project requires Python for running the backend and the necessary packages.

3) PostgreSQL: This project uses PostgreSQL as its primary database. You can run it through Docker.

## Installation of Required Tools
1. Docker & Docker Compose
# Ubuntu / Debian:
sudo apt update
sudo apt install docker.io docker-compose

# Arch Linux:
sudo pacman -S docker docker-compose

MacOS: Download and install Docker Desktop from Docker's official website.

# Ensure Docker is running:
docker --version
docker-compose --version


2. Python (Latest Version)
# Ubuntu / Debian:
sudo apt update
sudo apt install python3 python3-pip

# Arch Linux:
sudo pacman -S python python-pip

# macOS: Install Python via Homebrew:
brew install python
Verify Python Installation:
python3 --version
pip3 --version


3. PostgreSQL
# PostgreSQL will be installed through Docker, so no additional local installation is required.


## Running the Project

# Step 1: Clone the Repository
To get started with the project, clone the repository to your local machine:

1) git clone https://github.com/your-username/NoteTakingAssessment.git
2) cd NoteTakingAssessment

# Step 2: Set Up Environment Variables
Create a .env file in the project root directory and add the following environment variables:
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=note_taking_assessment
TOKEN=your_telegram_bot_token
DOMAIN=your_web_domain
HOST=your_host_name # typically 0.0.0.0
PORT=your_web_port  # typically 8000 by default

NB: Make sure to replace your_postgres_user and your_postgres_password with your actual PostgreSQL credentials.

# Step 3: Build and Run Docker Containers
The project is set up with Docker Compose. To start the containers for the backend and database, run the following command:

docker-compose up --build
This command will:

Build the Docker images for the application.
Start up the PostgreSQL container and the Python backend container.

# Step 4: Running Database Migrations
Once the Docker containers are running, you'll need to apply the database migrations:
docker-compose exec web python manage.py migrate

# Step 5: Access the Application
After the containers are up and running, you can access the application in your browser at:

http://localhost:8000

# Step 6: Stopping the Application
To stop the running Docker containers, execute:
docker-compose down
