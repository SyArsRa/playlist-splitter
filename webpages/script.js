const button = document.getElementById("Slice");

button.addEventListener("mouseover",function(event){
  const div = document.getElementsByClassName("title");
  div[0].className = "titlehover";
})

button.addEventListener("mouseout",function(event){
  const div = document.getElementsByClassName("titlehover");
  div[0].className = "title";
})

button.addEventListener("click",function(event) {
  if (button.className.includes("pressed")) {
    document.getElementById("playlistForm").submit();
  } else {
    var title = document.getElementsByClassName("titlecenter");
    title[0].className = "moveleft";
    title = document.getElementsByClassName("moveleft");
    title[0].ontransitionend = () => {
      button.className += " pressed";
      var form = document.createElement("form");
      form.setAttribute("method", "post");
      form.setAttribute("action", "");
      form.setAttribute("align", "center");
      form.setAttribute("style", "color:#28282B");
      form.setAttribute("class", "formcenter");
      form.setAttribute("id","playlistForm")
      var playlist = document.createElement("input");
      playlist.setAttribute("type", "text");
      playlist.setAttribute("name", "playlistId");
      playlist.setAttribute("id", "playid")
      playlist.setAttribute("placeholder", "Enter Playlist URL");
      form.appendChild(playlist);
      button.innerHTML = "Submit!";
      document.getElementById("ti").appendChild(form);
    }
  }
})

document.getElementById("hoverbtn").addEventListener("mouseover", function(){
  input = document.getElementById("playid");
  if (input != null) {
    if (input.value.trim().length == 0 ){
      button.disabled = true;
    } else {
      button.disabled = false;
    }
  }
})
