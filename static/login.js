function loginForm(e){
    e.preventDefault();
    let email = document.getElementById('email').value;
    let password = document.getElementById('password').value;
    let sendData = JSON.stringify({"email": email,"password":password});
    let requestOptions = postRequestOptions
    requestOptions.body = sendData
    fetch("/user/login", requestOptions)
    .then(response => response.json())
    .then(result=>{
        if (result['alert'] == 'success'){
            document.getElementById('alert').innerHTML = `
            <div class="alert alert-success text-center alert-dismissable notification is-toast">
            <strong>LOGIN SUCCESSFULL </strong>
          </div>
            `
        }else if (result['alert'] == 'invalid'){
            document.getElementById('alert').innerHTML = `
            <div class="alert alert-danger text-center alert-dismissable notification is-toast">
            <strong>ACCOUNT NOT FOUND</strong>
          </div>
            ` 
        }
    })
    .catch(error => console.log('error', error));

}