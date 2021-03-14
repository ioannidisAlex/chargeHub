function setup(){
        var canvas = createCanvas(400, 400);
        canvas.parent('anime');
    }
    
function draw(){
    background(251);
    var raf = [4.9, 3.2, 4.55, 2.92, 0.47, 0.81];
    let c = color('#1f8056');
    noFill()
    stroke(c);
    for (let i = 0; i < 5; i++) {
      strokeWeight(1+raf[i]/10);
      arc(135,height/2-12, raf[i]*54,raf[i]*54, 0+i+(frameCount/36),PI+HALF_PI+i+(frameCount/36));
    }
    for (let i = 5; i < 6; i++) {
      strokeWeight(1+raf[i]/10);
      arc(135,height/2-12, raf[i]*54,raf[i]*54, 0+i-(frameCount/36),PI+HALF_PI+i-(frameCount/36));
    }
    //strokeWeight(1+4/10);
    //arc(width/2,height/2,4*30,4*30,PI,PI+HALF_PI);
}