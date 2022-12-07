const userNameField = document.querySelector('#userNameField')
const uNfeedbackField = document.querySelector('#uNfeedbackField')
const emailField = document.querySelector('#emailField')
const eMfeedbackField = document.querySelector('#eMfeedbackField')
const userNameSuccessOutput = document.querySelector('.userNameSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')

// submitBtn.addEventListener('')

showPasswordToggle.addEventListener('click',(e)=>{
    if(showPasswordToggle.textContent === "SHOW"){
        showPasswordToggle.textContent = "HIDE"
        passwordField.setAttribute("type","text")
    }else{
        showPasswordToggle.textContent = "SHOW"
        passwordField.setAttribute("type","password")
    }
})
emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value;
    console.log('emailVal',emailVal)

    emailField.classList.remove("is-invalid")
    eMfeedbackField.style.display='none';

    if(emailVal.length >0){
        fetch("/authentication/validate-email",{
            body: JSON.stringify({email: emailVal}),
            method:"POST",
        })
        .then((res) => res.json())
        .then((data) =>{
            if(data.email_error){
                submitBtn.disabled = true;
                emailField.classList.add("is-invalid")
                eMfeedbackField.style.display='block';
                eMfeedbackField.innerHTML=`<p>${data.email_error}</p>`
            }else{
                submitBtn.removeAttribute('disabled');
            }  
        })
    }

})

userNameField.addEventListener('keyup',(e)=>{
    
    const userNameVal = e.target.value;
    userNameSuccessOutput.style.display ="block"
    userNameSuccessOutput.textContent =`Checking ${userNameVal}`
    userNameField.classList.remove("is-invalid")
    uNfeedbackField.style.display='none';

    if(userNameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({userName : userNameVal}), 
            method:"POST",
        })
        .then((res) => res.json())
        .then((data) =>{
            userNameSuccessOutput.style.display ="none"
            if(data.username_error){
                submitBtn.disabled = true;
                userNameField.classList.add("is-invalid")
                uNfeedbackField.style.display='block';
                uNfeedbackField.innerHTML=`<p>${data.username_error}</p>`
            }else{
                submitBtn.removeAttribute('disabled');
            }  
        }
        );
    }
});