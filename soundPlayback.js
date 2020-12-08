let context = new AudioContext();


// Diese Daten bekommt man später von der Schnittstelle
let flag1 = true;
let flag2 = false;
let flag3 = false;
let flag4 = false;

if(flag1){
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
}

if(flag2){
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
}

if(flag3){
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
}

if(flag4){
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
}