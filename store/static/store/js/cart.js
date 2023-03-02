// console.log("hello world")

var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId : ', productId, 'action : ', action)
        console.log('user : ', user)
        if(user == 'AnonymousUser') {
            console.log('not logged in')
        } else {
            updateUserOrder(productId, action)
        }
        
    })
}

function updateUserOrder(productId, action) {
    console.log('user is logged in, sending data...')
    var url = '/update-item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
    },
        body: JSON.stringify({'productId':productId, 'action':action})
    }).then((response) => {
        // console.log('response', response)
        return response.json();
    }).then((data) => {
        location.reload()
        // console.log('data', data)
    })
}