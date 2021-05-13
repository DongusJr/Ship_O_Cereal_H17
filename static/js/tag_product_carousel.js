$.ajax({
    url: '/get_tags_json',
    type: 'GET',
    success: function(resp) {

        var newHtml = resp.data.map(d => {

            let text = `<div class="tag_name">
                            <a href="/products?tag=${d.name}"><h1>${d.name}</h1></a>
                       </div>
                        <div class="tag_div inner-carousel">
                        <div class="track">`
            for (let product in d.products) {
                text += `<div class="landingProductDiv card-container">
                            <a href="/products/${d.products[product].id}">
                        
                                <div class="landingProductImageDiv">
                                <img src="${d.products[product].image}" alt='image for ${d.products[product].name} missing' class="landingProductImage">
                                </div>
                        
                                <h4>${d.products[product].name}</h4>
                                <p>${d.products[product].short_description}</p>
                                <h3 class="smallPriceTag">${d.products[product].price}£</h3>
                                <p>${d.products[product].category}</p>
                            </a>
                        </div>`
            }
            text += `</div>
                    </div>
                     <div class="carousel-nav">
                    <button class="arrow-btn prev"><i class="fas fa-arrow-left fa-2x"><</i></button>
                    <button class="arrow-btn next"><i class="fas fa-arrow-right fa-2x">></i></button>
                     </div>`
            return text
        });
        $('.tags_with_products').html(newHtml.join(''));
        make_event_listeners_for_next_prev(document)
        },
    error: function(xhr, status, error) {
        console.error(errors)
    }
})

function make_event_listeners_for_next_prev(document) {
    const prev_list = document.getElementsByClassName("prev");
    const next_list = document.getElementsByClassName("next");
    console.log(next_list)
    const carousel = document.querySelector(".carousel-container");
    const track_list = document.getElementsByClassName("track");
    for (let i = 0; i < prev_list.length; i++) {
        let width = carousel.offsetWidth;
        let index = 0;
        let next = next_list[i];
        let prev = prev_list[i];
        let track = track_list[i];
        window.addEventListener("resize", function () {
            width = carousel.offsetWidth;
        });
        next.addEventListener("click", function (e) {
            e.preventDefault();
            index = index + 1;
            prev.classList.add("show");
            track.style.transform = "translateX(" + index * -width + "px)";
            if (track.offsetWidth - index * width < index * width) {
                next.classList.add("hide");
            }
        });
        prev.addEventListener("click", function () {
            index = index - 1;
            next.classList.remove("hide");
            if (index === 0) {
                prev.classList.remove("show");
            }
            track.style.transform = "translateX(" + index * -width + "px)";
        });
    }
}
