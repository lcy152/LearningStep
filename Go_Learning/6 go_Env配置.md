# Learning and talking

* 配置环境变量(go1.13)

## Chapter 1

#### 1. GOPROXY

GOPROXY环境变量是伴随着modules而生的，在go1.13中得到了增强，可以设置为逗号分隔的url列表来指定多个代理，其默认值为https://proxy.golang.org,direct，也就是说google为我们维护了一个代理服务器，但是因为墙的存在，这个默认设置对中国的gopher并无卵用，应第一时间修改。

go命令在需要下载库包的时候将逐个试用设置中的各个代理，直到发现一个可用的为止。direct表示直连，所有direct之后的proxy都不会被使用，一个设置例子：
~~~~
    GOPROXY=https://proxy.golang.org,https://myproxy.mysite:8888,direct
~~~~

GOPROXY环境变量可以帮助我们下载墙外的第三方库包，比较知名的中国区代理goproxy.cn。当然，通过设置https_proxy环境变量设也可以达到此目的。但是一个公司通过在内部架设一个自己的goproxy服务器来缓存第三方库包，库包下载速度会更快,可以感觉到module有一点maven的意思了，但是易用性上还有很长的路要走。

#### 2. GOPRIVATE
使用GOPROXY可以获取公共的包，这些包在获取的时候会去https://sum.golang.org进行校验，这对中国的gopher来说又是一个比较坑的地方，Go为了安全性推出了Go checksum database（sumdb），环境变量为GOSUMDB，go命令将在必要的时候连接此服务来检查下载的第三方依赖包的哈希是否和sumdb的记录相匹配。很遗憾，在中国也被墙了，可以选择设置为一个第三方的校验库，也可更直接点将GOSUMDB设为off关闭哈希校验，当然就不是很安全了。

除了public的包，在现实开发中我们更多的是使用很多private的包，因此就不适合走代理，所以go1.13推出了一个新的环境变量GOPRIVATE，它的值是一个以逗号分隔的列表，支持正则（正则语法遵守 Golang 的 包 path.Match）。在GOPRIVATE中设置的包不走proxy和checksum database，例如：

~~~~
    GOPRIVATE=*.corp.example.com,rsc.io/private
~~~~

#### 3. GONOSUMDB 和 GONOPROXY
这两个环境变量根据字面意思就能明白是设置不进行校验和不走代理的包，设置方法也是以逗号分隔

#### 4. go env -w
可能是go也觉得环境变量有点多了，干脆为go env增加了一个选项-w，来设置全局环境变量，在Linux系统上我们可以这样用：
~~~~
    go env -w GOPROXY=https://goproxy.cn,direct
    go env -w GOPRIVATE=*.gitlab.com,*.gitee.com
    go env -w GOSUMDB=off
~~~~


