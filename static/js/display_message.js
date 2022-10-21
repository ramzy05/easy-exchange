function getAllErrors(mixedErrors) {
    let keys = Object.keys(mixedErrors)
    let errors = []
    for (const key of keys) {
        for (const error of mixedErrors[key]){
            errors = errors.concat([error.message])
        }
    }
    return  errors
}

function displayMessage(message,type){
    const messageBox = document.getElementById('message-box')
    messageBox.classList.add(type)
    messageBox.classList.add('show')
    messageBox.querySelector('p').innerText = message
    = message
    setTimeout(() => {
        messageBox.className = ''
        messageBox.classList.remove(type)
        messageBox.classList.remove('show')
        messageBox.querySelector('p').innerText = ''
    }, 1500)
  }
