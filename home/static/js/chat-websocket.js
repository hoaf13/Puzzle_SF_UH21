// CHATBOT WEBSOCKET 

const chatSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/'
);

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

window.onload = function(){
  $("#chat-circle").click();
  $("#chat-input").focus();
}

$(function() {
    var INDEX = 0; 
    var emojis = [0x1F600, 0x1F604, 0x1F34A, 0x1F344, 0x1F37F, 0x1F363, 0x1F370, 0x1F355, 0x1F354, 0x1F35F, 0x1F6C0, 0x1F48E, 0x1F5FA, 0x23F0, 0x1F579, 0x1F4DA, 0x1F431, 0x1F42A, 0x1F439, 0x1F424];    
    $("#chat-submit").click(function(e) {
      e.preventDefault();
      var msg = $("#chat-input").val(); 
      if(msg.trim() == ''){
        return false;
      }
      const message = msg;
      chatSocket.send(JSON.stringify({
          'message': message
      }));
      generate_message(msg, 'self');
      var buttons = [
          {
            name: 'Existing User',
            value: 'existing'
          },
          {
            name: 'New User',
            value: 'new'
          }
        ]; 
      chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        generate_message(data.message, 'user');                  
      };   
    })
    
    $("#chat-input").keypress(function (event) {
        if (event.which === 13 || event.keyCode === 13 || event.key === "Enter") {
            $("#chat-submit").click()
            event.preventDefault();
        }
    });

    function generate_message(msg, type) {
      INDEX++;
      var str="";
      str += "<div id='cm-msg"+INDEX+"' class=\"chat-msg "+type+"\">";
      str += "        <\/span>";
      str += "          <div class=\"cm-msg-text\">";
      str += msg;
      str += "          <\/div>";
      str += "        <\/div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);
      if(type == 'self'){
       $("#chat-input").val(''); 
      }    
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);    
    }  
    
    function generate_button_message(msg, buttons){    
      INDEX++;
      var btn_obj = buttons.map(function(button) {
         return  "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\""+button.value+"\">"+button.name+"<\/a><\/li>";
      }).join('');
      var str="";
      str += "<div id='cm-msg-"+INDEX+"' class=\"chat-msg user\">";
      str += "        <\/span>";
      str += "          <div class=\"cm-msg-text\">";
      str += msg;
      str += "          <\/div>";
      str += "          <div class=\"cm-msg-button\">";
      str += "            <ul>";   
      str += btn_obj;
      str += "            <\/ul>";
      str += "          <\/div>";
      str += "        <\/div>";
      $(".chat-logs").append(str);
      $("#cm-msg-"+INDEX).hide().fadeIn(300);   
      $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight}, 1000);
      $("#chat-input").attr("disabled", true);
    }
    
    $(document).delegate(".chat-btn", "click", function() {
      var value = $(this).attr("chat-value");
      var name = $(this).html();
      $("#chat-input").attr("disabled", false);
      generate_message(name, 'self');
    })
    
    $("#chat-circle").click(function() {    
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
      $("#chat-input").focus();
    })
    
    $(".chat-box-header").click(function() {
      $("#chat-circle").toggle('scale');
      $(".chat-box").toggle('scale');
    })
    
  })