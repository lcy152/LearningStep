# Learning and talking

* websocket

## Chapter 5

#### 1. 服务端

~~~~
http.HandleFunc("/echo", echo)

func echo( w http.ResponseWriter, r *http.Request){
    c, _ := upgrader.Upgrade(w, r, nil)
    defer c.Close()
    for {
        mt, message, _ := c.ReadMessage()
        // c.ReadMessage()是阻塞的,也就是说,当有消息来时,它后面的代码才会被执行.
        c.WriteMessage(mt, []byte{})
        if mt == websocket.CloseMessage {
			close(receiveChan)
			_ = c.Close()
			return
		}
    }
}
~~~~

#### 2. 客户端
~~~~
ws = new WebSocket("ws://127.0.0.1:8080/echo");
ws.onopen = function(evt) {...}
ws.onmessage = function(evt) {...}            
ws.onerror = function(evt) {...}
document.getElementById("send").onclick = function(evt) {
    if (!ws) {return false;}
    ws.send(input.value);
    return;
};
~~~~