window.addEventListener("resize", function () {
    "use strict"; window.location.reload();
});

document.addEventListener("DOMContentLoaded", function () {

    // make it as accordion for smaller screens
    if (window.innerWidth < 992 || getComputedStyle(document.documentElement).getPropertyValue('has-hover') == false) {

        // close all inner dropdowns when parent is closed
        document.querySelectorAll('.navbar .dropdown').forEach(function (dropdown) {
            dropdown.addEventListener('hidden.bs.dropdown', function () {
                // after dropdown is hidden, then find all submenus
                this.querySelectorAll('.dropdown-submenu').forEach(function (submenu) {
                    // hide every submenu as well
                    submenu.style.display = 'none';
                });
            })
        });

        document.querySelectorAll('.dropdown-menu a').forEach(function (element) {
            element.addEventListener('click', function (e) {
                e.stopPropagation();

                let nextEl = this.nextElementSibling;
                if (nextEl && nextEl.classList.contains('dropdown-submenu')) {
                    // prevent opening link if link needs to open dropdown
                    e.preventDefault();

                    if (nextEl.style.display == 'block') {
                        nextEl.style.display = 'none';
                    } else {
                        // hide all other menus
                        document.querySelectorAll('.dropdown-submenu').forEach(function (submenu) {
                            submenu.style.display = 'none';
                            element.blur();
                        });
                        // remove focus from all items
                        document.querySelectorAll('.dropdown-menu a').forEach(function (dropdownMenu) {
                            dropdownMenu.blur();
                        });
                        // show the clicked menu and focus on the expanded menu
                        element.focus();
                        nextEl.style.display = 'block';
                    }

                }
            });
        });
    } else { // add proper focus for larger screens
        document.querySelector('.dropdown-menu > li > a, .dropdown-submenu').forEach(function (element) {
            element.addEventListener('mouseover', function (e) {
                e.stopPropagation();
                element.focus();
            });
        });
    }
    // end if innerWidth

});
	// DOMContentLoaded  end