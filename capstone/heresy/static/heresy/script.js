const force_org_id = [
    "idHQ",
    "idElites",
    "idTroops",
    "idFastAttack",
    "idHeavySupport",
]

document.addEventListener("DOMContentLoaded", () => {
    unit_list_items()
    army_list_value()
})

// keep track of list items in local storage. 
function unit_list_items() {
    if (!localStorage.getItem("list_items")) {
        localStorage.setItem("list_items", 0)
    }
    // reset if the page resets (list resets)
    if (localStorage.getItem("list_items") != 0) {
        localStorage.setItem("list_items", 0)
    }
}

function army_list_value() {
    if (!localStorage.getItem("army_points")) {
        localStorage.setItem("army_points", 0)
    }
    if (localStorage.getItem("army_points") != 0) {
        localStorage.setItem("army_points", 0)
    }
}


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

function slot_showhide(box) {
    let id = document.getElementById(`${box}`)
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
        let member_tot = document.getElementById(`member_total_${unit_pk}`)
        if (member_tot) {
            member_tot = parseInt(document.getElementById(`member_total_${unit_pk}`).innerHTML)
        } else {
            member_tot = 0
        }
        const full_total = squad_total + member_tot + weapon_total
        const total_html = document.getElementById(`fulltotal_${unit_pk}`)
        // change total html
        total_html.innerHTML = `UNIT TOTAL: ${full_total}pts`

    })
}


function addUnitToList(button) {
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
        const force_org = response["force_org"]
        let squad_size = Number(response["members"])
        // empty weapon list
        weapon_list.forEach((key) => {
            // get number of each weapon
            let weapon_no = document.getElementById(`${key}_${id_num}`).value
            if (weapon_no > 0) {
                weapon_array.push(`${weapon_no} ${key}`)
            }         
        })
        // get unit size
        const squad_added = document.getElementById(`memberadded_${id_num}`)
        if (squad_added) {
            squad_size = squad_size + Number(squad_added.value)
        }
        
        const unit_total = document.getElementById(`fulltotal_${id_num}`).innerHTML.replace(/[^\d]/g, "")
        list_items++;
        localStorage.setItem("list_items", list_items)
        // add items to html
        add_list_html(id_num, weapon_array, list_items, unit_total, unit_name, force_org, squad_size)
    })
}


function add_list_html(id_num, weapon_array, list_items, unit_total, unit_name, force_org,squad_size) {
    const container = document.getElementById(`id${force_org}`)

    let unit_box = document.createElement("div");
    unit_box.setAttribute("id", `listunit_${list_items}`);
    // create unit title bar
    let unit_title = document.createElement("div");
    unit_title.setAttribute("class", "row")
    // unit title name
    let title_name = document.createElement("div")
    title_name.setAttribute("id", `luname_${list_items}`)
    title_name.setAttribute("class", "col")
    title_name.innerHTML = `${unit_name} (${squad_size})`
    // unit title points, rght aligned
    let title_pts = document.createElement("div")
    title_pts.setAttribute("id", `lupts_${list_items}`)
    title_pts.setAttribute("class", "col text-end")
    title_pts.innerHTML = `${unit_total}pts`
    // add onto title div
    unit_title.appendChild(title_name)
    unit_title.appendChild(title_pts)
    // add onto main unit box
    unit_box.appendChild(unit_title)
    // create list of unit weapons if applicable
    if (weapon_array != "") {
        let weapon_ul = document.createElement("ul")
        weapon_ul.setAttribute("id", `luwpli_${list_items}`)
        weapon_ul.setAttribute("class", "list-group list-group-flush")
        // add weapons to list
        for (i = 0; i < weapon_array.length; ++i) {
            let weapon_li = document.createElement("li")
            weapon_li.setAttribute("id", `luwp_${list_items}_${i}`)
            weapon_li.innerHTML = `${weapon_array[i]}`
            weapon_ul.appendChild(weapon_li)
        }     
        unit_box.appendChild(weapon_ul)   
    }
    // add delete button
    let box_delete = document.createElement("div")
    box_delete.setAttribute("id", `deletebox_${list_items}`)
    box_delete.setAttribute("class", "btn btn-sm")
    box_delete.innerHTML = "Remove"
    unit_box.appendChild(box_delete)

    // send to correct force org slot
    container.appendChild(unit_box)
    // add delete box to button
    add_delete_event(list_items, unit_total)
    change_armyvalue(unit_total)
}

function add_delete_event(list_items, unit_total) {
    let button = document.getElementById(`deletebox_${list_items}`)
    button.addEventListener("click", () => {
        let box = document.getElementById(`listunit_${list_items}`)
        box.remove()
        change_armyvalue(`-${unit_total}`)
    })
    
}

function change_armyvalue(unit_total) {
    let armypoints = document.querySelector("#armyvalue")
    let newvalue = Number(localStorage.getItem("army_points"))
    newvalue = newvalue + Number(unit_total)
    localStorage.setItem("army_points", newvalue)
    armypoints.innerHTML = `${newvalue}pts`
}

    
function save_whole_list() {
    let listname = document.querySelector("#listname").innerHTML
    console.log(listname)
    fetch('/list_name_check', {
        method: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
            "newname": listname,
        })
    })
    .then(response => response.json())
    .then(response => {
        if (response["warning"]) {
            apply_warning(response["warning"])
        } else {
            const list_items = localStorage.getItem("list_items")
            const warning_count = 0
            const list_points = document.querySelector("#armyvalue").innerHTML.replace("pts", "")
            for (i = 1; i <= list_items; i++) {
                let unit_exist = document.getElementById(`listunit_${i}`)
                if (unit_exist) {
                    let unit_name = document.getElementById(`luname_${i}`).innerHTML
                    let unit_points = document.getElementById(`lupts_${i}`).innerHTML.replace("pts","")
                    let unit_weapons = document.getElementById(`luwpli_${i}`)
                    let weapon_list = []
                    if (unit_weapons) {
                        let lilist = unit_weapons.getElementsByTagName("li").length
                        for (j = 0; j < lilist; ++j) {
                            let liweapon = document.getElementById(`luwp_${i}_${j}`).innerHTML
                            weapon_list.push(liweapon)
                        }
                    }
                let list_name = document.querySelector("#listname").innerHTML
                // send data to be stored
                fetch('/savelist', {
                    method: "PUT",
                    headers: {'X-CSRFToken': csrftoken},
                    body: JSON.stringify({
                    "unit_name": unit_name,
                    "unit_points": unit_points,
                    "unit_weapons": weapon_list,
                    "list_name": list_name,
                    "list_points": list_points,
                    })
                })
                .then(response => response.json())
                .then(response => {
                    if (response["warning"]) {
                        apply_warning(response["warning"])
                    }
                })
            }
            else {
                warning_count += 1
            }                
        }
        if (warning_count >= list_items) {
            apply_warning("List is empty")
        }
                
        }
        
    })

    
}

function list_name() {
    let listname = document.querySelector("#listname")
    let newname = document.querySelector("#newname")
    let nametext = document.querySelector("#nametext").value
    
    if (newname.hidden === true) {
        newname.hidden = false
        listname.hidden = true
    } 
    else {
        apply_warning("")
        newname.hidden = true
        listname.hidden = false
        if (nametext === "") {
            apply_warning("Please enter a list name")
        } else {
            listname.innerHTML = nametext
        }
        
    }
}

function apply_warning(warning) {
    const warning_box = document.querySelector("#warning-div")
    warning_box.innerHTML = warning
}


        
        