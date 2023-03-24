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
  
    //println("window ",  rect_x - rect_h);
    
    //control on the border of the window
    if ( (xpos > rect_x - rect_h) && (xpos < rect_x + rect_h) && (ypos > rect_y - half_width) && (ypos < rect_y + half_width) ){
      
      //create dots
      circle = createShape(ELLIPSE, xpos, ypos, diameter, diameter);
      circle.setFill(color(170));
      
      //show dots
      shape(circle);
      } 
  }

}
