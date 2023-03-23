document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#menu').onchange = function() {
        document.querySelector('#hello').style.color = this.value;
    }

});