window.addEventListener("resize", function () {
    "use strict"; window.location.reload();
});

document.addEventListener("DOMContentLoaded", function () {
    let hasHover = getComputedStyle(document.documentElement).getPropertyValue('--has-hover');
    // make dropdowns open onclick instead of onhover for accordion on smaller screens or touch devices
    if (window.innerWidth < 992 || hasHover.includes('0')) {


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
                    // close submenu if it is already open and unfocus the link
                    if (nextEl.style.display == 'block') {
                        element.blur();
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
    }
    if (window.innerWidth >= 992) {
        // make caret in navbar point to the left when a dropdown is open
        document.querySelectorAll('.caret-hover').forEach(function (element) {
            let caret = element.querySelector('.caret-hover a');
            element.addEventListener('mouseenter', function (e) {
                caret.classList.add('carot-left')
            });
            element.addEventListener('mouseleave', function (e) {
                caret.classList.remove('carot-left')
            });
        });
    }

    // end if innerWidth

});
	// DOMContentLoaded  end