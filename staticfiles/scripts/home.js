
document.addEventListener("DOMContentLoaded", function () {
    var comments = document.getElementById('user-comments')
    var b = document.querySelector('.user-comment-elements')
    var c = document.getElementsByClassName('far fa-comments fa-2x');
    
    for (i = 0; i < c.length; i++) {
        c[i].addEventListener('click', function() {
            var user_comments = this.parentElement.parentElement.parentElement.parentElement.parentElement.nextSibling;
            if (user_comments.style.display == ''){
                user_comments.style.display = 'block';
            }
            else if (user_comments.style.display == 'block'){
                user_comments.style.display = '';
            }
        })
    }
    

   
    
            

       




})
