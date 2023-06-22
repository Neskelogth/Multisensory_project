import java.util.Arrays;

class Bow {
  int diameter;
  PShape circle;
  float [] prev_x, prev_y, prev_z;
  PShape line;
  
  Bow(int d){
    diameter = d;
    prev_x = new float[1];
    prev_y = new float[1];
    prev_z = new float[1];
    
    prev_x[0] = 753;
    prev_y[0] = 753;
    prev_z[0] = 753;
    
  }
  
  void append_to_array(float x, float y, float z){
    
    prev_x = append_arr(prev_x, x);
    prev_y = append_arr(prev_y, y);
    prev_z = append_arr(prev_z, z);
  }
  
  float[] append_arr(float[]   arr, float val){
    
    if (arr.length == 1 && arr[0] == 753){
      arr[0] = val;
    }else{
      arr = Arrays.copyOf(arr, arr.length + 1);
      arr[arr.length - 1] = val;   
      System.out.println(arr.length);
    }
    return arr;
  }
  
  //display Bow shaking in two different planes
  //plane x-y and plane x-z ? 
  void display(float rect_x , float rect_y, float rect_w, float rect_h, boolean yz){
    
    for(int i = 0; i < prev_x.length; i++){
      
      circle = createShape(ELLIPSE, rect_x + (prev_z[i] * rect_w / 2), rect_y - (prev_y[i] * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
      circle.setFill(color(0, 255, 0));
      //show dots
      shape(circle);
      
      circle = createShape(ELLIPSE, rect_x + (prev_x[i] * rect_w / 2) + width / 2, rect_y - (prev_y[i] * rect_h / 2), diameter, diameter);  // the - in the second place is to invert the axis in the vertical direction
      circle.setFill(color(0, 255, 0));
      //show dots
      shape(circle);
    }
    
    //define the position in the display
    fill(198);
    //ellipse(xpos, ypos, diameter, diameter);
    
    fill(100);
    //ellipse(xpos, zpos, diameter, diameter);
  }

}
