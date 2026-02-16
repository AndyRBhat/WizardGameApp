# 🧙‍♂️ Wizard Survival

> **A survival game built with Python, running entirely in the browser using Pyodide, which is a webAssembly translator that teaches the browser to understand Python.**

![Game Screenshot](/images/Game%20screenshot.png)

# 🎮 [CLICK HERE TO PLAY THE GAME](https://andyrbhat.github.io/WizardGameApp/)
---

## 📖 About the Project

**Wizard Survival** is an interactive 2D survival game where players play as a wizard travelling in a forest, where they must dodge incoming, hungry monsters and survive for 135 seconds!

I built this project to practice **Event-Driven Programming** and **Python Logic**. Unlike standard Python scripts that run in a terminal, this project runs in the browser using **Pyodide**, allowing me to write Python code that controls web elements in real-time.

### 🎯 Learning Goals
This project helped me deepen my understanding of:
* **WebAssembly:** Running compiled Python code in the browser without a backend server.
* **Event-Driven Programming:** Handling user inputs and game loops asynchronously.
* **Algorithm Design:** Creating difficulty (No. of monsters spawned) that scales with the game timer.

---

## 🎮 How to Play

* **Objective:** Survive for **135 seconds** without dying.
* **Mechanics:** Monsters spawn at increasing rates as the timer counts down. Try to survive their assault!

### 🕹️ Controls

| Key | Action |
| :---: | :--- |
| **W** | Move Up ⬆️ |
| **A** | Move Left ⬅️ |
| **S** | Move Down ⬇️ |
| **D** | Move Right ➡️ |

---

## 🛠️ Technical Implementation

The project utilizes Pyodide to run python on a webpage.

### 1. Game Logic (My Contribution)
The core gameplay resides in `program.py`, which I wrote to implement the game mechanics.
* **State Management:** Tracking variables for health, timer, and coordinate positions (`x`, `y`).
* **Game Loop:** Implementing the `countdown()` function and monster spawning logic using interval timers.
* **Collision Logic:** Defining what happens to the wizard(player)'s health when they get hit by the monsters.
* **Input Handling:** Allowing for player movement using standard WASD keystrokes.
* **Algorithm Design:** Creating logic that increases monster spawn rates as the timer decreases (difficulty scaling).

### 2. The Engine (Pyodide & JavaScript)
This game uses `pyodide.js` to load the Python runtime.
* **`button_config.js`**: Fetches the raw Python code and writes it to Pyodide's virtual filesystem. It captures browser events to start the game loop.
* **`mylibrary.py` (Helper Tool)**: To support interaction with the HTML DOM, I utilized a helper library that abstracts functions needed to handle HTML elements. It handles creating HTML elements, CSS transformations, and managing `setTimeout`/`setInterval`.

---

## 📂 Project Structure

```text
├── images/             # Game assets (sprites, backgrounds)
├── audio/              # Sound effects and music
├── resources/          # UI icons and styles
├── program.py          # Main game logic (Written by me)
├── mylibrary.py        # Custom Python-to-JS wrapper library
├── button_config.js    # Pyodide configuration and loader
├── index.html          # Main entry point
└── style.css           # Game styling

```
## 🚀 How to Run Locally

Because this project uses WebAssembly, browsers will block it if you try to open `index.html` directly from your file explorer due to **CORS (Cross-Origin Resource Sharing)** policies. You must run a local server to play it.

### Option 1: Using Visual Studio Code (Recommended)
This is the easiest method if you are using VS Code.

1.  **Install the "Live Server" Extension:**
    * Open VS Code and click the Extensions icon on the left sidebar.
    * Search for **"Live Server"** (by Ritwick Dey) and install it.
2.  **Open the Project:**
    * Open the `wizard-survival` folder in VS Code.
3.  **Launch the Game:**
    * Right-click on `index.html` in the file explorer.
    * Select **"Open with Live Server"**.
    * Your default browser will open automatically and the game will load.

> **⚠️ Note on "Missing Import" Errors:**
> When viewing the code in VS Code, you may see red error squiggles under lines like `from js import document` or `from pyodide import ...`.
> * **This is normal.** These libraries only exist inside the web browser's runtime (Pyodide).
> * Your local visual studio editor (Pylance extention) cannot see them, but the code will run perfectly in the browser.

### Option 2: Using Python Terminal
If you prefer the command line or don't use VS Code:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/wizard-survival.git](https://github.com/yourusername/wizard-survival.git)
    cd wizard-survival
    ```
2.  **Start the server:**
    ```bash
    python -m http.server
    ```
3.  **Open the Game:**
    * Visit `http://localhost:8000` in your browser.

``
## 🔮 Future Improvements
[ ] Scoreboard: Implement local storage to save high scores.

[ ] Power-ups: Add tomes(power ups) to restore health or help dealing with monsters.

[ ] Mobile Support: Add touch controls for mobile playability.


`
# 👨‍💻 Author
Andy(Aniruddha) R Bhat Aspiring Programmer & Robotics Engineer | Class of 2028
Built using Python and Pyodide.