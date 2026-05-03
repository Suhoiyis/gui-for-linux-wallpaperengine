import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:lwg_gui/main.dart';

void main() {
  testWidgets('App renders without crashing', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: WallpaperApp()));
    await tester.pump();
    expect(find.byType(MainScreen), findsOneWidget);
  });
}