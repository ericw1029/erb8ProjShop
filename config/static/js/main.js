const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();


setTimeout(() => {
    console.log('setTimeout')
    $("#message").fadeOut("slow");
    // document.querySelector('#message').style.visibility = "hidden"
},3000)