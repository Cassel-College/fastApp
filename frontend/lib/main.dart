import 'package:flutter/material.dart';
import 'package:frontend/http_tools.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  void _sendHttpRequest() async {

    // 构建请求参数
    final Map<String, dynamic> testParams = {
      "id": "string"
    };

    try {
      // 动态设置 HttpTools 全局的 IP 和 Port
      // HttpTools().globalIp = ip;
      // HttpTools().globalPort = port;

      // 发起 POST 请求
      // final response = await HttpTools().post(
      //   '/api/v1/example/example',
      //   data: testParams,
      // );
      // 发起 GET 请求
      final response = await HttpTools().get(
        '/api/v1/example/example',
      );
      // 检查返回数据的结构
      print('Return response: ${response}'); // 打印返回数据(response));

      setState(() {
        _counter = response.toString().length;
      });
    } catch (e) {
      print('Login error: $e');
      rethrow; // 将异常向上传递
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter Demo Home Page'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          FloatingActionButton(
            onPressed: _incrementCounter,
            tooltip: 'Increment',
            child: const Icon(Icons.add),
          ),
          SizedBox(height: 10),
          FloatingActionButton(
            onPressed: _sendHttpRequest,
            tooltip: 'Send HTTP Request',
            child: const Icon(Icons.send),
          ),
        ],
      ),
    );
  }
}