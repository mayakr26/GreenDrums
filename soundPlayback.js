let context = new AudioContext();

function startSound() {
    switch (x) {
        case 1:
            fetch("drumsounds/sound1.wav")
            .then(response => response.arrayBuffer())
            .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
            .then(audioBuffer => {
                let sourceBufferNode = context.createBufferSource();
                sourceBufferNode.buffer = audioBuffer;

                sourceBufferNode.connect(context.destination);
                sourceBufferNode.start(context.currentTime);
            })
            .catch(console.error);
            break;
        case 2:
            fetch("drumsounds/sound2.wav")
            .then(response => response.arrayBuffer())
            .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
            .then(audioBuffer => {
                let sourceBufferNode = context.createBufferSource();
                sourceBufferNode.buffer = audioBuffer;

                sourceBufferNode.connect(context.destination);
                sourceBufferNode.start(context.currentTime);
            })
            .catch(console.error);
            break;
        case 3:
            fetch("drumsounds/sound3.wav")
            .then(response => response.arrayBuffer())
            .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
            .then(audioBuffer => {
                let sourceBufferNode = context.createBufferSource();
                sourceBufferNode.buffer = audioBuffer;

                sourceBufferNode.connect(context.destination);
                sourceBufferNode.start(context.currentTime);
            })
            .catch(console.error);
            break;
        case 4:
            fetch("drumsounds/sound4.wav")
            .then(response => response.arrayBuffer())
            .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
            .then(audioBuffer => {
                let sourceBufferNode = context.createBufferSource();
                sourceBufferNode.buffer = audioBuffer;

                sourceBufferNode.connect(context.destination);
                sourceBufferNode.start(context.currentTime);
            })
            .catch(console.error);
            break;

    }
}