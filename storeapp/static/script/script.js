/*
  BloomShop front-end demo.
  Cart buttons and the cart badge are static for Django integration later.
*/

document.addEventListener("DOMContentLoaded", function () {
    setupProductSearch();
    setupAuthForms();
});

// Handle the storefront's demo auth forms without sending credentials anywhere.
function setupAuthForms() {
    var signInForm = document.getElementById("sign-in-form");
    var signUpForm = document.getElementById("sign-up-form");
    var passwordToggles = document.querySelectorAll("[data-toggle-password]");

    for (var i = 0; i < passwordToggles.length; i++) {
        (function (toggle) {
            var passwordInput = document.getElementById(toggle.getAttribute("data-toggle-password"));
            var reveal = function () {
                passwordInput.type = "text";
                toggle.setAttribute("aria-pressed", "true");
            };
            var conceal = function () {
                passwordInput.type = "password";
                toggle.setAttribute("aria-pressed", "false");
            };

            toggle.addEventListener("mouseenter", reveal);
            toggle.addEventListener("mouseleave", conceal);
            toggle.addEventListener("focus", reveal);
            toggle.addEventListener("blur", conceal);
            toggle.addEventListener("touchstart", reveal, { passive: true });
            toggle.addEventListener("touchend", conceal);
            toggle.addEventListener("touchcancel", conceal);
        })(passwordToggles[i]);
    }
    if (signInForm !== null) {
        signInForm.addEventListener("submit", function (event) {
            event.preventDefault();
            showAuthFeedback("Sign-in is ready to connect to an account service.", false);
        });
    }

    if (signUpForm !== null) {
        signUpForm.addEventListener("submit", function (event) {
            event.preventDefault();
            var password = document.getElementById("signup-password").value;
            var confirmation = document.getElementById("signup-confirm").value;

            if (password !== confirmation) {
                showAuthFeedback("Those passwords do not match. Please try again.", true);
                document.getElementById("signup-confirm").focus();
                return;
            }

            showAuthFeedback("Your details are ready. Account creation is not connected in this demo.", false);
        });
    }
}

function showAuthFeedback(message, isError) {
    var feedback = document.getElementById("auth-feedback");

    if (feedback === null) return;
    feedback.textContent = message;
    feedback.classList.toggle("is-error", isError);
}

// Filter the product cards while the customer types in the search box.
function setupProductSearch() {
    var searchInput = document.querySelector('input[type="search"]');
    var productCards = document.querySelectorAll(".product-card");

    if (searchInput === null || productCards.length === 0) {
        return;
    }

    searchInput.addEventListener("input", function () {
        var searchText = searchInput.value.toLowerCase();

        for (var i = 0; i < productCards.length; i++) {
            var productName = productCards[i].querySelector(".product-title").textContent.toLowerCase();
            productCards[i].parentElement.hidden = !productName.includes(searchText);
        }
    });
}

// This is a demo form: it shows a message but does not send data to a server.
function setupContactForm() {
    var contactForm = document.getElementById("contact-form");

    if (contactForm === null) {
        return;
    }

    contactForm.addEventListener("submit", function (event) {
        event.preventDefault();
        document.getElementById("contact-feedback").textContent =
            "Thanks! This demo form is not connected to a server.";
        contactForm.reset();
    });
}



//  FETCH WORKINGS ARE HERE

function check(e,product_id,action){
    e.preventDefault()
    let datas=document.getElementsByName('csrfmiddlewaretoken')[0].value
    let details={id:product_id,action:action}
    console.log("check Function is called");
    

    fetch("/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":datas
        },
        body:JSON.stringify(details)
    }).then(response => response.json())
    .then(data => {
        document.getElementById('cart_count').innerHTML=data.count
          
    })
   
    
}





function removes(e,cart_id){
    e.preventDefault()
    let csrf=document.getElementsByName('csrfmiddlewaretoken')[0].value
    let details={id:cart_id}
    console.log("remove function called");
    fetch("http://127.0.0.1:8000/store/cart/",{
        method:"POST",
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrf
        },
        body:JSON.stringify(details)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('cart-'+ cart_id ).remove()
        if(data.empty){
            document.getElementById('empty_cart').hidden=false
        }
        document.getElementById('total').innerHTML=data.total
        document.getElementById('cart_count').innerHTML=data.count
    })
   
    
}


