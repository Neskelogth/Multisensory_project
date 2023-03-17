class Barycenter {
  float xpos, ypos;
  int diameter;
  
  Barycenter (float x , float y, int d){
    xpos = x;
    ypos = y;
    diameter = d;
  }
  
  //display the barycenter
  void display(){
    fill(198);
    ellipse(xpos, ypos, diameter, diameter);
  }

}
