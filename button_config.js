// FIX 1: Point directly to your program file
async function fetchPythonSource() {
  return fetch("./program.py").then((r) => r.text());
}

// Helper to fetch the library
async function fetchmylibrary() {
  return fetch("./mylibrary.py").then((r) => r.text());
}

// Error checking
function addErrorToDOM(error) {
  const mylibraryError = error.message.split(/Error in/)[1];
  let errorMessage;
  if (mylibraryError) {
      errorMessage = "Error in" + mylibraryError;
  } else {
      let errorTokens = error.message.split(/  File/);
      let lastToken = errorTokens.pop();
      errorTokens = lastToken.split("\n");
      errorMessage = errorTokens.slice(1).join("\n");
  }
  if (errorMessage) {
      const errorElement = document.querySelector("#error");
      errorElement.style.padding = "32px";
      errorElement.style.margin = "24px";
      errorElement.textContent = errorMessage;
  }
}

// For if Pyodide loads
const pyodideLoadedEvent = new Event("PyodideLoaded");

(async () => {
  let pyodide = await loadPyodide();
  let librarySource = await fetchmylibrary();
  pyodide.FS.writeFile("mylibrary.py", librarySource);

  // Load the main program
  let pythonSourceCode = await fetchPythonSource();
  pyodide.runPython(pythonSourceCode);
})()
  .then(() => {
      window.dispatchEvent(pyodideLoadedEvent);
      window.addEventListener("error", addErrorToDOM);
  })
  .catch((e) => {
      addErrorToDOM(e);
      enableStartButton();
  });

// When Pyodide loads, enable the start button
window.addEventListener("PyodideLoaded", () => {
  if (document.readyState === "complete") {
      enableStartButton();
  } else {
      window.addEventListener("DOMContentLoaded", enableStartButton);
  }
});

// To disable the start button after it has been pressed
function disableStartButton() {
    const startButton = document.querySelector("#start");
    if (startButton) {
        startButton.disabled = true;
    }
}

// Enable start button
function enableStartButton() {
    const startButton = document.querySelector("#start");
    if (startButton) {
        startButton.disabled = false;
    }
}

// To disable the pause button after it has been pressed
function disablePauseButton() {
    const pauseButton = document.querySelector("#pause");
    if (pauseButton) {
        pauseButton.disabled = true;
    }
    // Adds the blackout screen again so the player can't interact while paused
    const blackout = document.createElement('div');
    blackout.setAttribute('id', 'blackout');
    const canvas = document.getElementById('canvas');
    canvas.appendChild(blackout);  
}

// For when the buttons are enabled and ready to be pressed
function enableButtons() {
    const otherButtons = document.querySelectorAll(".other-buttons");
    if (otherButtons) {
        // Enable every button, one by one
        for (let i = 0; i < otherButtons.length; i++) {
            otherButtons[i].disabled = false;
        }
    }
    // Remove blackout so user can interact with the project
    const parent = document.getElementById("canvas");
    const child = document.getElementById("blackout");
    parent.removeChild(child);
}

    // Event listener for the start/play button
    // Also creates a new button since bthe old one gets deleted
    document.body.addEventListener("start", () => {
    const startButton = document.createElement("button");
    startButton.setAttribute("id", "start")
    startButton.classList.add("button-style");
    //startButton.IdList.add("start");
    startButton.onclick = play;
    startButton.innerHTML = `
          <img src="resources/play.png" class="btn-icon">
          <p class="btn-text">Play</p>
    `;
    document.querySelector(".button-container").prepend(startButton);
});

// Makes the animations play
function play() {
    function _translate_x(element, distance, time = null) {
        function _translate() {
            element.style.transform = `translateX(${distance}px)`;
        }
        element.start_time = Date.now();
        setTimeout(_translate, 50);
    }
  // Disable the start button and enable the other ones
  disableStartButton();
  enableButtons();
    

function _translate_y(element, distance) {
    function _translate() {
        element.style.transform = `translateY(${distance}px)`
    }
    element.start_time = Date.now()
    setTimeout(_translate, 50)
}
    const allElements = document.querySelectorAll("#canvas img");
    allElements.forEach((element) => {
        element.start_time = Date.now();
        element.style.transition = `${element.time}s linear transform`;
        if (element.animation_direction === "right") {
            _translate_x(element, element.distance_left);
        } else if (element.animation_direction === "left") {
            _translate_x(element, -element.distance_left);
        } else if (element.animation_direction === "up") {
            _translate_y(element, -element.distance_left);
        } else if (element.animation_direction === "down") {
            _translate_y(element, element.distance_left);
        }
        
    });
}

// Pause button functionality
function pause() {
    // Selects all images within the canvas
    const allElements = document.querySelectorAll("#canvas img");
    // Set and track positioning/location of each img
    allElements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        const canvasRect = document.querySelector("#canvas").getBoundingClientRect();
        const top = rect.top - canvasRect.top;
        const left = rect.left - canvasRect.left;
        const width = element.style.width;
        element.style = "";
        element.style.position = "absolute";
        element.style.top = top + "px";
        element.style.left = left + "px";
        element.style.transition = "";
        element.style.transform = "";
        element.style.width = width;

        // Tracks animations within the images in the canvas
        element.time = element.time - (Date.now() - element.start_time) / 1000;
        if (element.animation_direction === "left") {
            element.distance_left = element.distance - (element.start_position - left)
        } else if (element.animation_direction === "right") {
            element.distance_left = element.distance - (left - element.start_position);
        } else if (element.animation_direction === "up") {
            element.distance_left = element.distance - (element.start_position - top);
        } else if (element.animation_direction === "down") {
            element.distance_left = element.distance - (top - element.start_position);
        }
    });
    // Disable pause button but enable start button
    disablePauseButton();
    enableStartButton();
}

// Mute button for audio elements on the page
function mutePage() {
    const bgMusic = document.querySelector("#bg-music");
    if (bgMusic) {
        bgMusic.pause();
    }
}

function start(button) {
    document.body.dispatchEvent(new Event("start"));
    button.remove();
    const bgMusic = document.querySelector("#bg-music");
    if (bgMusic) {
        bgMusic.play();
    }
    enableButtons();
    disableStartButton();
}