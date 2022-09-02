
const codePinToggle = document.getElementById('code-pin-toggle')
const codePinBox = document.getElementById('code-pin')
const codePin = codePinBox.dataset.code
codePinToggle.onclick = function(){
    if(codePinToggle.classList.contains('show')){
        codePinToggle.classList.remove('show')
        codePinBox.innerText = '* * * *'
    }else{
        codePinToggle.classList.add('show')
        codePinBox.innerText = `${codePin[0]} ${codePin[1]} ${codePin[2]} ${codePin[3]}`
    }
}
