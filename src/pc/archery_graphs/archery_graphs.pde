/*
Load CSV file 
Read sequentially all the data 
update position of the data
 */

//A Barycenter object
Barycenter bary;

//A Archer object;
Archer archer;

//A Subcanvas object;
subCanvas[] canvas;

int diameter = 10;
int index = 0;
int counter = 0;

int size_h;
int size_w;

int max_x_length;
int max_y_length;

void setup() {
  
  //set the title of the window
  surface.setTitle("Archery Visual Feedback Control");
  surface.setResizable(false);
  //surface.setLocation(100, 100);
  //windows size(w,h)
  //size(1500, 900);
  fullScreen();
  //white background
  background(255);
  noStroke();
  
  fill(0, 255, 0);
  
  max_x_length = 0;
  max_y_length = 0;

  String[] lines = loadStrings("../pc_side/config.txt");
  
  for (int i = 0 ; i < lines.length; i++) {
    
    if (lines[i].contains("shoulder_length")){
     
      String[] arr_split = lines[i].split(" ");
      max_x_length += int(arr_split[1]);
      
    }else if (lines[i].contains("shoulder_elbow_length") || lines[i].contains("elbow_wrist_length")){
      
      String[] arr_split = lines[i].split(" ");
      max_x_length += (int(arr_split[1]) * 2);
      max_y_length += int(arr_split[1]);
    }
  }

  //setting position of all subcanvas (x,y,w,h)
  canvas = new subCanvas[2];
  size_w = (width - 140);
  size_h = (height - 200 ) / 3;
  canvas[1] = new subCanvas(width / 2, 5 * height / 6, 5, size_h, size_h);
  canvas[0] = new subCanvas(width / 2, height / 3, 5, size_w - 300, 2 * height / 3 - 160);
  
}

void draw() {  
  background(255);
  //subcanvas

  fill(255, 0, 0);
  circle(width / 2, height / 2, 40);

  canvas[1].showAxis("BARYCENTER POSITION");
  canvas[0].showAxis("ARMS POSITION");
    
  canvas[0].display();
  canvas[1].display();
   
  //loading csv file
  Table table;
  try{
    table = loadTable("data/data.csv");
    TableRow row = table.getRow(0);
  
    bary = new Barycenter(row.getFloat(0), row.getFloat(1), diameter);
    archer = new Archer(row.getFloat(5), row.getFloat(6), row.getFloat(7), row.getFloat(8), row.getFloat(9), row.getFloat(10), row.getFloat(11), row.getFloat(12), row.getFloat(13), row.getFloat(14), row.getFloat(15), row.getFloat(16), diameter);
 
  }catch(Exception e){
      //println("Opened file while writing probably");
  }

  bary.display(width / 2, 5 * height / 6, size_h - 20, size_h - 20);  // to make sure points are never going to be on the border of the window
  archer.display(width / 2, height / 3, size_w - 20, height - 100, max_x_length, max_y_length);  
  
  //noLoop();
  
}
