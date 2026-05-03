import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class PlatformService {
  static const _channel = MethodChannel('lwg_gui/platform');

  Future<dynamic> invoke(String method, [Map<String, dynamic>? args]) async {
    try {
      return await _channel.invokeMethod(method, args);
    } on PlatformException catch (e) {
      throw PlatformException(
        code: e.code,
        message: 'Method $method failed: ${e.message}',
      );
    }
  }
}

final platformServiceProvider = Provider<PlatformService>((_) {
  return PlatformService();
});