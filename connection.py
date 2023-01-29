# pip install python-osc
from pythonosc import udp_client
import argparse
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  parser2 = argparse.ArgumentParser()
  parser2.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
  parser2.add_argument("--port", type=int, default=5006,
      help="The port the OSC server is listening on")
  args2 = parser2.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port) # Pure Data
  client2 = udp_client.SimpleUDPClient(args2.ip, args2.port) # Processing

  client.send_message("/on", 1)

  fig, ax = plt.subplots()
  ax.set_xlim([-1, 1])
  ax.set_ylim([-1, 1])
  ax.set_aspect('equal')
  ax.grid(True)

  circle = plt.Circle((0, 0), radius=0.1, color='r')
  ax.add_patch(circle)

  cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

  x = 0
  y = 0

  def on_move(event):
    global x,y
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        circle.center = x, y
    fig.canvas.draw_idle()
    client.send_message("/x", x)
    client.send_message("/y", -y)
    client2.send_message("/x", x)
    client2.send_message("/y", -y)


  fig.canvas.mpl_connect('motion_notify_event', on_move)
  plt.show()

  client.send_message("/on", 0)