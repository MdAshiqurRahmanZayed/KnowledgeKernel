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


document.addEventListener("DOMContentLoaded", function () {
     // make it as accordion for smaller screens
     if (window.innerWidth < 992) {

          // close all inner dropdowns when parent is closed
          document.querySelectorAll('.navbar .dropdown').forEach(function (everydropdown) {
               everydropdown.addEventListener('hidden.bs.dropdown', function () {
                    // after dropdown is hidden, then find all submenus
                    this.querySelectorAll('.submenu').forEach(function (everysubmenu) {
                         // hide every submenu as well
                         everysubmenu.style.display = 'none';
                    });
               })
          });

          document.querySelectorAll('.dropdown-menu a').forEach(function (element) {
               element.addEventListener('click', function (e) {
                    let nextEl = this.nextElementSibling;
                    if (nextEl && nextEl.classList.contains('submenu')) {
                         // prevent opening link if link needs to open dropdown
                         e.preventDefault();
                         if (nextEl.style.display == 'block') {
                              nextEl.style.display = 'none';
                         } else {
                              nextEl.style.display = 'block';
                         }

                    }
               });
          })
     }
     // end if innerWidth
}); 
