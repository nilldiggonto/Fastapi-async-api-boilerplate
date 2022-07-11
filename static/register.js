function registerForm(e){
    e.preventDefault();
    let email = document.getElementById('email').value;
    let phone = document.getElementById('phone').value;
    let password = document.getElementById('password').value;
    let password2 =document.getElementById('password2').value ;
    let sendData = JSON.stringify({"email": email,"password":password,"confirm_password": password2,"phone_no":phone});
    let requestOptions = postRequestOptions
    requestOptions.body = sendData
    fetch("/user/signup", requestOptions)
    .then(response => response.json())
    .then(result=>{
        if (result['alert'] == 'register'){
            document.getElementById('alert').innerHTML = `
            <div class="alert alert-success text-center alert-dismissable notification is-toast">
            <strong>REGISTER SUCCESSFULL </strong>
          </div>
            `
        }else if (result['alert'] == 'email'){
            document.getElementById('alert').innerHTML = `
            <div class="alert alert-danger text-center alert-dismissable notification is-toast">
            <strong>ACCOUNT EXISTS</strong>
          </div>
            ` 
        }else if (result['alert'] == 'password'){
            document.getElementById('alert').innerHTML = `
            <div class="alert alert-danger text-center alert-dismissable notification is-toast">
            <strong>PASSWORD MISMATCH</strong>
          </div>
            ` 
        }
    })
    .catch(error => console.log('error', error));

}