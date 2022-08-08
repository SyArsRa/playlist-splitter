const btns = document.getElementsByClassName('btnChoice');

Array.from(btns).forEach(btn => {
    btn.addEventListener('mouseover',function(event){
      btn.parentNode.parentNode.parentNode.className = "cards cardsHover";
    });
    btn.addEventListener('mouseout',function(event){
      btn.parentNode.parentNode.parentNode.className = "cards";
    });
})
