async function sendMessage(){

let input = document.getElementById("message");
let chat = document.getElementById("chat");

let msg = input.value;

chat.innerHTML += "<p>You: "+msg+"</p>";

let res = await fetch("http://127.0.0.1:8000/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
});

let data = await res.json();

chat.innerHTML += "<p>AI: "+data.response+"</p>";

input.value="";
}