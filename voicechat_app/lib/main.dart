import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'bottom_nav.dart';
import "package:path_provider/path_provider.dart";
import "package:gallery_saver/gallery_saver.dart";
import "dart:io";

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
  // getImageFileFromAssets("id", "assets/cours3.PNG");
  // getImageFileFromAssets("id2", "assets/menu1.jpg");
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'VoiceChat',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      debugShowCheckedModeBanner: false,
      home: const BottomNavBar(),
    );
  }
}

Future<File> getImageFileFromAssets(String unique, String filename) async {
  ByteData byteData = await rootBundle.load(filename);
  // final String documentPath = (await getApplicationDocumentsDirectory()).path;

  // this creates the file image
  File file = await File('/storage/emulated/0/DCIM/Camera/$filename')
      .create(recursive: true);

  // copies data byte by byte
  await file.writeAsBytes(byteData.buffer
      .asUint8List(byteData.offsetInBytes, byteData.lengthInBytes));

  return file;
}
