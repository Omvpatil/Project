const divchildContainer = document.querySelector('.pre-content'); // Assuming a container for divchilds
divchildContainer.addEventListener('click', function(event) {
  const clickedDivchild = event.target.closest('.divchild');
  if (clickedDivchild) {
    const checkbox = clickedDivchild.querySelector('.inp-cbx');
    checkbox.checked = !checkbox.checked;

    const label = clickedDivchild.querySelector('.cbx');
    if (checkbox.checked) {
      label.classList.add('checked');
      clickedDivchild.classList.add('adjusting');

      applyAnimation(clickedDivchild);

      requestAnimationFrame(function() {
        clickedDivchild.style.opacity = 0;
        setTimeout(() => {
          clickedDivchild.parentNode.removeChild(clickedDivchild);
            setTimeout(() => {
              adjustDivChildPositions();
            },1000);
        }, 700);
      });
    } else {
      label.classList.remove('checked');
    }
  }
});

function applyAnimation(clickedDivchild) {
    var height = clickedDivchild.offsetHeight;
    var parentDiv = document.getElementById('pre-content');
    var childDivs = parentDiv.querySelectorAll('divchild');
    var selectedDivs = [];
    for (var i = 0; i < childDivs.length; i++) {
        var div = childDivs[i];
        if (div !== clickedDivchild) {
        setTimeout(function() {
            div.classList.add('.adjusting');
            element.style.transform = 'translateY(-'+ height +')';
            },1000);
        }
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

function addEditableDivItem() {
        var button = event.target;
        var parent_name = button.parentNode;
        var li = document.createElement("li");
        li.className = "text";
        li.id = "draggable";
        li.style.overflow = "hidden";
        var input1 = document.createElement("div");
        input1.className = "taskName";
        input1.textContent = "Enter task";

        var input2 = document.createElement("div");
        input2.className = "taskTime";
        input2.textContent = "Enter Time";


        var btRow = document.createElement("div");
        btRow.className = "btn-row";
        btRow.style.display = "flex";
        btRow.style.flexDirection = "row";
        btRow.style.gap = "12rem";
        btRow.style.overflow = "hidden";
        btRow.style.marginLeft = "1rem";

        var editButton = document.createElement("button");
        editButton.className = "editTask";
        editButton.textContent = 'edit';
        editButton.style.cursor = "pointer";

        var saveButton = document.createElement("button");
        saveButton.className = "submitTask";
        saveButton.textContent = 'save';
        saveButton.style.cursor = "pointer";

        if (parent_name.nodeName === "UL") {
        li.appendChild(input1);
        li.appendChild(input2);
        btRow.appendChild(editButton);
        btRow.appendChild(saveButton);
        li.appendChild(btRow);
        parent_name.appendChild(li);
        } else {
            console.error("Parent node is not a UL element");
        }
}


