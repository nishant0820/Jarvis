$(document).ready(function (){
    eel.init()()

    $('.text').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });
    
    // Siri configuration
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "1",
        speed: "0.30",
        autostart: true
      });

      $('.siri-message').textillate({
        loop: true,
        sync: true,
        in:{
            effect: "bounceIn",
        },
        out:{
            effect: "bounceOut",
        },
    });

    // Mic button click event
    $("#MicBtn").click(function (){
        eel.playAssistantSound()
        $("#Oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands()()
    });

    // Shorcut Key win+j
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey){
            eel.playAssistantSound()
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands()()
        }
    }
    document.addEventListener('keyup', doc_keyUp, false);

    // To play assisatnt 
    function PlayAssistant(message){
        if (message != "") {
            $("#Oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands(message);
            $("#chatbox").val("")
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // Toggle fucntion to hide and display mic and send button 
    function ShowHideButton(message){
        if (message.length == 0) {
            $("#MicBtn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
        else {
            $("#MicBtn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
        }
    }

    // Key up event handler on text box
    $("#chatbox").keyup(function (){
        let message = $("#chatbox").val();
        ShowHideButton(message)
    });
    
    // Send button event handler
    $("#SendBtn").click(function (){
        let message = $("#chatbox").val()
        PlayAssistant(message)
    });

    // Enter press event handler on chat box
    $("#chatbox").keypress(function (e){
        key = e.which;
        if (key == 13) {
            let message = $("#chatbox").val()
            PlayAssistant(message)
        }
    });

});