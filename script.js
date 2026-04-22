function sendMessage(){
  let input = document.getElementById("message");
  let chat = document.getElementById("chat");
  let msg = input.value.trim();
  if(msg === "") return;
  chat.innerHTML += "<p><b>You:</b> " + msg + "</p>";
  fetch("http://127.0.0.1:8000/chat",{
  method:"POST",
  headers:{
    "Content-Type":"application/json"
  },
  body:JSON.stringify({message:msg})
})
  .then(res => res.json())
  .then(data => {
    chat.innerHTML += "<p><b>AI:</b> " + data.response + "</p>";
    chat.scrollTop = chat.scrollHeight;
})

.catch(err => {
    chat.innerHTML += "<p>Error connecting to server</p>";
});
});
input.value="";
}
