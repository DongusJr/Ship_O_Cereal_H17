$('.btn-nav').click(function(e) {
    let cookies = document.cookie.split(";");
    for (let cookie in cookies){
        if (cookie === 'payment_done') {
            console.log("works!")
        }
    }
});