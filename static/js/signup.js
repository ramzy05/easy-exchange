
 function handleAccountCreateFormDidSubmit(event){
    event.preventDefault()
    const myForm = event.target
    const myFormData = new FormData(myForm)
    const url = myForm.getAttribute('action')
    const method = myForm.getAttribute('method')
    const xhr = new XMLHttpRequest()
    const responseType = 'json'
    xhr.responseType = responseType
    xhr.open(method, url)
    xhr.onload =  function(){
        if(xhr.status === 201){
            // console.log(xhr.response)
            displayMessage('Your account has been successfully created', 'success')
            // myForm.reset()
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
const signupForm = document.getElementById('signup-form')
signupForm.addEventListener('submit', handleAccountCreateFormDidSubmit)