const spinner = document.getElementById("spinner");
const codePin = document.getElementById('id_code_pin')
const countryInput = document.getElementById('id_country')
const receiverInput = document.getElementById('id_receiver')
const fromCurrencyLabel = document.querySelector('[for="id_amount"]').querySelector('span')
const toCurrencyLabel = document.querySelector('[for="id_amount_converted"]').querySelector('span')
const fromCurrencyInput = document.querySelector('#id_amount')
const toCurrencyInput = document.querySelector('#id_amount_converted')

const submitBtn = document.querySelector('#submit-btn')


countryInput.onchange = handleCountryOnChange 

fromCurrencyInput.onchange = handleChangeOnFromAmountInput
toCurrencyInput.onchange = handleChangeOnToAmountInput
codePin.onkeypress = typeOnlyDigits;

function typeOnlyDigits(e){
    if (e.which < 48 || e.which > 57) {
    e.preventDefault();
  }
}

function load_users(users){
    let usersFormats = `<option value=" ">Choose the receiver</option>`
    for(const user of users){
        usersFormats += `<option value="${user.username}">${user.first_name} ${user.last_name}</option>`

    }
    receiverInput.innerHTML = usersFormats 
}

function handleCountryOnChange(e){
    
    if(e.target.value === ' '){
        load_users([])
        toCurrencyLabel.innerHTML = ''
        return
    }
    e.preventDefault()
        spinner.removeAttribute('hidden');
        const country = e.target.value
        const url = '/users/'+country
        const method = 'POST'
        const csrftoken = getCookie('csrftoken')
        const xhr = new XMLHttpRequest()
        const responseType = 'json'
        xhr.responseType = responseType
        xhr.open(method, url)
        xhr.setRequestHeader('X-CSRFToken', csrftoken)
        xhr.onload =  function(){
            if(xhr.status === 200){
                // console.log(xhr.response.users)
                spinner.setAttribute('hidden', '');
                load_users(xhr.response.users)
                toCurrencyLabel.innerHTML = xhr.response.currency    
               
                    let to = toCurrencyLabel.innerText
                    let from = fromCurrencyLabel.innerText
                    let amount = fromCurrencyInput.value
                    convertAmount(to, from, amount,'from-to')
               
            } else if(xhr.status === 400){
                console.log(xhr.response)
            } else if(xhr.status === 404){
                console.log(xhr.response)
                toCurrencyLabel.innerHTML =''
            }else if (xhr.status === 500){
                alert('There was a server error, please try again.')
            }
        }
        xhr.onerror = function(){
            alert('An error occured, Please try again later.')
        }
        xhr.send()
}

function handleChangeOnFromAmountInput(e) {
    imposeMinMax(e.target)
   
    if (countryInput.value !== ''){
        let to = toCurrencyLabel.innerText
        let from = fromCurrencyLabel.innerText
        let amount = e.target.value 
        convertAmount(to, from, amount,'from-to')
    }
}

function handleChangeOnToAmountInput(e){
    if (countryInput.value !== ''){
        let from = toCurrencyLabel.innerText
        let to = fromCurrencyLabel.innerText
        let amount = e.target.value 
        convertAmount(to, from, amount,'to-from')
    }
}
function imposeMinMax(el){
    if(el.value != ""){
      if(parseInt(el.value) < parseInt(el.min)){
        el.value = el.min;
      }
      if(parseInt(el.value) > parseInt(el.max)){
        el.value = el.max;
      }
    }
  }
function convertAmount(to,from,amount, direction){
    // return 100
    if (to == '' || from == '') return
    var myHeaders = new Headers();
    myHeaders.append("apikey", "wS55XguJEzNOuWaCmBQ2sCLmLKtg2vge");
    
var requestOptions = {
  method: 'GET',
  redirect: 'follow',
  headers: myHeaders
};

spinner.removeAttribute('hidden')
submitBtn.disabled = true
fetch(`https://api.apilayer.com/exchangerates_data/convert?to=${to}&from=${from}&amount=${amount}`, requestOptions)
  .then(response => response.text())
  .then(result => {
    let data = JSON.parse(result)
    if(data?.success === true){
        data.result = Number(data.result).toFixed(2)
        if(direction === 'from-to'){
            toCurrencyInput.value = data.result
            spinner.setAttribute('hidden', '')
            submitBtn.disabled = false
        }
        else{
            fromCurrencyInput.value = data.result//to-from
        /*
                if the result is greater than the max of my account, let's us set fromInput to the max
                and recall convertAmount

        */
            if(parseInt(data.result) > fromCurrencyInput.max){
                imposeMinMax(fromCurrencyInput)
                let to = toCurrencyLabel.innerText
                let from = fromCurrencyLabel.innerText
                let amount = fromCurrencyInput.max
                convertAmount(to, from, amount,'from-to')

            }
        }
        spinner.setAttribute('hidden', '')
        submitBtn.disabled = false

    }
  })
  .catch(error => console.log('error', error));
}

function inputsAreNotBlank(){
    return (
        countryInput.value != ' ' && 
        fromCurrencyInput.value != '' && 
        toCurrencyInput.value != '' &&
        receiverInput.value != ' ' &&
        codePin.value != ''
    )
}
function handleTransactionFormDidSubmit(e){
        e.preventDefault()
        const myForm = e.target
        const myFormData = new FormData(myForm)
        const url = myForm.getAttribute('action')
        const method = myForm.getAttribute('method')
        if (inputsAreNotBlank()){

            const xhr = new XMLHttpRequest()
            const responseType = 'json'
        xhr.responseType = responseType
        xhr.open(method, url)
        xhr.onload =  function(){
            if(xhr.status === 201){
                // console.log(xhr.response)
                // myForm.reset()
                displayMessage('Transaction has been completed', 'success')
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
    }else{
        displayMessage('please fill all the fields','error')
    }
}
    const transacForm = document.getElementById('transac-form')
    transacForm.addEventListener('submit', handleTransactionFormDidSubmit)
