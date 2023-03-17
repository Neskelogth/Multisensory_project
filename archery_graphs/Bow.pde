class Bow {
  float xpos, ypos, zpos;
  int diameter;
  
  Bow(float x , float y, float z, int d){
    xpos = x;
    ypos = y;
    zpos = z;
    diameter = d;
  }
  
  //display Bow shaking in two different planes
  //plane x-y and plane x-z ? 
  void display(){
    //define the position in the display
    fill(198);
    ellipse(xpos, ypos, diameter, diameter);
    
    fill(100);
    ellipse(xpos, zpos, diameter, diameter);
  }

}
