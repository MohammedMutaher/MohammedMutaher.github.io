document.addEventListener('DOMContentLoaded', function() {

    // ---- Dropdown menu (open/close on click, close when clicking elsewhere) ----
    var dropdown = document.querySelector('[data-nav-dropdown]');
    if (dropdown) {
        var toggle = dropdown.querySelector('[data-nav-toggle]');

        function setOpen(isOpen) {
            dropdown.classList.toggle('is-active', isOpen);
            toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        }

        toggle.addEventListener('click', function(event) {
            event.preventDefault();
            setOpen(!dropdown.classList.contains('is-active'));
        });
        toggle.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                setOpen(!dropdown.classList.contains('is-active'));
            }
        });
        dropdown.querySelectorAll('.navbar-dropdown a').forEach(function(link) {
            link.addEventListener('click', function() { setOpen(false); });
        });
        document.addEventListener('click', function(event) {
            if (!dropdown.contains(event.target)) { setOpen(false); }
        });
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') { setOpen(false); }
        });
    }

    // ---- Publication topic tabs ----
    var buttons = Array.from(document.querySelectorAll('[data-publication-filter]'));
    var publications = Array.from(document.querySelectorAll('[data-publication]'));
    var emptyMessage = document.querySelector('[data-publication-empty]');
    if (!buttons.length || !publications.length) {
        return;
    }

    function applyFilter(filter) {
        var visibleCount = 0;
        publications.forEach(function(publication) {
            var tags = (publication.dataset.tags || '').split(/\s+/).filter(Boolean);
            var isVisible = filter === 'all' || tags.indexOf(filter) !== -1;
            publication.hidden = !isVisible;
            if (isVisible) { visibleCount += 1; }
        });
        if (emptyMessage) { emptyMessage.hidden = visibleCount > 0; }
    }

    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            buttons.forEach(function(other) {
                var isActive = other === button;
                other.classList.toggle('is-active', isActive);
                other.setAttribute('aria-pressed', isActive ? 'true' : 'false');
            });
            applyFilter(button.dataset.publicationFilter || 'all');
        });
    });
});
