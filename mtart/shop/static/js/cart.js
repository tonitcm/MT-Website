
var updateBtns = document.getElementsByClassName('update-cart') //getting buttons// 

//for loop, loop through buttons lengths and each iteration//
//functions executes on each click//
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){ 
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:',action)  //updating buttons//

//changing the behaviour of what happens depending on the user thats logged in: anonymous or authenticated//

        console.log('USER:', user)
        if(user == 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item/'

//fetch api post request, 

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })

//get the response 

    .then((response) => {
        return response.json()
    })

//console the data    

    .then((data) => {
        console.log('data:', data) //getting the data from views update_item
        location.reload() //reload the page
    })
}


    
