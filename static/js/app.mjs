function set_nav_current_page() {
    const data = document.querySelectorAll('[data-active-state]>li>a')
    const current_page = window.location.pathname
    data.forEach((item) => {
        if (item.getAttribute('href') === current_page) {
            item.classList.add('active')
        }
    })
}

function main() {
    set_nav_current_page()
}

document.addEventListener('DOMContentLoaded', main)