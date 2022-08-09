const btns = document.getElementsByClassName('btnChoice');
const card = document.getElementById("linkCard")

Array.from(btns).forEach(btn => {
    btn.addEventListener('mouseover',function(event){
      btn.parentNode.parentNode.parentNode.className = "cards cardsHover";
    });
    btn.addEventListener('mouseout',function(event){
      btn.parentNode.parentNode.parentNode.className = "cards";
    });
})

/*
event listner which checks for the the form input field being empty or not and if empty disables the button
*/
card.addEventListener("mouseover", function(){
  input = document.getElementById("playId");
  if (input != null) {
    if (input.value.trim().length == 0 ){
      btns[0].disabled = true;
    } else {
      btns[0].disabled = false;
    }
  }
})
