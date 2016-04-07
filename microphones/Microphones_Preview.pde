static ArrayList<Point> listeners = new ArrayList<Point>();
static Point target;
 
void setup() {
  // Set the listeners and target
  size(500, 500);
  listeners.add(new Point(-50, 0));
  listeners.add(new Point(50, 0));
  listeners.add(new Point(0, -50));
  listeners.add(new Point(0, 50));
  //listeners.add(new Point(-30, 68));
  //listeners.add(new Point(30, 68));
 
  target = new Point(0, 0);
 
}
 
void draw() {
  // White background
  background(255);
 
  // Set target position to mouse
  if (mousePressed) {
    target.SetPos(mouseX - width / 2, -mouseY + height/2);
  }
 
  // Push matrix before we do transformations
  pushMatrix();
 
  // Flip y axis so negative is down
  scale(1, -1);
  translate(0, -height);
 
  // Move origin to center
  translate(width/2, height/2);
 
  // Get the closest listeners. This will be the master (zero time)
  Point closest = getClosest();
  // Subtract this from the slave distance to get the data you
  // will have in practice
  float minDist = dist(closest, target);
  drawPoints(closest);
 
  for(Point p : listeners)
  {
    // Don't draw the hyperbola twice
    if(p == closest) continue;
   
    // Draw hyperbola using master, slave, timing difference, and sample resolution
    drawHyperbola(closest, p, dist(p, target) - minDist, 400);
  }
 
  popMatrix();
}
 
Point getClosest()
{
  Point closest = listeners.get(0);
  for(int i = 1; i < listeners.size(); i++)
  {
    if(dist(listeners.get(i), target) < dist(closest, target))
    {
      closest = listeners.get(i);
    }
  }
  return closest;
}
 
// Master is always closer
void drawHyperbola(Point master, Point slave, float difference, int resolution)
{
  // Distance from center
  float c = dist(master, slave) / 2f;
  // Vertices
  float a = c - difference / 2f;
  float b = sqrt(c*c - a*a);
  // center x
  float h = 0; //lerp(master.x, slave.x, 0.5f);
  // center y
  float k = 0; //lerp(master.y, slave.y, 0.5f);
  
  float xCent = (slave.x - master.x)/2 + master.x;
  float yCent = (slave.y - master.y)/2 + master.y;
  
  // In radians
  float angle = new PVector(master.x - slave.x, master.y - slave.y).heading();
  pushMatrix();
  
  //translate((slave.x - master.x) / 2, -(slave.y - master.y) / 2);
  // Rotate parabola
  // HACK -- rotating extra 90 degrees instead of changing formula
  translate(xCent - (slave.x - master.x)/2, yCent - (slave.y - master.y)/2);
  rotate(angle + PI/2);
 
  
  // Draw axis for visualization
  stroke(255, 0, 0);
  line(0, 0, 0, 100);
  line(0, 0, 0, -100);
  stroke(0);
 
  float increments = width / resolution;
  float lastX = -width/2;
  float lastY1 = 0;
  float lastY2 = 0;
 
  // Asymptotes
  stroke(0, 255, 0);
  //line(-width/2, (a/b*(-width/2)), width/2, (a/b*(width/2)));
  //line(-width/2, -(a/b*(-width/2)), width/2, -(a/b*(width/2)));
  // Difference line (vertex)
  stroke(0, 0, 255);
  //line(slave.x, 0, difference-slave.x, 0);
  stroke(0);
 
  for(int i = 0; i < resolution * 10; i++)
  {
    float x = -width/2 + i * increments;
    
    b = dist(master, slave);
    c = difference;
    float underSqrt = (pow(b, 4)*pow(c, 2)-2*pow(b, 2)*pow(c, 4)+pow(c, 6)+4*pow(b, 2)*pow(c, 2)*pow(x, 2)-4*pow(c, 4)*pow(x, 2));

    float y1 = (b*b*b - b*c*c - sqrt(underSqrt))/(2*(b*b-c*c));
    float y2 = (b*b*b - b*c*c + sqrt(underSqrt))/(2*(b*b-c*c));
   
    // Draw parabolas
    if(i != 0)
    {
      line(lastX, lastY1, x, y1);
      line(lastX, lastY2, x, y2);
    }
   
    // Store last coordinates for drawing
    lastX = x;
    lastY1 = y1;
    lastY2 = y2;
  }
  popMatrix();
}
 
float dist(Point a, Point b)
{
  return dist(a.x, a.y, b.x, b.y);
}
 
void drawPoints(Point master)
{
    // Draw listeners
  fill(255);
  for(Point p : listeners)
  {
    if(p == master)
      fill(0, 0, 255);
    else
      fill(255);
    ellipse(p.x, p.y, 5, 5);
  }
 
  // Draw red target
  fill(255, 0, 0);
  ellipse(target.x, target.y, 5, 5);
}
 
class Point {
  float x;
  float y;
 
  Point(float x, float y)
  {
    SetPos(x, y);
  }
 
  void SetPos(float x, float y)
  {
    this.x = x;
    this.y = y;
  }
}