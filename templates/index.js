document.querySelectorAll('.divchild').forEach(item => {
    item.addEventListener('click', function() {
        // Toggle the 'expanded' class on click
        this.classList.toggle('expanded');
    });
});
