var categories_rows_div = document.getElementById("categories-tags-rows");
var categories_rows = document.getElementsByClassName("categories-tags");
var textAreaElement = document.getElementsByClassName("keywords-input")[0];
var tags = new Array;
var current_row_id = 0;

function retrieveDataFromTextArea(event){
    if (event.keyCode == 13){
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

    if(current_row_id < 0 | categories_rows[current_row_id].children.length > 4){
        window.current_row_id += 1;
        createNewCategoryRow();
    }

    let tag_id = tags.length;
    let new_tag_element = document.createElement("div");
    new_tag_element.id = "KeywordTagID" + tag_id;
    new_tag_element.classList.add("new-category-keyword-tag");
    new_tag_element.innerHTML = "<div class='delete-btn'>X</div><h5>" + tag_name + "</h5>";
    new_tag_element.onclick = function(){deleteTag(tag_id)};
    categories_rows[current_row_id].appendChild(new_tag_element);
    tag_id = new_tag_element.id;
    return tag_id;
}

function deleteTag(tag_id){
    let tag_to_remove = tags.splice(tags.indexOf(tag_id), 1)[0];
    document.getElementById(tag_to_remove).remove();
    updateCategoryRows();
    rebalanceTagsRows();
}

function rebalanceTagsRows(){
    for(let i=0; i<categories_rows.length; i++){
        let children_len = categories_rows[i].children.length;
        if(children_len < 5 & children_len > 0){
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