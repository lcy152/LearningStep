# Learning and talking

## 1. Angular使用js文件

* angular.json:
~~~~
"scripts": [
    "src/assets/js/download.js"
],
~~~~

* download.js:
~~~~
var plugin = {
    downloadTxt: function (filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }
}
~~~~

* 在src下的typing.d.ts中:
~~~~
declare var plugin: any;
~~~~

* 在组件中使用
~~~~
plugin.downloadTxt(fileName, data['sn']);
~~~~
