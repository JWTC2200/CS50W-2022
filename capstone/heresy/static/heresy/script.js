function unit_showhide(id) {
    console.log(id)
    box = document.querySelector(`#box${id}`)
    console.log(box)
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

function total_points(id) {
    console.log(id)
}