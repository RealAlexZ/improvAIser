const RhythmSequencer = () => {
    const [isPlaying, setIsPlaying] = React.useState(false);
    const [isRecording, setIsRecording] = React.useState(false);
    const [currentBeat, setCurrentBeat] = React.useState(-1);
    const [userBeatsRow1, setUserBeatsRow1] = React.useState(Array(16).fill(0));
    const [userBeatsRow2, setUserBeatsRow2] = React.useState(Array(16).fill(0));
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

    const tempo = 120;
    const beatInterval = (60 / tempo) * 1000;
    const eligibleKeys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'];

    React.useEffect(() => {
        const handleKeyPress = (e) => {
            if (isRecording && eligibleKeys.includes(e.key)) {
                const newBeatsRow1 = [...userBeatsRow1];
                const newBeatsRow2 = [...userBeatsRow2];
                
                if (currentBeat < 16) {
                    newBeatsRow1[currentBeat] = 1;
                } else {
                    newBeatsRow2[currentBeat - 16] = 1;
                }
                
                setUserBeatsRow1(newBeatsRow1);
                setUserBeatsRow2(newBeatsRow2);
            }
        };

        if (isRecording) {
            window.addEventListener('keydown', handleKeyPress);
        }
        return () => window.removeEventListener('keydown', handleKeyPress);
    }, [isRecording, currentBeat, userBeatsRow1, userBeatsRow2]);

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
                    if (beat >= 31) {
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
        setUserBeatsRow1(Array(16).fill(0));
        setUserBeatsRow2(Array(16).fill(0));
        backgroundAudioRef.current.currentTime = 0;
        backgroundAudioRef.current.play();
    };

    const startRecording = () => {
        setUserBeatsRow1(Array(16).fill(0));
        setUserBeatsRow2(Array(16).fill(0));
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
                <div>Your Input:</div>
                <div className="sequence-grid">
                    {userBeatsRow1.map((beat, index) => (
                        <div
                            key={`row1-${index}`}
                            className={`beat-box ${
                                beat === 1 ? 'correct' : ''
                            } ${currentBeat === index ? 'current' : ''}`}
                        />
                    ))}
                </div>
                <div className="sequence-grid">
                    {userBeatsRow2.map((beat, index) => (
                        <div
                            key={`row2-${index}`}
                            className={`beat-box ${
                                beat === 1 ? 'correct' : ''
                            } ${currentBeat === index + 16 ? 'current' : ''}`}
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