function handleAccountCreateFormDidSubmit(event){
    event.preventDefault()
    const myForm = event.target
    const myFormData = new FormData(myForm)
    const url = myForm.getAttribute('action')
    const method = myForm.getAttribute('method')
    const csrftoken = getCookie('csrftoken')
    const xhr = new XMLHttpRequest()
    const responseType = 'json'
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.setRequestHeader('X-CSRFToken', csrftoken)
    xhr.onload =  function(){
        if(xhr.status === 200){
            // console.log(xhr.response)
            // myForm.reset()
            displayMessage('You have been authenticated', 'success')
            redirect(xhr.response.url)
        } else if(xhr.status === 400){
            const formErrors = getAllErrors(xhr.response.errors)
            displayMessage(formErrors[0], 'error')
        //    console.log(xhr.response)
               
           
        }else if (xhr.status === 500){
            alert('There was a server error, please try again.')
        }
    }
    xhr.onerror = function(){
        alert('An error occured, Please try again later.')
    }
    xhr.send(myFormData)
}
const signinForm = document.getElementById('signin-form')
signinForm.addEventListener('submit', handleAccountCreateFormDidSubmit)