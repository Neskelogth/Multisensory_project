class Archer {
  float shoulderL_x, shoulderL_y;
  float shoulderR_x, shoulderR_y;
  
  float elbowL_x, elbowL_y;
  float elbowR_x, elbowR_y;
  
  float wristL_x, wristL_y;
  float wristR_x, wristR_y;
  
  int diameter;
  PShape circle;
  PShape line;
  
  Archer(float ls_x, float ls_y, float rs_x, float rs_y, float le_x, float le_y, float re_x, float re_y, float lw_x, float lw_y, float rw_x, float rw_y, int d){
    
    shoulderL_x = ls_x;
    shoulderL_y = ls_y;
    shoulderR_x = rs_x;
    shoulderR_y = rs_y;
    
    elbowL_x = le_x;
    elbowL_y = le_y;
    elbowR_x = re_x;
    elbowR_y = re_y;
    
    wristL_x = lw_x;
    wristL_y = lw_y;
    wristR_x = rw_x;
    wristR_y = rw_y;
    
    diameter = d;
  }
  
  //display the archer arms configuration from a view from top
  void display(float rect_x , float rect_y, float rect_w, float rect_h, int max_x, int max_y){
    
    max_x /= 2;
    max_y /= 2;
    
    circle = createShape(ELLIPSE, rect_x + (shoulderL_x / max_x * rect_w / 2), rect_y - (shoulderL_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 0, 255));
    //show dots
    shape(circle);
    
    circle = createShape(ELLIPSE, rect_x + (shoulderR_x / max_x * rect_w / 2), rect_y - (shoulderR_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 255, 0));
    //show dots
    shape(circle);
    
    circle = createShape(ELLIPSE, rect_x + (elbowL_x / max_x * rect_w / 2), rect_y - (elbowL_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 0, 255));
    //show dots
    shape(circle);
    
    circle = createShape(ELLIPSE, rect_x + (elbowR_x / max_x * rect_w / 2), rect_y - (elbowR_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 255, 0));
    //show dots
    shape(circle);
    
    circle = createShape(ELLIPSE, rect_x + (wristL_x / max_x * rect_w / 2), rect_y - (wristL_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 0, 255));
    //show dots
    shape(circle);
    
    circle = createShape(ELLIPSE, rect_x + (wristR_x / max_x * rect_w / 2), rect_y - (wristR_y / max_y * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 255, 0));
    //show dots
    shape(circle);
    
    line = createShape();
    line.beginShape(LINES);
    line.noFill();
    line.stroke(255, 0, 0);
    line.strokeWeight(1.5);
    line.vertex(rect_x + (shoulderL_x / max_x * rect_w / 2), rect_y - (shoulderL_y / max_y * rect_h / 2));
    line.vertex(rect_x + (shoulderR_x / max_x * rect_w / 2), rect_y - (shoulderR_y / max_y * rect_h / 2));
    line.endShape();
    shape(line);
    
    line = createShape();
    line.beginShape(LINES);
    line.noFill();
    line.stroke(255, 0, 0);
    line.strokeWeight(1.5);
    line.vertex(rect_x + (shoulderL_x / max_x * rect_w / 2), rect_y - (shoulderL_y / max_y * rect_h / 2));
    line.vertex(rect_x + (elbowL_x / max_x * rect_w / 2), rect_y - (elbowL_y / max_y * rect_h / 2));
    line.endShape();
    shape(line);
    
    line = createShape();
    line.beginShape(LINES);
    line.noFill();
    line.stroke(255, 0, 0);
    line.strokeWeight(1.5);
    line.vertex(rect_x + (shoulderR_x / max_x * rect_w / 2), rect_y - (shoulderR_y / max_y * rect_h / 2));
    line.vertex(rect_x + (elbowR_x / max_x * rect_w / 2), rect_y - (elbowR_y / max_y * rect_h / 2));
    line.endShape();
    shape(line);
    
    line = createShape();
    line.beginShape(LINES);
    line.noFill();
    line.stroke(255, 0, 0);
    line.strokeWeight(1.5);
    line.vertex(rect_x + (elbowL_x / max_x * rect_w / 2), rect_y - (elbowL_y / max_y * rect_h / 2));
    line.vertex(rect_x + (wristL_x / max_x * rect_w / 2), rect_y - (wristL_y / max_y * rect_h / 2));
    line.endShape();
    shape(line);
    
    line = createShape();
    line.beginShape(LINES);
    line.noFill();
    line.stroke(255, 0, 0);
    line.strokeWeight(1.5);
    line.vertex(rect_x + (elbowR_x / max_x * rect_w / 2), rect_y - (elbowR_y / max_y * rect_h / 2));
    line.vertex(rect_x + (wristR_x / max_x * rect_w / 2), rect_y - (wristR_y / max_y * rect_h / 2));
    line.endShape();
    shape(line);
    
    fill(198);
    //ellipse(xpos, ypos, diameter, diameter);
  }

}
