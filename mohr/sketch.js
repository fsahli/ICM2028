let circleCenter, circleRadius;
let tensorSquare;
let drag = false;
let angle, refangle, P, R, rotangle;
let inputSigmaX, inputSigmaY, inputTauXY;
let updateButton;
let sigmax_ref, sigmay_ref, tauxy_ref;
let sigmax, sigmay, tauxy;
let scaling;
let sigmax_im, sigmay_im, tauxy_im;
let sigmaxp_im, sigmayp_im, tauxyp_im;

function setup() {
    createCanvas(800, 400);
    circleCenter = createVector(width / 2*1.2, height / 2);
    circleRadius = 150;
    tensorSquare = new TensorSquare(100, 100, 100);
    angle = PI/4;
    // Create input fields for sigmaX, sigmaY, and tauXY
    inputSigmaX = createInput('40');
    inputSigmaX.position(20, height);
    
    inputSigmaY = createInput('-40');
    inputSigmaY.position(140, height);
    inputTauXY = createInput('30');
    inputTauXY.position(260, height);

    // Create a button to update the values
    updateButton = createButton('Update Values');
    updateButton.position(380, height);
    updateButton.mousePressed(updateStressValues); // Attach event listener to button

    updateStressValues(); // Initialize with default values
  
    sigmax_im = loadImage("sigmax.png");
    sigmay_im = loadImage("sigmay.png");
    tauxy_im = loadImage("tauxy.png");
  
    sigmaxp_im = loadImage("sigmaxp.png");
    sigmayp_im = loadImage("sigmayp.png");
    tauxyp_im = loadImage("tauxyp.png");

}


function draw() {
    background(255);
  
    // drawTex('\\sigma_x', 20, height*0.9);
    // drawTex('\\sigma_y', 140, height*0.9);
    // drawTex('\\tau_{xy}', 260, height*0.9);
    image(sigmax_im, 20, height*0.95);
    sigmax_im.resize(0,20);
    image(sigmay_im, 140, height*0.95);
    sigmay_im.resize(0,20);
    image(tauxy_im, 260, height*0.95);
    tauxy_im.resize(0,20);
    
    sigmax = P + R*cos(angle);
    sigmay = P - R*cos(angle);
    tauxy = R*sin(angle);

    rotangle = (refangle - angle)*180/(2*3.1415);
    text(`= ${sigmax.toFixed(1)}`,40, 300);
    text(`= ${sigmay.toFixed(1)}`,40, 320);
    text(`= ${tauxy.toFixed(1)}`,40, 340);
    text(`θ = ${rotangle.toFixed(1)}º`,25, 360);


    image(sigmaxp_im, 20,290);
    sigmaxp_im.resize(0,15);
    image(sigmayp_im, 20,310);
    sigmayp_im.resize(0,15);
    image(tauxyp_im, 20, 330);
    tauxyp_im.resize(0,15);
    
    
    tensorSquare.sigmaX = sigmax*scaling;
    tensorSquare.sigmaY = sigmay*scaling;
    tensorSquare.tauXY = tauxy*scaling;
  
    drawMohrsCircle();
    tensorSquare.display();
  

}


function drawTex(tex, posx, posy) {
  let texp = createP();
  texp.style('font-size', '15px');
  texp.position(posx, posy);
  katex.render(tex, texp.elt)

}
// Function to read input values and update the stress components
function updateStressValues() {
    sigmaX_ref = parseFloat(inputSigmaX.value());
    sigmaY_ref = parseFloat(inputSigmaY.value());
    tauXY_ref = parseFloat(inputTauXY.value());
  
    P = (sigmaX_ref + sigmaY_ref)/2;
    R = sqrt(sq(tauXY_ref) + sq(P - sigmaX_ref));
    refangle = atan2(tauXY_ref, sigmaX_ref - P);
    print(P, R, refangle);
    scaling = 40/(P + R);


}

function drawMohrsCircle() {
    // Drawing Mohr's circle
    stroke(0);
    noFill();
    ellipse(circleCenter.x, circleCenter.y, 2 * circleRadius);
  // axis line
      line(circleCenter.x - circleRadius*1.1,circleCenter.y ,circleCenter.x + circleRadius*1.1,circleCenter.y  )
  // diameter line
    line(circleCenter.x - circleRadius*cos(angle),circleCenter.y - circleRadius*sin(angle),circleCenter.x + circleRadius*cos(angle),circleCenter.y + circleRadius*sin(angle) )
  // vert line 1  
      line(circleCenter.x - circleRadius*cos(angle),circleCenter.y - circleRadius*sin(angle),circleCenter.x - circleRadius*cos(angle),circleCenter.y )
      image(sigmayp_im, circleCenter.x - circleRadius*cos(angle) + 5,circleCenter.y + 5);
    sigmayp_im.resize(0,15);
  
  // vert line 1
      line(circleCenter.x + circleRadius*cos(angle),circleCenter.y + circleRadius*sin(angle),circleCenter.x + circleRadius*cos(angle),circleCenter.y )
      image(sigmaxp_im, circleCenter.x + circleRadius*cos(angle) + 5,circleCenter.y + 5);
    sigmaxp_im.resize(0,15);
      image(tauxyp_im, circleCenter.x + circleRadius*cos(angle) + 5,circleCenter.y + circleRadius*sin(angle)+ 5);
    tauxyp_im.resize(0,15);
  
  
  
  /////////////// ref line /////////////////
    stroke('blue')
      noFill();
  // diameter line
    line(circleCenter.x - circleRadius*cos(refangle),circleCenter.y - circleRadius*sin(refangle),circleCenter.x + circleRadius*cos(refangle),circleCenter.y + circleRadius*sin(refangle) )
  
  // vert line 1  
      line(circleCenter.x - circleRadius*cos(refangle),circleCenter.y - circleRadius*sin(refangle),circleCenter.x - circleRadius*cos(refangle),circleCenter.y )
  // vert line 1
      line(circleCenter.x + circleRadius*cos(refangle),circleCenter.y + circleRadius*sin(refangle),circleCenter.x + circleRadius*cos(refangle),circleCenter.y )
  stroke(0);

}


class TensorSquare {
    constructor(x, y, size) {
        this.x = x;
        this.y = y;
        this.size = size;
        this.sigmaX = 50;  // Example starting value
        this.sigmaY = 50;  // Example starting value
        this.tauXY = 30;   // Example starting value
    }

    display() {
        push();
        translate(this.x + this.size/2, this.y + this.size/2);
        rotate(-rotangle*3.1415/180);
        rect(-this.size/2, -this.size/2, this.size, this.size);
        // Update and display stress values
        this.drawArrows();
        pop();
    }

    drawArrows() {
        let spacing = 10;  // Space from the edge of the square for shear arrows
        
        // Sigma X arrows (horizontal)
        this.drawArrow(-this.size/2, 0, -this.size/2- this.sigmaX, 0);
        this.drawArrow(this.size/2, 0,  this.size/2 + this.sigmaX, 0);
        
        // Sigma Y arrows (vertical)
        this.drawArrow(0, -this.size/2, 0, -this.size/2 - this.sigmaY);
        this.drawArrow(0, this.size/2, 0, this.size/2 + this.sigmaY);
        
        // Tau XY arrows (shear) with added spacing from edges
        this.drawArrow(-this.size/2 - spacing, 0, -this.size/2 - spacing, 0 + this.tauXY);
        this.drawArrow(this.size/2 + spacing, 0, this.size/2 + spacing,  - this.tauXY);
        this.drawArrow(0, -this.size/2 - spacing,  this.tauXY, -this.size/2 - spacing);
        this.drawArrow(0, this.size/2 + spacing, 0 - this.tauXY, this.size/2 + spacing);
    }

    drawArrow(startX, startY, endX, endY) {
        stroke(0);
        line(startX, startY, endX, endY);
        let angle = atan2(endY - startY, endX - startX);
        push();
        translate(endX, endY);
        rotate(angle);
        triangle(0, -5, 10, 0, 0, 5);
        pop();
    }
}





function mousePressed() {
    // Check if within Mohr's circle
    if (dist(mouseX, mouseY, circleCenter.x, circleCenter.y) <= circleRadius) {
        drag = true;

      print('pressed')
    }
}

function mouseReleased() {
    drag = false;
}

function mouseDragged() {
    if (drag) {
        // Update the circle and tensor values based on dragging
      let target_angle = atan2(mouseY - circleCenter.y, mouseX - circleCenter.x);
      angle += (target_angle - angle);
    }
}
