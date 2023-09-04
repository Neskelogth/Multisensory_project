class Barycenter {
  float xpos, ypos;
  int diameter;
  PShape circle;
  
  Barycenter (float x , float y, int d){
    xpos = x;
    ypos = y;
    diameter = d;
  }
    
  
  //display the barycenter
  void display(float rect_x , float rect_y, float rect_w, float rect_h){
    //Calculate the corner points of the rectangle
    float half_width = rect_w/2;
    
    //create dots
    circle = createShape(ELLIPSE, rect_x + (ypos * rect_h / 2), rect_y + (xpos * rect_w / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
    circle.setFill(color(0, 255, 0));
    //show dots
    shape(circle);
  }

}
