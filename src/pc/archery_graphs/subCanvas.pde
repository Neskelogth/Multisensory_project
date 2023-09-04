class subCanvas {
  float x,y;
  float contour;
  PShape s;
  float w,h;
  PShape axis_x, axis_y;
  
  subCanvas(float x_ , float y_, float contour_, float w_, float h_){
    
    x = x_;
    y = y_;
    w = w_;
    h = h_;
    contour = contour_;
   
    s = createShape();
    s.beginShape();
    s.noFill();
    s.stroke(100);
    s.strokeWeight(contour);
    // Exterior part of shape
    s.vertex(x - w / 2, y - h / 2); //h + x,-w/2 + y
    s.vertex(x - w / 2, y + h / 2);  //h + x, w/2 + y
    s.vertex(x + w / 2, y + h / 2); // -h + x,w/2 + y
    s.vertex(x + w / 2, y - h / 2); //-h + x,-w/2 + y
    // Finish off shape
    s.endShape(CLOSE);
    
  }
  
  void showAxis(String box_title){
    
    
    
    float half_width = w/2;
    float half_height = h/2;
    int font_size = 25;
    
    axis_x = createShape();
        axis_x.beginShape(LINES);
        axis_x.noFill();
        axis_x.stroke(200);
        axis_x.strokeWeight(1.2);
        axis_x.vertex(x - half_width, y);
        axis_x.vertex(x + half_width, y);
        axis_x.endShape();
      
      axis_y = createShape();
        axis_y.beginShape(LINES);
        axis_y.noFill();
        axis_y.stroke(200);
        axis_y.strokeWeight(1.2);
        axis_y.vertex(x, y - half_height);
        axis_y.vertex(x, y + half_height);
        axis_y.endShape();
      
      fill(120);
      textSize(font_size);
      textAlign(CENTER);
      text(box_title, x, y + half_height + font_size);
        
      //show axis
      shape(axis_x);
      shape(axis_y);
  }
  
  void display(){
    shape(s);
  }
  
}
