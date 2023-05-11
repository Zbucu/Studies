let styles: any = {default: "../src/Lab_1.css", alternative: "../src/Lab_1_2.css"};

let def_style = document.createElement("link");
def_style.rel = "stylesheet";
def_style.href = styles["default"];
document.getElementsByTagName("head")[0].appendChild(def_style);

let s_sheets = def_style.href!.split('/');
let current_sheet: string = s_sheets![s_sheets!.length - 1];
link_gen(current_sheet);

function change_style(name: string){
    let curr_style = document.getElementsByTagName("link").item(0);
    let new_style = document.createElement("link");
    new_style.setAttribute("rel", "stylesheet");
    new_style.setAttribute("href", styles[name]);

    document.getElementsByTagName("head").item(0)!.replaceChild(new_style, curr_style!);
    link_gen(styles[name]);
}

function link_gen(s_sheet: string){
    let foot = document.getElementsByTagName("footer")[0];

    for(const [key,value] of Object.entries(styles)){
        if(value!.toString() !== s_sheet.toString()){
            let style_link = document.createElement("a");
            style_link.id = key + "Style";
            style_link.innerHTML = "Style: " + key;
            style_link.onclick = function(){
                change_style(key);
            }
            if(foot.firstChild){
                foot!.replaceChild(style_link,foot.firstChild);
            }
            else{
                foot!.appendChild(style_link);
            }
        }
    }

}