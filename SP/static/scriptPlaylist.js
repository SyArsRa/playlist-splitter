const topIcon = document.getElementById("Top");

//Displays To Top button when the user scrolls

document.addEventListener("scroll", function(event){
  var pagePostion = window.scrollY;
  if ( pagePostion != 0 ){
    topIcon.className = "material-symbols-outlined";
    topIcon.textContent =  "arrow_upward";
  }
  else{
    topIcon.className = "";
    topIcon.textContent =  "";
  }
})

//Function that take user to top when the to top icon is clicked

topIcon.addEventListener("click", function(event){
  window.scrollTo({ top: 0, behavior: 'smooth' });
})
