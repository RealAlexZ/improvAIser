// Selecting piano keys using their ids
let keys = ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5'];
let pianoKeys = {};
keys.forEach(function(key) {
    pianoKeys[key] = document.querySelector('#' + key);
});

let noteDirectory = 'notes';

// Playing the note (at max volume)
function playNote(note) {
    let audio = audioFiles[note].cloneNode(true); // Clone Audio object

    audio.volume = 1.0;
    audio.play();

    audio.onended = function() {
        audio.currentTime = 0;
    };
}

// Pressed animation defining and mousedown/up calling in
function addPressed(key) {
    key.classList.add('pressed');
}

function removePressed(key) {
    key.classList.remove('pressed');
}

// Mouse Events
keys.forEach(function(key) {
    pianoKeys[key].onmousedown = function() {
        playNote(key);
        addPressed(this);
        noteDisplay.innerText = key; // Fixed mouse note Display error
    };

    pianoKeys[key].onmouseup = function() {
        removePressed(this);
    };

    pianoKeys[key].onmouseout = function() {
        removePressed(this);
    };
});

// Keyboard handling
const keyMappings = {
    'a': 'C4',
    's': 'D4',
    'd': 'E4',
    'f': 'G4',
    'g': 'A4',
    'h': 'C5',
    'j': 'D5',
    'k': 'E5',
    'l': 'G5',
    ';': 'A5'
};

let noteDisplay = document.querySelector('#noteDisplay');
let originalText = noteDisplay.innerText;
const pressedKeys = {}; // Fixed bell ringing issue
let loaded = false;

document.body.addEventListener('keydown', function(e) {
    if (loaded === true) {
        const key = e.key.toLowerCase();
        if (key === ' ') { // Linking spacebar with noteDisplay
            noteDisplay.click();
        }
        if (keyMappings[key] && !pressedKeys[key]) {
            let pianoKey = pianoKeys[keyMappings[key]];
            addPressed(pianoKey);
            playNote(keyMappings[key]);
            noteDisplay.innerText = keyMappings[key];
            pressedKeys[key] = true;
        }
    } else {
        alert('ePiano is loading');
    }
});

document.body.addEventListener('keyup', function(e) {
    const key = e.key.toLowerCase();
    if (keyMappings[key]) {
        let pianoKey = pianoKeys[keyMappings[key]];
        removePressed(pianoKey);
        pressedKeys[key] = false;
    }
});

// Audio file linking
const noteNames = ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5'];
let audioFiles = {};

// Audio preloading
async function preloadAudio(dataUrl) {
    const audio = new Audio();

    const load = async () => {
        return new Promise((resolve, reject) => {
            audio.src = dataUrl;
            audio.oncanplaythrough = () => resolve(audio);
            audio.onerror = reject;
        });
    };

    await load();
    return audio;
}

async function loadAudioFiles() {
    let loadedCount = 0;
    const totalNotes = noteNames.length;

    noteDisplay.innerText = `Loading: 0/${totalNotes}`;

    try {
        for (let note of noteNames) {
            try {
                audioFiles[note] = await preloadAudio(audioData[note]);
                loadedCount++;
                noteDisplay.innerText = `Loading: ${loadedCount}/${totalNotes}`;
            } catch (error) {
                console.error(`Failed to load ${note}:`, error);
            }
        }

        if (loadedCount === totalNotes) {
            noteDisplay.innerText = originalText;
            loaded = true;
        } else {
            noteDisplay.innerText = "Error: Some notes failed to load";
        }
    } catch (error) {
        console.error("Error loading audio files:", error);
        noteDisplay.innerText = "Error loading audio";
    }
}

// Note Names to keys
document.addEventListener("DOMContentLoaded", function() {
    noteDisplay.innerText = "Loading...";

    let keys = document.querySelectorAll(".keys div");
    keys.forEach(function(key) {
        let span = key.querySelector("span");
        span.textContent = key.id;
        span.classList.add('hidden');
    });

    // Load when page is ready
    loadAudioFiles().then(() => {
        noteDisplay.innerText = originalText;
        loaded = true;
    });
});

// Toggle Note Display
noteDisplay.addEventListener('click', function() {
    const noteElements = document.querySelectorAll('.note');

    noteElements.forEach((element) => {
        element.classList.toggle('hidden');
    });
});

noteDisplay.addEventListener('mouseenter', function() {
    originalText = noteDisplay.innerText;
    noteDisplay.innerText = "Toggle Notes";
    noteDisplay.style.fontSize = "1.1rem";
});

noteDisplay.addEventListener('mouseleave', function() {
    noteDisplay.innerText = originalText;
    noteDisplay.style.fontSize = "1.3rem";
});