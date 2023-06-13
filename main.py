def web_page():

  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 30px; text-decoration: none; font-size: 10px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}.button3{background-color: red;}</style></head><body> <h1>ESP Web Server</h1> 
  <strong>Order a car </strong></p>
  <table>
  <tr><td></td><td><p><a href="/?direction=forward"><button class="button button2">Forward</button></a></p></td><td></td></tr>
  <tr><td><p><a href="/?direction=left"><button class="button button2">Left</button></a></p></td><td><p><a href="/?direction=off"><button class="button button3">STOP</button></a></p></td>
  <td><p><a href="/?direction=right"><button class="button button2">DROITE</button></a></p></td></tr>
  <tr><td></td><td><p><a href="/?direction=backwards"><button class="button button2">Backwards</button></a></p></td><td></td></tr>
  </body></html>
  </table>
  """
  return html

def stop_car():
    dc_motor.stop()
    dc_motor1.stop()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  direction_forward = request.find('/?direction=forward')
  direction_stop = request.find('/?direction=off')
  direction_right = request.find('/?direction=right')
  direction_left = request.find('/?direction=left')
  direction_backwards = request.find('/?direction=backwards')
  if direction_forward == 6: # we click on the forward button
    dc_motor.forward(80) # the car is moving
    dc_motor1.forward(80)
  if direction_stop == 6: # we click on the stop button
    dc_motor.stop() # the car stops
    dc_motor1.stop()
  if direction_right == 6: # we click on the right button
    dc_motor.forward(10) # the car turns right
    dc_motor1.forward(80)
  if direction_left == 6: # we click on the left button
    dc_motor.forward(80) # the car turns left
    dc_motor1.forward(10)
  if direction_backwards == 6: #we click on the backwards button
    dc_motor.backwards(80) # the car reverses
    dc_motor1.backwards(80)  

  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()