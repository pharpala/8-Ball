# Pool Game Application

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

## Technologies used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Javascript](https://img.shields.io/badge/Javascript-F0DB4F?style=for-the-badge&labelColor=black&logo=javascript&+logoColor=F0DB4F)
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

## Introduction

Welcome to the Pool Game Application! This is a full stack web application that simulates a pool game. The game features realistic physics, allowing players to enjoy a smooth and engaging experience.

## Features

- Realistic physics using a C library, allowing for precise ball movements and collision handling.
- Backend scripting and server handling with Python.
- SQLite database to store game and player information.
- Interactive front end built with HTML, CSS, and JavaScript.
- Easy-to-use interface for entering game and player information.

## Technology Stack

- **C**: Physics engine for the game.
- **Python**: Backend and scripting.
- **Swig**: To connect Python and C code.
- **SQLite**: Database management.
- **JavaScript**: Frontend interactivity.
- **HTML/CSS**: Frontend structure and styling.

## Screenshots

Here are some screenshots of the application:

### Home Screen

![Home Screen](utils/home_screen.png)

### Game Setup

![Game Setup](utils/game_setup.png)

### Game Ending

![Game End](utils/game_end.png)

## Installation

To run this application, you will need the socslinux container. If you have it, run it and follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/pharpala/8-Ball.git
    cd 8-ball
    cd src
    ```

2. **Compile the C code**:
    Use the following command to compile the C code:

    ```bash
    make
    ```

3. **Attach Shared C library**:
    Use the following command to attach the .so library to the program:

    ```bash
    export LD_LIBRARY_PATH=`pwd`
    ```

4. **Run the application**:

    ```bash
    python server.py 5500
    ```

## Usage

1. Open your browser and go to `http://localhost:5000`.
2. Enter the game name and player names when prompted.
3. Start the game and enjoy! You can drag the cue ball to play.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
