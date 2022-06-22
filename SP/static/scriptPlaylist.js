const topIcon = document.getElementById("Top");
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
