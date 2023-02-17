/* player */

var player;
var video_list
document.onreadystatechange = function () {
     // console.log(document.readyState);
     if (document.readyState == 'interactive') {
          player = document.getElementById("player")
          video_list = document.getElementById("video_list")
          
          maintainRatio()
     }
}

function maintainRatio() {
     var w = player.clientWidth
     var h = (w * 9) / 16
     // console.log({
     //      w,
     //      h
     // });
     player.height = h
     video_list.style.maxHeight = h + "px"
}
window.onresize = maintainRatio

function toogleSelection(id) {
     document.getElementById(id).classList.toggle('collapsed');
}

// jquery end

setTimeout(function () {
     $('#message').fadeOut('slow')
}, 4000)



// Not required
function removeElement(element) {
     element.remove();
}



var navbar = document.querySelector('.navbar');
var threshold = 200;

window.addEventListener('scroll', function () {
     if (window.scrollY >= threshold) {
          navbar.classList.add('scrolled');
     } else {
          navbar.classList.remove('scrolled');
     }
});