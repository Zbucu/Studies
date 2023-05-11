
// localStorage.clear();
showTODO();
min_date();
document.getElementById('Submit').addEventListener("click", function() {
    
    var input_c = document.getElementById('content').value;
    if (input_c.length<3 || input_c.length>255)
    {

    }
    else
    {
    var input_d = document.getElementById('date').value;
    const tab = [input_c, input_d];
    var max = -1;
    for(var i = 0; i<localStorage.length; i++)
    {

        console.log(Number(JSON.parse(localStorage.key(i))));
        if (Number(localStorage.key(i)) > max)
        {
            max = Number(localStorage.key(i));
        }
    }
    window.localStorage.setItem(max+1, JSON.stringify(tab));
    document.getElementById('content').value="";
    document.getElementById('date').value="";
    // window.localStorage.setItem('date', input_d);
    
    document.querySelector('#lista').innerHTML = "";
        showTODO();
    // updateTODO();
}
});

document.getElementById('searchbar').addEventListener("input", function() {
    var a = document.getElementById('searchbar').value.length;
    if(a>=3)
    {
        find(document.getElementById('searchbar').value);
    }
    else
    {
        document.querySelector('#lista').innerHTML = "";
        showTODO();
    }
});



function add_delete_buttons(reg) {
    var reg=reg;
    var few_buttons = document.getElementsByClassName('del');
    const tab = [];
    for(var i = 0; i < few_buttons.length; i++) {
        (function(index) {
            tab.push(few_buttons[index].id);
            few_buttons[index].addEventListener("click", function() {
             delete_task(few_buttons[index], tab, reg);
           })
          })(i);
      }
}

function delete_task(task_button, tab, reg) {
    var ind = tab.indexOf(task_button.id);
if (ind !== -1) {
  tab.splice(ind, 1);
}
    localStorage.removeItem(task_button.id);
    document.querySelector('#lista').innerHTML = "";
    show_after_del(tab, reg);

}

function find(input) {
    var reg = new RegExp(input);
    document.querySelector('#lista').innerHTML = "";
    for (var i = 0; i<localStorage.length;i++)
    {
        // console.log(JSON.parse(localStorage.getItem(localStorage.key(i)))[0]);
        if(reg.test(JSON.parse(localStorage.getItem(localStorage.key(i)))[0]))
        {
            show_a(localStorage.key(i), reg, input);
        }
        else
        {
        }
    }
    add_delete_buttons(reg);

}

function show_a(key_curr, reg, input){
    var list = document.getElementById('lista');
    

    var item = document.createElement("li");
    item.className = "tasks";
    var i1 = document.createElement("h3");  
    i1.id = "task_name";
    i1.textContent = JSON.parse(localStorage.getItem(key_curr))[0];
    var rep = JSON.parse(localStorage.getItem(key_curr))[0].match(reg);
    i1.innerHTML = i1.innerHTML.replace(reg, "<mark>" + rep + "</mark>");
    var i2 = document.createElement("p");
    i2.textContent = JSON.parse(localStorage.getItem(key_curr))[1];
    var i3 = document.createElement("button");
    i3.innerHTML = 'Delete';
    i3.className = "del";
    i3.id = key_curr;
    item.appendChild(i1);
    item.appendChild(i2);
    item.appendChild(i3);
    list.prepend(item);

    var task_tab = document.getElementsByClassName("tasks");
for(var i = 0; i < task_tab.length; i++) {
    (function(index) {
        task_tab[index].firstChild.addEventListener("click", function() {
        task_tab[index].firstChild.setAttribute("contenteditable", true); 
       })
        task_tab[index].firstChild.addEventListener("blur", function(){

        var klucz = task_tab[index].lastChild.id;
        var zmiana = task_tab[index].firstChild.innerText;
        var tab = JSON.parse(localStorage.getItem(klucz));
        tab[0]=zmiana;
        localStorage.setItem(klucz, JSON.stringify(tab));
        find(input);
       })
      })(i);
  }

}


function showTODO() {
    var list = document.getElementById('lista');
    var max = Number.MAX_VALUE;
    var max_2 = -1;
    for(var j = 0; j<localStorage.length; j++){
    for(var i = 0; i<localStorage.length; i++){
        var klucz = Number(localStorage.key(i));
        if(klucz>max_2 && klucz<max)
        {
            max_2 = klucz;
        }
    }
    max = max_2;
    max_2 = -1;

    var item = document.createElement("li");
    item.className = "tasks";
    var i1 = document.createElement("h3");
    i1.textContent = JSON.parse(localStorage.getItem(max))[0];
    i1.id = "task_name";
    var i2 = document.createElement("p");
    i2.textContent = JSON.parse(localStorage.getItem(max))[1];
    var i3 = document.createElement("button");
    // i3.innerHTML = max;
    i3.innerHTML = 'Delete';
    i3.className = "del";
    i3.id = max;
    item.appendChild(i1);
    item.appendChild(i2);
    item.appendChild(i3);
    list.appendChild(item);
    }

var task_tab = document.getElementsByClassName("tasks");
for(var i = 0; i < task_tab.length; i++) {
    (function(index) {
        task_tab[index].firstChild.addEventListener("click", function() {
        task_tab[index].firstChild.setAttribute("contenteditable", true); 
       })
        task_tab[index].firstChild.addEventListener("blur", function(){
        var klucz = task_tab[index].lastChild.id;
        var zmiana = task_tab[index].firstChild.innerHTML;
        var tab = JSON.parse(localStorage.getItem(klucz));
        tab[0]=zmiana;
        localStorage.setItem(klucz, JSON.stringify(tab));
       })
      })(i);
  }




add_delete_buttons();
}

function show_after_del(list_of_buttons, reg) {
    
    if (reg!==undefined)
    {
        var list = document.getElementById('lista');
    
    for(var i = 0; i<localStorage.length; i++){
    if(list_of_buttons.includes(localStorage.key(i)))
    {
    var item = document.createElement("li");
    var i1 = document.createElement("h3");
    i1.textContent = JSON.parse(localStorage.getItem(localStorage.key(i)))[0];
    
    
    var rep = JSON.parse(localStorage.getItem(localStorage.key(i)))[0].match(reg);
    i1.innerHTML = i1.innerHTML.replace(reg, "<mark>" + rep + "</mark>");
    
    var i2 = document.createElement("p");
    i2.textContent = JSON.parse(localStorage.getItem(localStorage.key(i)))[1];
    var i3 = document.createElement("button");
    i3.innerHTML = localStorage.key(i);
    i3.className = "del";
    i3.id = localStorage.key(i);
    item.appendChild(i1);
    item.appendChild(i2);
    item.appendChild(i3);
    list.appendChild(item);
    }
}
add_delete_buttons(reg);
}
else{
    showTODO();
}

}

function updateTODO() {
    var list = document.getElementById('lista');
    

    var item = document.createElement("li");
    var i1 = document.createElement("h3");
    i1.textContent = JSON.parse(localStorage.getItem(localStorage.key(0)))[0];
    var i2 = document.createElement("p");
    i2.textContent = JSON.parse(localStorage.getItem(localStorage.key(0)))[1];
    var i3 = document.createElement("button");
    i3.innerHTML = 'Delete';
    i3.className = "del";
    i3.id = localStorage.key(0);
    item.appendChild(i1);
    item.appendChild(i2);
    item.appendChild(i3);
    list.prepend(item);

    add_delete_buttons();
}

function min_date(){
    var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();

if (dd < 10) {
   dd = '0' + dd;
}

if (mm < 10) {
   mm = '0' + mm;
} 
    
today = yyyy + '-' + mm + '-' + dd;
document.getElementById("date").setAttribute("min", today);
}







