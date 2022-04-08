window.addEventListener("resize", function () {
    "use strict"; window.location.reload();
});

document.addEventListener("DOMContentLoaded", function () {

    // make it as accordion for smaller screens
    if (window.innerWidth < 992) {

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
                        nextEl.style.display = 'block';
                    }

                }
            });
        });
    }
    // end if innerWidth

});
	// DOMContentLoaded  end