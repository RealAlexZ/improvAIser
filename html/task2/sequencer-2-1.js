const rhythmBlocks = [
    [1, 0, 0, 0],
    [1, 0, 1, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 1]
];

const generateRandomPattern = () => {
    let pattern = [];
    // We need 4 blocks to make a 16-beat pattern
    for (let i = 0; i < 4; i++) {
        const randomBlock = rhythmBlocks[Math.floor(Math.random() * rhythmBlocks.length)];
        pattern = [...pattern, ...randomBlock];
    }
    return pattern;
};

const RhythmSequencer = () => {
    const [isPlaying, setIsPlaying] = React.useState(false);
    const [isRecording, setIsRecording] = React.useState(false);
    const [currentBeat, setCurrentBeat] = React.useState(-1);
    const [userBeats, setUserBeats] = React.useState(Array(16).fill(0));
    const [countdown, setCountdown] = React.useState(-1);
    const [targetPattern, setTargetPattern] = React.useState(generateRandomPattern());
    
    const backgroundAudioRef = React.useRef(null);
    
    React.useEffect(() => {
        if (!backgroundAudioRef.current && audioData.background) {
            backgroundAudioRef.current = new Audio(audioData.background);
            backgroundAudioRef.current.loop = true;
        }
        
        return () => {
            if (backgroundAudioRef.current) {
                backgroundAudioRef.current.pause();
                backgroundAudioRef.current.currentTime = 0;
            }
        };
    }, []);

    const tempo = 120;
    const beatInterval = (60 / tempo) * 1000;
    const eligibleKeys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'];

    React.useEffect(() => {
        const handleKeyPress = (e) => {
            if (isRecording && eligibleKeys.includes(e.key)) {
                const newBeats = [...userBeats];
                if (targetPattern[currentBeat] === 1) {
                    newBeats[currentBeat] = 1;
                } else {
                    newBeats[currentBeat] = -1;
                }
                setUserBeats(newBeats);

                if (socket.readyState === WebSocket.OPEN) {
                    socket.send(keyMappings[e.key] + ":" + currentBeat);  // Send the key press to the server
                }
            }
        };

        if (isRecording) {
            window.addEventListener('keydown', handleKeyPress);
        }
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [isRecording, currentBeat, userBeats]);

    React.useEffect(() => {
        let intervalId;

        if (countdown > 0) {
            intervalId = setInterval(() => {
                setCountdown(c => c - 1);
            }, 1000);
        } else if (countdown === 0) {
            setIsRecording(true);
            setCountdown(-1);
            setCurrentBeat(0);
            backgroundAudioRef.current.currentTime = 0;
            backgroundAudioRef.current.play();
        }

        if ((isPlaying || isRecording) && countdown === -1) {
            intervalId = setInterval(() => {
                setCurrentBeat(beat => {
                    if (beat >= 15) {
                        if (isRecording) {
                            setIsRecording(false);
                            setIsPlaying(false);
                            backgroundAudioRef.current.pause();
                            backgroundAudioRef.current.currentTime = 0;
                            
                            if (socket.readyState === WebSocket.OPEN) {
                                socket.send("END");  // Send the key press to the server
                            }
                            
                            return -1;
                        }
                        backgroundAudioRef.current.currentTime = 0;
                        return 0;
                    }
                    return beat + 1;
                });
            }, beatInterval);
        }

        return () => {
            clearInterval(intervalId);
        };
    }, [isPlaying, isRecording, countdown]);

    const startPlayback = () => {
        setTargetPattern(generateRandomPattern());
        setIsPlaying(true);
        setCurrentBeat(0);
        setUserBeats(Array(16).fill(0));
        backgroundAudioRef.current.currentTime = 0;
        backgroundAudioRef.current.play();
    };

    const startRecording = () => {
        setUserBeats(Array(16).fill(0));
        setCountdown(4);

        if (socket.readyState === WebSocket.OPEN) {
            socket.send("Task 1");  // Send the key press to the server
            let send_str = "";
            for (let i = 0; i < targetPattern.length; ++i) {
                send_str += targetPattern[i].toString();
            }
            socket.send(send_str);
        }
    };

    const stopSequencer = () => {
        setIsPlaying(false);
        setIsRecording(false);
        setCurrentBeat(-1);
        setCountdown(-1);
        backgroundAudioRef.current.pause();
        backgroundAudioRef.current.currentTime = 0;
    };

    return (
        <div className="sequencer-container">
            {/* Countdown Overlay */}
            {countdown > 0 && (
                <div className="countdown-overlay">
                    {countdown}
                </div>
            )}
            
            <div className="controls">
                <button
                    onClick={startPlayback}
                    disabled={isPlaying || isRecording}
                    className="btn btn-play"
                >
                    ▶️ Play
                </button>
                <button
                    onClick={startRecording}
                    disabled={isPlaying || isRecording}
                    className="btn btn-record"
                >
                    ⏺️ Record
                </button>
                <button
                    onClick={stopSequencer}
                    disabled={!isPlaying && !isRecording}
                    className="btn btn-stop"
                >
                    ⏹️ Stop
                </button>
            </div>

            <div>
                <div>Rhythm Blocks:</div>
                <div className="sequence-grid">
                    {targetPattern.map((beat, index) => (
                        <div
                            key={`target-${index}`}
                            className={`beat-box ${beat ? 'active' : ''} ${currentBeat === index ? 'current' : ''}`}
                        />
                    ))}
                </div>
            </div>

            <div>
                <div>Your Input:</div>
                <div className="sequence-grid">
                    {userBeats.map((beat, index) => (
                        <div
                            key={`user-${index}`}
                            className={`beat-box ${
                                beat === 1 ? 'correct' : 
                                beat === -1 ? 'incorrect' : ''
                            } ${currentBeat === index ? 'current' : ''}`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
};

ReactDOM.render(
    <RhythmSequencer />,
    document.getElementById('sequencer-root')
);