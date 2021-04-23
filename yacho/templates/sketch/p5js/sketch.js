function setup() {
    // put setup code here
    createCanvas(windowWidth, windowHeight);
}

function draw() {
    // put drawing code here
    background(0);

    translate(width / 2.0, height / 2.0);
    scale(1.0 + 0.02 * sin(frameCount / TWO_PI / 2.0));
    fill(255); textSize(24); textAlign(CENTER, CENTER);
    text('Your sketch `{{ id }}` is running.', 0, -20.0);
    text('Happy Processing!', 0, 20.0);
}

function windowResized() {
    resizeCanvas(windowWidth, windowHeight);
}
