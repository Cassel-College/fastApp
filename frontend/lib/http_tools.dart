import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HttpTools {
  static final HttpTools _instance = HttpTools._internal();
  late Dio _dio;
  String? globalIp; // Define globalIp
  String? globalPort; // Define globalPort

  factory HttpTools() {
    return _instance;
  }

  HttpTools._internal() {
    String ip = globalIp ?? '127.0.0.1';
    String port = globalPort ?? '8000';
    _dio = Dio(BaseOptions(
      baseUrl:
          'http://$ip:$port', // Use globalIp and globalPort, fallback to defaults
      connectTimeout: const Duration(seconds: 15),
      receiveTimeout: const Duration(seconds: 15),
      headers: {'accept': 'application/json'},
    ));
    print('初始化完成...');
    print('Current IP: $ip, Port: $port'); // 添加打印当前的ip和port
  }

  Future<void> refreshProxySettings() async {
    await loadGlobalProxySettings(); // 刷新代理设置
    String ip = globalIp ?? '127.0.0.1';
    String port = globalPort ?? '8000';
    print('Current IP: $ip, Port: $port'); // 添加打印当前的ip和port
    _dio.options.baseUrl = 'http://$ip:$port'; // 更新baseUrl
  }

  Future<void> loadGlobalProxySettings() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    globalIp = prefs.getString('proxy_ip');
    globalPort = prefs.getString('proxy_port');
  }

  Future<dynamic> get(String path,
      {Map<String, dynamic>? queryParameters}) async {
    await refreshProxySettings(); // 在每次get请求前刷新设置
    try {
      final response = await _dio.get(path, queryParameters: queryParameters);
      print('GET Response: $response');
      print('GET Response data: ${response.data}');
      if (response.statusCode == 200) {
        return response.data;
      } else {
        throw Exception('HTTP Error: ${response.statusCode}');
      }
    } catch (e) {
      print('GET Error: $e');
      rethrow;
    }
  }

  Future<dynamic> post(String path, {dynamic data}) async {
    await refreshProxySettings(); // 在每次get请求前刷新设置
    try {
      final response = await _dio.post(path, data: data);
      // print('POST Response: $response');
      print('POST Response data: ${response.data}');
      if (response.statusCode == 200 || response.statusCode == 201) {
        return response.data;
      } else {
        throw Exception('HTTP Error: ${response.statusCode}');
      }
    } catch (e) {
      print('POST Error: $e');
      rethrow;
    }
  }
}
