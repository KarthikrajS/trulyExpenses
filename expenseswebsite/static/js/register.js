const userNameField = document.querySelector('#userNameField')

userNameField.addEventListener('keyup',(e)=>{
    
    const userNameVal = e.target.value;
    console.log('userNameVal',userNameVal)
    if(userNameVal.length > 0){
        fetch("/authentication/validate-username",{
            body:JSON.stringify({userName : userNameVal}), 
            method:"POST",
        })
        .then((res) => res.json())
        .then((data) =>
            console.log('data', data)
        );
    }
});