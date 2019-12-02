# Learning and talking

* 配置环境变量

## Chapter 1

#### 1. post请求

~~~~
func (m *WorkerManager) ChangeTaskStatus(id int64, status int) bool {
	url := m.Config.DataManagerIp + "/" + "task"
	client := &http.Client{}
	params := struct {
		Id     int64 `json:"rowid"`
		Status int   `json:"task_status"`
	}{id, status}
	request, err := json.Marshal(params)
	req, err := http.NewRequest("POST", url, strings.NewReader(string(request)))
	if err != nil {
		return false
	}
	c := http.Cookie{
		Name:  "session_id",
		Value: m.Config.UserKeyCode,
	}
	req.AddCookie(&c)
	resp, err := client.Do(req)
	if err != nil {
		return false
	}
	body, err := ioutil.ReadAll(resp.Body)
	var mapResult map[string]interface{}
	err = json.Unmarshal(body, &mapResult)
	if err != nil {
		return false
	}
	if mapResult["error_code"] != "DG0001" {
		return false
	}
	return true
}

~~~~