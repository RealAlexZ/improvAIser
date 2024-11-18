const RhythmSequencer = () => {
    const [isPlaying, setIsPlaying] = React.useState(false);
    const [isRecording, setIsRecording] = React.useState(false);
    const [currentBeat, setCurrentBeat] = React.useState(-1);
    const [userBeats, setUserBeats] = React.useState(Array(16).fill(0));
    const [countdown, setCountdown] = React.useState(-1);
    
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

    const targetPattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0];
    const tempo = 120;
    const beatInterval = (60 / tempo) * 1000;

    React.useEffect(() => {
        const handleKeyPress = (e) => {
            if (isRecording && e.key === 'j') {
                const newBeats = [...userBeats];
                if (targetPattern[currentBeat] === 1) {
                    newBeats[currentBeat] = 1;
                } else {
                    newBeats[currentBeat] = -1;
                }
                setUserBeats(newBeats);
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
        setIsPlaying(true);
        setCurrentBeat(0);
        setUserBeats(Array(16).fill(0));
        backgroundAudioRef.current.currentTime = 0;
        backgroundAudioRef.current.play();
    };

    const startRecording = () => {
        setUserBeats(Array(16).fill(0));
        setCountdown(4);
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