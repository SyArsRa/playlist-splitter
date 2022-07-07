//Creating a constant variable to store slice button

const button = document.getElementById("Slice");

//Mouse hover listner to check for mouse hovering over the button to change title class element to titlehover

button.addEventListener("mouseover",function(event){
  const div = document.getElementsByClassName("title");
  div[0].className = "titlehover";
})

//Mouse out listner to listen to mouse moving away from the button to change the class of titlehover class to title

button.addEventListener("mouseout",function(event){
  const div = document.getElementsByClassName("titlehover");
  div[0].className = "title";
})

//Button Click Listner to listen for click of the slice button
button.addEventListener("click",function(event) {
  //if statment to check if the button has been presssed already
  if (button.className.includes("pressed")) {
    //submit the form if the button is been pressed for the second time
    document.getElementById("playlistForm").submit();
  } else {
    //creating a form  and input field for when the button is pressed for the first time
    var title = document.getElementsByClassName("titlecenter");
    title[0].className = "moveleft";
    title = document.getElementsByClassName("moveleft");
    title[0].ontransitionend = () => {
      button.className += " pressed";
      var form = document.createElement("form");
      form.setAttribute("method", "post");
      form.setAttribute("align", "center");
      form.setAttribute("style", "color:#28282B");
      form.setAttribute("class", "formcenter");
      form.setAttribute("id","playlistForm");
      form.setAttribute("action","/SP/playlist/");
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

/*
event listner which checks for the the form input field being empty or not and if empty disables the button, works only after the button
has been pressed once
*/
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
