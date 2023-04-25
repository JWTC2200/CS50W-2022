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
    console.log(total)
    const location = document.getElementById(`member_total_${id_num}`)
    location.innerHTML = `Total: ${total}pts`
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
}

function recalculateUnitTotal() {
    
}


function addUnitToList(button) {
    let id_num = button.id.split("_")[1]
    console.log(id_num)

}