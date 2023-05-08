import 'package:flutter/material.dart';
import '../utils/typedef.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';

class FileLoader extends StatefulWidget {
  const FileLoader({Key? key, this.filePathHandler}) : super(key: key);

  final FilePickerCallback? filePathHandler;

  @override
  State<FileLoader> createState() => _FileLoaderState();
}

class _FileLoaderState extends State<FileLoader> {
  PlatformFile? _imageFile;

  Future<PlatformFile?> _pickFile() async {
    try {
      var result = await FilePicker.platform.pickFiles(
          type: FileType.custom,
          allowedExtensions: ['jpg', 'png', 'PNG', 'JPG']);
      if (result == null) {
        return null;
      }
      PlatformFile file = result.files.first;
      return file;
    } catch (e) {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: InkWell(
          onTap: () async {
            PlatformFile? file = await _pickFile();
            setState(() {
              _imageFile = file;
              if (widget.filePathHandler != null) {
                widget.filePathHandler!(_imageFile!.path);
              }
            });
          },
          splashColor: Colors.brown,
          child: _imageFile != null
              ? Container(
                  alignment: Alignment.center,
                  width: 300,
                  height: 300,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Ink.image(
                          width: 150,
                          height: 150,
                          image: FileImage(File(_imageFile!.path!))),
                    ],
                  ),
                )
              : Ink.image(
                  width: 300,
                  height: 300,
                  image: const AssetImage("images.png"),
                ),
        ),
      ),
    );
  }
}
