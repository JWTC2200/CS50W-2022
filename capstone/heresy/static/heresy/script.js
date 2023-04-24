function unit_showhide(id) {
    console.log(id.firstElementChild)

    if (id.firstElementChild.hidden === false) {
        id.firstElementChild.hidden = true
    }else {
        id.firstElementChild.hidden = false
    }

}

function slot_showhide(id) {
    if (id.hidden === false) {
        id.hidden = true
    }else {
        id.hidden = false
    }
}