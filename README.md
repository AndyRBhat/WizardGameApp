# 🧙‍♂️ Wizard Survival

> **A browser-based survival game built with Python, running entirely in the client via WebAssembly (Pyodide).**

![Game Screenshot](/images/Game%20screenshot.png)

---

## 📖 About the Project

**Wizard Survival** is an interactive 2D game where players control a wizard to dodge incoming enemies and survive against the clock.

I built this project to practice **Event-Driven Programming** and **Python Logic**. Unlike standard Python scripts that run in a terminal, this project runs in the browser using **Pyodide**, allowing me to write Python code that controls web elements in real-time.

### 🎯 Learning Goals
This project helped me deepen my understanding of:
* **WebAssembly:** Running compiled Python code in the browser without a backend server.
* **Event-Driven Programming:** Handling user inputs and game loops asynchronously.
* **Algorithm Design:** Creating difficulty scaling that reacts to the game timer.

---

## 🎮 How to Play

* **Objective:** Survive for **135 seconds** without letting your health drop to zero.
* **Mechanics:** Enemies spawn at increasing rates as the timer counts down. Colliding with enemies reduces health.

### 🕹️ Controls

| Key | Action |
| :---: | :--- |
| **W** | Move Up ⬆️ |
| **A** | Move Left ⬅️ |
| **S** | Move Down ⬇️ |
| **D** | Move Right ➡️ |

---

## 🛠️ Technical Implementation

This project utilizes a custom architecture to execute Python in the browser.

### 1. Game Logic (My Contribution)
The core gameplay resides in `program.py`, which I wrote to implement the game mechanics.
* **State Management:** Tracking variables for health, timer, and coordinate positions (`x`, `y`).
* **Game Loop:** Implementing the `countdown()` and enemy spawning logic using interval timers.
* **Collision Logic:** Defining how the wizard interacts with enemies.
* **Input Handling:** Binding keyboard events to coordinate updates.
* **Algorithm Design:** Creating logic that increases enemy spawn rates as the timer decreases (difficulty scaling).

### 2. The Engine (Pyodide & JavaScript)
The application relies on `pyodide.js` to load the Python runtime.
* **`button_config.js`**: Fetches the raw Python code and writes it to Pyodide's virtual filesystem. It captures browser events to initialize the game loop.
* **`mylibrary.py` (Helper Tool)**: To facilitate interaction with the HTML DOM, I utilized a helper library that abstracts low-level JS operations. It handles creating HTML elements, CSS transformations, and managing `setTimeout`/`setInterval`.

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

**1. Clone the repository**
git clone [https://github.com/yourusername/wizard-survival.git](https://github.com/yourusername/wizard-survival.git)
cd wizard-survival

2. Start a local server (using Python):
python -m http.server

3. Open the Game:
! Open http://localhost:8000 in your browser

``
## 🔮 Future Improvements
[ ] Scoreboard: Implement local storage to save high scores.

[ ] Power-ups: Add collectible items to restore health or freeze enemies.

[ ] Mobile Support: Add touch controls for mobile playability.


`
# 👨‍💻 Author
Andy(Aniruddha) R Bhat Aspiring Programmer & Robotics Engineer | Class of 2028
Built using Python and Pyodide.