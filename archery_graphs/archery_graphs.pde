/*
Load CSV file 
Read sequentially all the data 
update position of the data
 */

// A Table object
Table table;

//A Barycenter object
Barycenter[] bary;

//A Bow object
Bow[] bow;

//A Archer object;
Archer[] archer;

//A Subcanvas object;
subCanvas[] canvas;

int diameter=5;
int index = 0;

void loadData() {
  // Load CSV file into a Table object
  // "header" option indicates the file has a header row
  table = loadTable("./data.csv", "header");

  // The size of the array is determined by the total number of rows in the CSV
  bary = new Barycenter[table.getRowCount()]; 
  bow = new Bow[table.getRowCount()]; 
  archer = new Archer[table.getRowCount()];

  // You can access iterate over all the rows in a table
  int rowCount = 0;
  for (TableRow row : table.rows()) {
    
    float barycenter_x = row.getFloat("barycenter_x");
    float barycenter_y = row.getFloat("barycenter_y");
    
    float bow_x = row.getFloat("bow_x");
    float bow_y = row.getFloat("bow_y");
    float bow_z = row.getFloat("bow_z");
    
    float ls_x = row.getFloat("left_shoulder_positions_x");
    float ls_y = row.getFloat("left_shoulder_positions_y");
    float rs_x = row.getFloat("right_shoulder_positions_x");
    float rs_y = row.getFloat("right_shoulder_positions_y");
    
    float le_x = row.getFloat("left_elbow_positions_x");
    float le_y = row.getFloat("left_elbow_positions_y");
    float re_x = row.getFloat("right_elbow_positions_x");
    float re_y = row.getFloat("right_elbow_positions_y");
    
    float lw_x = row.getFloat("left_wrist_positions_x");
    float lw_y = row.getFloat("left_wrist_positions_y");
    float rw_x = row.getFloat("right_wrist_positions_x");
    float rw_y = row.getFloat("right_wrist_positions_y");
    
    bary[rowCount] = new Barycenter(barycenter_x + width/4, barycenter_y + height/4, diameter);
    bow[rowCount] = new Bow(bow_x, bow_y, bow_z, diameter);
    archer[rowCount] = new Archer(ls_x, ls_y, rs_x, rs_y, le_x, le_y, re_x, re_y, lw_x, lw_y, rw_x, rw_y, diameter);
    rowCount++;
  }
}

void setup() {
  
  //set the title of the window
  surface.setTitle("Archery Visual Feedback Control");
  surface.setResizable(false);
  surface.setLocation(100, 100);
  //windows size(w,h)
  size(1500, 900);
  //translate origin to the center of the window
  translate(width/2, height/2);
  //white background
  background(255);
  noStroke();
  //loading csv file
  loadData();

  //setting position of all subcanvas (x,y,w,h)
  canvas = new subCanvas[4];
  int size_h = width/4 -60;
  int size_w = height/4 + 140;
  canvas[0] = new subCanvas(width/4, height/4, 5, size_w, size_h);
  canvas[0].showAxis(-1,-1);
  println("check ", canvas[0].x, canvas[0].y);
  canvas[1] = new subCanvas(width/4, 3*height/4, 5, size_w, size_h);
  println("check ", canvas[1].x, canvas[1].y);
  canvas[1].showAxis(3,-1);
  canvas[2] = new subCanvas(3*width/4, height/4, 5, size_w, size_h);
  canvas[2].showAxis(-1,-1);
  canvas[3] = new subCanvas(3*width/4, 3*height/4, 5, size_w, size_h);
  canvas[3].showAxis(-1,-1);
}

void draw() {
  //subcanvas 
  canvas[0].display();
  canvas[1].display();
  canvas[2].display();
  canvas[3].display();
  
  //get the barycenter animation
  bary[index].display(width/4,height/4,  height/4 + 140, width/4 - 60);
  //10000 measurements in csv file
  if (index >= bary.length - 1) {
    println("STOP");
    noLoop();
  }
  index++;
}
