var categories_rows_div = document.getElementById("categories-tags-rows");
var category_name_input = document.getElementsByClassName("category-name-input")[0];
var send_data_btn = document.getElementById("send-data-btn");
var categories_rows = document.getElementsByClassName("categories-tags");
var textAreaElement = document.getElementsByClassName("keywords-input")[0];
var tags = new Array;
var current_row_id = 0;

var ROW_LENGTH = 5;

class Tag{
    constructor(_id, _name){
        this.id = _id;
        this.name = _name;
    }
}

function retrieveDataFromTextArea(event){
    if (event.keyCode == 13 & textAreaElement.value != ""){
        data = textAreaElement.value;
        data = data.split(", ");
        textAreaElement.value = "";
        for(let i=0; i<data.length; i++){
            if(data[i] != "\n" & data[i] != " "){
                tags.push(addTag(data[i]));
            }
        }
    }

}

function updateCategoryRows(){
    window.categories_rows = document.getElementsByClassName("categories-tags");
}

function createNewCategoryRow(){
    let new_category_row = document.createElement("div");
    new_category_row.classList.add("categories-tags");
    categories_rows_div.appendChild(new_category_row);
    updateCategoryRows();
}

function addTag(tag_name){

    if(current_row_id < 0 | categories_rows[current_row_id].children.length > ROW_LENGTH-1){
        window.current_row_id += 1;
        createNewCategoryRow();
    }

    let tag_id = tags.length;
    let new_tag_element = document.createElement("div");
    new_tag_element.id = "KeywordTagID" + tag_id;
    new_tag_element.classList.add("new-category-keyword-tag");
    new_tag_element.innerHTML = "<div class='delete-btn'>X</div><h5 class='tag-name'>" + tag_name + "</h5>";
    new_tag_element.onclick = function(){deleteTag(tag_id)};
    categories_rows[current_row_id].appendChild(new_tag_element);
    tag_id = new_tag_element.id;
    let new_tag = new Tag(tag_id, tag_name);
    return new_tag;
}

function deleteTag(tag_id){
    let new_tags = new Array();
    for(let i=0; i<tags.length; i++){
        if(tags[i].id != tag_id)
            new_tags.push(tags[i]);
    }
    tags = new_tags;
    document.getElementById(tag_id).remove();
    updateCategoryRows();
    rebalanceTagsRows();
}

function rebalanceTagsRows(){
    for(let i=0; i<categories_rows.length; i++){
        let children_len = categories_rows[i].children.length;
        if(children_len < ROW_LENGTH & children_len > 0){
            if(categories_rows.length > i+1){
                categories_rows[i].appendChild(categories_rows[i+1].children[0]);
            }
        }
        else if(children_len == 0 & categories_rows.length > 1){
            categories_rows[i].remove();
            window.current_row_id--;
        }
    }
}



// send data to server

send_data_btn.addEventListener("click", (event)=>{
    event.preventDefault();
    sendData();
})

var xmlhttp = new XMLHttpRequest();

function serializeData(){
    keywords_list = new Array();
    for(let i=0; i<tags.length; i++){
        tag_name = (tags[i].name).trim();
        keywords_list.push(tag_name);
    }
    json_data = JSON.stringify({category_name: category_name_input.value, keywords: keywords_list});
    return(json_data);
}

function sendData(){
    xmlhttp.open("POST", "/create-category");
    xmlhttp.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    xmlhttp.send(serializeData());
}

retrieveDataFromTextArea(new KeyboardEvent('keydown', {bubbles: true, cancelable: true, keyCode: 13}));