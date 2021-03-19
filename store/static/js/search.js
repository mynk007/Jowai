// search functionality



// document.getElementById("search_btn").addEventListener('click',function(e){
//     location.href="/"
// })

search=document.getElementById("searchtxt")
search.addEventListener('input',function(e){

    var inputVal=search.value.toLowerCase();
    var post=document.getElementsByClassName('post')
    Array.from(post).forEach(function(element){
        names=element.getElementsByTagName('strong')[0].innerText
        if(names.toLowerCase().includes(inputVal)){
            element.style.display="block"
        }
        else{
            element.style.display="none"
        }
    })
})