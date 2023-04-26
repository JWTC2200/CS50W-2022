document.addEventListener("DOMContentLoaded", () => {
    unit_list_items()
})
    // keep track of list items in local storage. 


const csrftoken = getCookie('csrftoken');

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}



function unit_showhide(unit) {
    box = document.querySelector(`#box${unit.id}`)
    if (box.hidden === false) {
        box.hidden = true
    } else {
        box.hidden = false
    }
}

function slot_showhide(id) {
    if (id.hidden === false) {
        id.hidden = true
    }else {
        id.hidden = false
    }
}

function total_unitMembers(members) {
    // get id 
    let id_num = members.id.split("_")[1]
    // get member cost from data attribute
    const points = members.getAttribute('data-points')
    const number = members.value
    const total = points * number
    const location = document.getElementById(`member_total_${id_num}`)
    location.innerHTML = `${total}pts`
    recalculateUnitTotal(id_num)
}

function total_weaponPoints(weapon) {
    // split id 
    id_weapon = weapon.id.split("_")[0]
    id_num = weapon.id.split("_")[1]
    // get points total and target element for total
    const points = document.getElementById(`${id_weapon}_cost_${id_num}`).innerHTML
    const total_field = document.getElementById(`${id_weapon}_total_${id_num}`)  
    //calculate total and change html 
    let total = weapon.value * points 
    total_field.innerHTML = total
    recalculateUnitTotal(id_num)
}

function recalculateUnitTotal(unit_pk) {
    // get unit pk -> id

    // get list of weapons (for id matching)
    fetch('/unittotal', {
        method: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            unit_pk: unit_pk,
        })
    })
    .then(response => response.json())
    .then(response => {
        // array of weapon names
        const weapon_list = Object.keys(response["list"]);
        let weapon_total = 0
        weapon_list.forEach((key) => {
            // get each total value and add for weapon_total
            let weapon_t = document.getElementById(`${key}_total_${unit_pk}`)
            if (weapon_t.innerHTML != "") {
                weapon_total = weapon_total + Number(weapon_t.innerHTML)
            }
        })
        const squad_total =  response["squad"]
        const member_total = parseInt(document.getElementById(`member_total_${unit_pk}`).innerHTML)
        const full_total = squad_total + member_total + weapon_total
        const total_html = document.getElementById(`fulltotal_${unit_pk}`)
        // change total html
        total_html.innerHTML = `UNIT TOTAL: ${full_total}pts`

    })
}

function unit_list_items() {
    if (!localStorage.getItem("list_items")) {
        localStorage.setItem("list_items", 0)
    }
    // reset if the page resets (list resets)
    if (localStorage.getItem("list_items") != 0) {
        localStorage.setItem("list_items", 0)
    }
}



function addUnitToList(button, method) {
    let list_items = localStorage.getItem("list_items")
    let id_num = button.id.split("_")[1]
    let weapon_array = []
    // get list of weapons
    fetch('/unittotal', {
        method: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            unit_pk: id_num,
        })
    })    
    .then(response => response.json())
    .then(response => {
        const unit_name = response["name"];
        const weapon_list = Object.keys(response["list"]);
        // empty weapon list
        weapon_list.forEach((key) => {
            // get number of each weapon
            let weapon_no = document.getElementById(`${key}_${id_num}`).value
            if (weapon_no > 0) {
                weapon_array.push(`${weapon_no} ${key}`)
            }         
        })
        const unit_total = document.getElementById(`fulltotal_${id_num}`).innerHTML.replace(/[^\d]/g, "")
        list_items++;
        localStorage.setItem("list_items", list_items)
        // add items to html
        add_list_html(id_num, weapon_array, list_items, unit_total, unit_name)
    })
}


function add_list_html(id_num, weapon_array, list_items, unit_total, unit_name) {
    const container = document.querySelector("#list-container")

    var unit_box = document.createElement("div");
    unit_box.setAttribute("id", `listunit_${list_items}`);
    unit_box_weapons = ""
    let list_li = ""
    for (i = 0; i < weapon_array.length; ++i) {
        console.log(weapon_array[i])
        li_html = `<li>${weapon_array[i]}</li>`
        list_li = list_li + li_html
    }
    if (list_li != "") {
        list_li = `<div><ul>${list_li}</ul></div>`
    }
    var list_head = `
    <div class="luname_${id_num}">${unit_name}</div>
    <div class="lupts_${id_num}">${unit_total}pts</div>
    `;
    
    unit_box.innerHTML = list_head + list_li

    container.appendChild(unit_box)
}