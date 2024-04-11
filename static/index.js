const divchildContainer = document.querySelector('.pre-content'); // Assuming a container for divchilds
divchildContainer.addEventListener('click', function(event) {
  const clickedDivchild = event.target.closest('.divchild');
  if (clickedDivchild) {
    const checkbox = clickedDivchild.querySelector('.inp-cbx');
    checkbox.checked = !checkbox.checked;

    const label = clickedDivchild.querySelector('.cbx');
    if (checkbox.checked) {
      label.classList.add('checked');
      clickedDivchild.classList.add('removing');

      applyAnimationToSiblings(clickedDivchild);

      requestAnimationFrame(function() {
        clickedDivchild.style.opacity = 0;
        setTimeout(() => {
          clickedDivchild.parentNode.removeChild(clickedDivchild);
          adjustDivChildPositions();
        }, 500);
      });
    } else {
      label.classList.remove('checked');
    }
  }
});

function applyAnimationToSiblings(clickedDivchild) {
  const viewportHeight = window.innerHeight;
  const scrolledDistance = window.scrollY;
  const divchildRect = clickedDivchild.getBoundingClientRect();
  const divchildTopInView = divchildRect.top >= 0 && divchildRect.top <= viewportHeight;
  const divchildBottomInView = divchildRect.bottom >= 0 && divchildRect.bottom <= viewportHeight;

  let nextSibling = clickedDivchild.nextElementSibling;
  while (nextSibling) {
    const siblingRect = nextSibling.getBoundingClientRect();
    const siblingTopInView = siblingRect.top >= 0 && siblingRect.top <= viewportHeight;
    const siblingBottomInView = siblingRect.bottom >= 0 && siblingRect.bottom <= viewportHeight;

    if (siblingTopInView || siblingBottomInView) {
      nextSibling.classList.add('adjusting');
      const translateY = Math.max(0, (divchildRect.bottom - scrolledDistance - siblingRect.top) / 15);
      nextSibling.style.transform = `translateY(-${translateY}px)`;
    }
    nextSibling = nextSibling.nextElementSibling;
  }
}









    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) =>{
        console.log(entry)
        if(entry.isIntersecting){
            entry.target.classList.add('scrollIn')
        }else{
            entry.target.classList.remove('scrollIn')
        }
        });
    });

    const hiddenElements = document.querySelectorAll('.divchild');
    hiddenElements.forEach((el)=> observer.observe(el));

