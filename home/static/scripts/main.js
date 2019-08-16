let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition)();

recognition.interimResults = true;
recognition.maxAlternatives = 5;
recognition.continuous = true;


let finalTranscript = '';

recognition.onend = (event) => {
    recognition.start();
}

recognition.onresult = (event) => {
    $('.microphone-status').text('Recognizing...');
    let interimTranscript = '';
    finalTranscript = '';
    for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
        let transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
            finalTranscript += transcript;
            $('.microphone-status').text('Fetching Result...');
            send_query(finalTranscript);
        } else {
            interimTranscript += transcript;
        }
    }
    $('.query').html(finalTranscript + '<i style="color:#555;">' + interimTranscript + '</>');
}

voices = window.speechSynthesis.getVoices();

var speech = new SpeechSynthesisUtterance();
speech.text = 'Hello Sir, How can I help you?';
speech.voice = voices[3];
speech.voiceURI = "Google UK English Male";
speech.volume = 1; // 0 to 1
speech.rate = 1; // 0.1 to 10
speech.pitch = 0; //0 to 2
speech.lang = 'en-GB';

function say_this(message){
    speech.text = message;
    window.speechSynthesis.speak(speech);
}

function mic_pressed() {
    $('.microphone').attr('src', mic_icon);
    recognition.start();
    $('.microphone-status').text('Listening...');
}

var pop_up = null;

function send_query(finalTranscript) {
    $.ajax(
    {
        type:"GET",
        url: "/fetch/",
        data: {'query': finalTranscript},
        success: function( data )
        {

            $('.microphone-status').text('Success!');
            setTimeout(function(){
                $('.microphone-status').text('Listening...');
            }, 3000);

            if(data.type == 'youtube'){
                say_this('Enjoy Sir!');

                if(pop_up != null){
                    pop_up.close();
                }
                pop_up = window.open(data.link, finalTranscript, "width=1280, height=720");
                if (window.focus) { pop_up.focus(); }
            }


        }
    });
}
