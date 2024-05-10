document.addEventListener('DOMContentLoaded', function() {
    // Get the cueball element from the SVG
    var cueball = document.getElementById('cueBall');
    var line = document.getElementById('line');

    line.setAttribute('x1', cueball.cx.baseVal.value);
    line.setAttribute('y1', cueball.cy.baseVal.value);

    // Define constants for scaling
    var scale = 4; // Adjust as needed

    // Variables to track mouse coordinates and dragging state
    var isDragging = false;
    var initX, initY; //Define initX and initY outside of the event listeners

    // Add mousedown event listener to start dragging
    cueball.addEventListener('mousedown', function(event) {
        isDragging = true;

        initX = event.clientX; // Assign value to initX
        initY = event.clientY; // Assign value to initY

        // Show the line
        line.style.display = 'block';
    });

    // Add mousemove event listener to track mouse movement
    document.addEventListener('mousemove', function(event) {
        if (isDragging) {
            var adjustedX = (event.clientX - initX) * scale + parseFloat(cueball.getAttribute('cx')); 
            var adjustedY = (event.clientY - initY) * scale + parseFloat(cueball.getAttribute('cy'));
            // Update the line position to end at the adjusted mouse position
            line.setAttribute('x2', adjustedX);
            line.setAttribute('y2', adjustedY);
        }
    });

    // Add mouseup event listener to stop dragging
    document.addEventListener('mouseup', function() {
        isDragging = false;
        var cueball = document.getElementById('cueBall');

        var finalX = (event.clientX - initX) * scale;
        var finalY = (event.clientY - initY) * scale;

        console.log("this is final X" + finalX)
        console.log(finalY)
        // Hide the line when dragging stops
        line.style.display = 'none';
    });
});

