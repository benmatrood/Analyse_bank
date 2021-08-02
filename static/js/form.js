document.getElementById('postForm').addEventListener('submit',getData);
function getData(e){
    e.preventDefault();
    var input1 = document.getElementById('input1').value;
    var input2 = document.getElementById('input2').value;
    var input3 = document.getElementById('input3').value;
    var input4 = document.getElementById('input4').value;
    var input5 = document.getElementById('input5').value;
    var input6 = document.getElementById('input6').value;
    var input7 = document.getElementById('input7').value;
    var input8 = document.getElementById('input8').value;

    var params = {user_input1:input1,
                    user_input2:input2,
                    user_input3:input3,
                    user_input4:input4,
                    user_input5:input5,
                    user_input6:input6,
                    user_input7:input7,
                    user_input8:input8 }
    

    var xhr = new XMLHttpRequest();
    xhr.open('post', '../output', true);
    xhr.setRequestHeader('Content-Type', 'application/json'),

    xhr.onload = function() {
        console.log('Reached');
        document.getElementById('prediction').innerHTML = this.responseText;
    }
    xhr.send(JSON.stringify(params));
}


