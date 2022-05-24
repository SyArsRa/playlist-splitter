const button = document.getElementById("Slice");

function inputcheck() {
  input = document.getElementById("playid");
  if (input != null) {
    if (input.value == undefined){
      button.disabled = true;
      console.log("h")
    } else {
      button.disabled = false;
      console.log("y")
    }
  }
}



button.addEventListener("mouseover",function(event){
  inputcheck()
  const div = document.getElementsByClassName("title");
  div[0].className = "titlehover";
})

button.addEventListener("mouseout",function(event){
  inputcheck()
  const div = document.getElementsByClassName("titlehover");
  div[0].className = "title";
})

button.addEventListener("click",function(event) {
  if (button.className.includes("pressed")) {
    document.getElementById("playid").submit();
  } else {
    var title = document.getElementsByClassName("titlecenter");
    title[0].className = "moveleft";
    title = document.getElementsByClassName("moveleft");
    title[0].ontransitionend = () => {
      button.className += " pressed";
      var form = document.createElement("form");
      form.setAttribute("method", "post");
      form.setAttribute("action", "");
      form.setAttribute("id", "playid");
      form.setAttribute("align", "center");
      form.setAttribute("style", "color:#28282B");
      form.setAttribute("class", "formcenter");
      var playlist = document.createElement("input");
      playlist.setAttribute("type", "text");
      playlist.setAttribute("name", "playid");
      playlist.setAttribute("placeholder", "Enter Playlist URL");
      form.appendChild(playlist);
      button.innerHTML = "Submit!";
      document.getElementById("ti").appendChild(form);
    }
  }
})
