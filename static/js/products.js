let order = '';
let category = '';
let tags = [];
let page = 1;
let criteria = '';

$(document).ready(function() {
    let currentURL = $(location).attr('href');
    if (currentURL.includes('?criteria=')){
        url_split = currentURL.split('?criteria=')
        criteria = url_split[url_split.length - 1]
    }
})

/*
    this function checks whether the user has any orders already in the url
    and gets the url from the request made
*/
$(document).ready(function() {
    $('.order_select').on('change', function(e) {
        e.preventDefault();
        order = $('.order_select').val();
        let url = make_url()
        make_ajax_request(url)
    })
})

/*
    this function collects the inputted category set by the user
    and creates the url so all information is retained
*/
$(document).ready(function() {
    $('.category_select').on('change', function(e) {
        e.preventDefault();
        // page = $('.active-page').html();
        category = $('.category_select').val();
        let url = make_url()
        make_ajax_request(url)
    })
})


/*
    this function finds all tags already search for by the user
    and collects all the tags already search for and filters further
*/
$(document).ready(function() {
    $('.inactiveTag').on('click', function(e) {
        e.preventDefault();
        let tag_button = $(e.target)
        if (tag_button.attr('class') !== 'activeTag'){
            tag_button.attr('class', 'activeTag');
            tags.push($(e.target).children().html())
        } else {
            tag_button.attr('class', 'inactiveTag');
            let index = tags.indexOf($(e.target).children().html())
            if (index > -1) { tags.splice(index, 1)}
        }
        page = $('.active-page').html();
        let url = make_url()
        make_ajax_request(url)
    })
})

/*
    navigation keeper for the active elements in use
*/
$(document).ready(function() {
    make_page_nav_event_listener()
})

/*
    Function that creates the navigation for the site
*/
function make_page_nav_event_listener() {
    $('.page_nav_button').on('click', function(e) {
        if ($(e.target).attr('id') === 'next_page') {
            page += 1;
        }
        if ($(e.target).attr('id') === 'num_page') {
            page = $(e.target).html();
        }
        if ($(e.target).attr('id') === 'previous_page') {
            page -= 1;
        }
        let url = make_url()
        make_ajax_request(url)
    })
}

/*
    Function that creates custom URL for site with current attributes set
 */
function make_url() {
    let tag_url = ''
    for (let i = 0; i < tags.length; i++){
        tag_url += '&tags=' + tags[i] + '&'
    }
    return '/products?page=' + page + '&order=' + order + '&category=' + category + '&criteria=' + criteria + tag_url + '&json_response=True'
}


/*
    Create an Ajax request for the site
 */
function make_ajax_request(url) {
            $.ajax({
            url: url,
            type: 'GET',
            success: function(resp) {
                var newHtml = resp.products.map(product => {
                    return `<div class="categoryProductDiv">
                                <a href="/products/${product.id}">
                            
                                    <div class="categoryProductImageDiv">
                                        <img class="categoryProductImage" src="${product.image}" alt='image for ${product.name} missing'>
                                    </div>
                                    <h4>${product.name}</h4>
                                    <p>${product.short_description}</p>
                                    <h4 class="smallPriceTag">${product.price}??</h4>
                                    <p>${product.category}</p>
                                </a>
                            </div>`
                    });
                $('#category').html(newHtml.join(''));
                make_page_nav(resp.pages)
            }
        })
}

/*
    Function which navigates between sites
 */
function make_page_nav(pages){
    var newHtml = ``
    if (pages.has_other_pages) {
        // Prev page
        newHtml += `<ul class="paginator">`
        if (pages.has_previous) {
            newHtml += `<li><a class="page_nav_button" id="previous_page">&laquo;</a></li>`; // href="?page=${pages.previous_page_number}
        } else {
            newHtml += `<li class="disabled"><span>&laquo;</span></li>`;
        }
        // Every page number
        for (let i=1; i< (pages.num_of_pages + 1); i++){
            if (pages.number == i) {
              newHtml += `<li class="active"><span class="active-page">${i}</span></li>`
            } else {
                newHtml += `<li><a class="page_nav_button" id="num_page">${i}</a></li>`; // href="?page=${i}"
            }
        }
        // Prev page
        if (pages.has_next) {
            newHtml += `<li><a class="page_nav_button" id="next_page">&raquo;</a></li>` // href="?page=${pages.next_page_number}"
        } else {
            newHtml += `<li class="disabled"><span>&raquo;</span></li>`
        }
        newHtml += `</ul>`
    }
    newHtml += `<p>Showing ${pages.start_index}-${pages.end_index} of ${pages.page_count}</p>`
    $('.page_nav').html(newHtml);
    $('#num_of_products').html(`<p id="num_of_products">Number of products found: ${pages.page_count}</p>`)
    make_page_nav_event_listener()
}
