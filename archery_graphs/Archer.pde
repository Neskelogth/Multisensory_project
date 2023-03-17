class Archer {
  float shoulderL_x, shoulderL_y;
  float shoulderR_x, shoulderR_y;
  
  float elbowL_x, elbowL_y;
  float elbowR_x, elbowR_y;
  
  float wristL_x, wristL_y;
  float wirstR_x, wristR_y;
  
  int diameter;
  
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
    wirstR_x = rw_x;
    wristR_y = rw_y;
    
    diameter = d;
  }
  
  //display the archer arms configuration from a view from top
  void display(){
    fill(198);
    //ellipse(xpos, ypos, diameter, diameter);
  }

}
