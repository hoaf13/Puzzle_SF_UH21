//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext //audio context to help us record

var recordButton = document.getElementById("record-button");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);

function startRecording() {
	console.log("recordButton clicked");
  console.log(recordButton.value);
  if (recordButton.value != "recording"){

    /*
      Simple constraints object, for more advanced audio features see
      https://addpipe.com/blog/audio-constraints-getusermedia/
    */
      
      var constraints = { audio: true, video:false }

    /*
        Disable the record button until we get a success or fail from getUserMedia() 
    */
    navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
      console.log("getUserMedia() success, stream created, initializing Recorder.js ...");

      /*
        create an audio context after getUserMedia is called
        sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
        the sampleRate defaults to the one set in your OS for your playback device

      */
      console.log("test");
      audioContext = new AudioContext();
      
      //update the format 
      /*  assign to gumStream for later use  */
      gumStream = stream;
      
      /* use the stream */
      input = audioContext.createMediaStreamSource(stream);

      /* 
        Create the Recorder object and configure to record mono sound (1 channel)
        Recording 2 channels  will double the file size
      */
      
      rec = new Recorder(input,{numChannels:1})

      //start the recording process
      rec.record()

      console.log("Recording started");

    }).catch(function(err) {
        //enable the record button if getUserMedia() fails
    });
    recordButton.value = "recording";
  }
  else{
    console.log("Stop recording");
    recordButton.value = "stop-recording";
    stopRecording();
  }
}
function stopRecording() {
	console.log("stopButton clicked");

	rec.stop();

	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//create the wav blob and pass it on to createDownloadLink
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	console.log("creating link")
	var url = URL.createObjectURL(blob);
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//name of .wav file to use during upload and download (without extendion)
	var filename = new Date().toISOString();

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//save to disk link
	link.href = url;
	link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
	
	//upload link
	console.log(blob);
    var xhttp = new XMLHttpRequest();

    xhttp.open("POST", "http://127.0.0.1:8000/apis/v1/save_record/", true);
    var data = new FormData();
    data.append('data', blob, 'audio_blob');
  //   var post_data = {
  
  //     'csrfmiddlewaretoken':"{{ csrf_token }}",
  //       "data": data,
  //   }
  //   $.ajax({
  //     url : "http://127.0.0.1:8000/apis/v1/save_record/",
  //     type: 'POST',
  //     dataType: 'json',
  //     data: post_data,
  //     cache : false,
  //     processData: false
  // }).done(function(response) {
  //     alert(response);
  // });
    // console.log(post_data);
    console.log(this.readyState);
    xhttp.send(data);
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);     
         }
    };
    
	//add the li element to the ol
}

// recording animation
$('#record-button').addClass("notRec");

$('#record-button').click(function(){
	if($('#record-button').hasClass('notRec')){
		$('#record-button').removeClass("notRec");
		$('#record-button').addClass("Rec");
	}
	else{
		$('#record-button').removeClass("Rec");
		$('#record-button').addClass("notRec");
	}
});	