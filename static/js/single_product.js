$(document).ready(function() {
    $('.singleProductImage').on('click', function(e) {
        e.preventDefault();
        let image = $(e.target).attr('src');
        console.log(image);
        $('#largeProductImagePicture').attr('src', image);
    })
})