//Creating a constant variables
const div = document.getElementById("topContainer");
const button = document.getElementById("Slice");

//Mouse hover listner to check for mouse hovering over the button to change colorContainer class element to colorContainerHover

button.addEventListener("mouseover",function(event){
  div.className = "colorContainerHover";
})

//Mouse out listner to listen to mouse moving away from the button to change the class of colorContainerHover class to colorContainer

button.addEventListener("mouseout",function(event){
  div.className = "colorContainer";
})

//Button Click Listner to listen for click of the slice button
button.addEventListener("click",function(event) {
  var title = document.getElementsByClassName("title");
  title[0].className = "moveleft";
  title = document.getElementsByClassName("moveleft");
  title[0].ontransitionend = () => {
  var form = document.createElement("form");
  form.setAttribute("method", "post");
  form.setAttribute("align", "center");
  form.setAttribute("style", "color:#28282B");
  form.setAttribute("class", "formcenter");
  form.setAttribute("id","playlistForm");
  form.setAttribute("action","/authorization/");
  document.getElementById("topContainer").appendChild(form);
  document.getElementById("playlistForm").submit();
    }
  })

/*
event listner which checks for the the form input field being empty or not and if empty disables the button, works only after the button
has been pressed once

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
*/
