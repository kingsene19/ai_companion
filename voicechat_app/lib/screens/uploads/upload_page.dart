import "package:flutter/material.dart";
import "../../components/file_loader.dart";
import 'dart:convert';
import 'package:http/http.dart' as http;

class UploadPage extends StatefulWidget {
  const UploadPage({Key? key, required this.fileType, this.classe, this.field})
      : super(key: key);

  final String? fileType;
  final String? classe;
  final String? field;

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  String? _imagePath;
  String? apiUrl;
  bool isUploading = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
      ),
      backgroundColor: Colors.white,
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            children: [
              isUploading
                  ? SizedBox(
                      height: 36,
                      width: 36,
                      child: CircularProgressIndicator(
                        valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
                      ),
                    )
                  : SizedBox(),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 20),
                child: Text(
                  "Upload an image of the ${widget.fileType}",
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Colors.black,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              Padding(
                  padding: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  child: Text(
                    _imagePath != null
                        ? "Make sure your ${widget.fileType} is clear"
                        : "Click on the zone to upload a file",
                    textAlign: TextAlign.center,
                    style: _imagePath != null
                        ? const TextStyle(
                            color: Colors.brown,
                            fontSize: 17,
                            decoration: TextDecoration.underline,
                            decorationColor: Colors.brown,
                          )
                        : const TextStyle(
                            color: Colors.brown,
                            fontSize: 15,
                          ),
                  )),
              FileLoader(
                filePathHandler: (value) {
                  setState(() {
                    _imagePath = value;
                  });
                },
              ),
              TextButton(
                  child: Text(
                    "Soumettre",
                    style: TextStyle(
                        color: Colors.white,
                        fontSize: 15,
                        fontWeight: FontWeight.bold),
                  ),
                  style: TextButton.styleFrom(backgroundColor: Colors.brown),
                  onPressed: () async {
                    if (_imagePath != null) {
                      var response = await uploadImage(_imagePath!);

                      showDialog(
                          context: context,
                          builder: (context) {
                            return AlertDialog(
                              title: response != null
                                  ? Text('Upload was successful')
                                  : Text('Upload failed'),
                              actions: [
                                TextButton(
                                  child: const Text('Ok'),
                                  onPressed: () {
                                    Navigator.of(context).pop();
                                    setState(() {
                                      isUploading = false;
                                    });
                                  },
                                )
                              ],
                            );
                          });
                    }
                  })
            ],
          ),
        ),
      ),
    );
  }

  uploadImage(String imagePath) async {
    try {
      setState(() {
        isUploading = true;
      });
      print("Uploading");
      if (widget.fileType == "menu") {
        apiUrl = "http://172.20.10.12:5000/extract_menu";
      } else {
        apiUrl = "http://172.20.10.12:5000/extract_schedule";
      }
      var url = Uri.parse(apiUrl!);
      var request = http.MultipartRequest("POST", url);
      var multipartFile = await http.MultipartFile.fromPath('file', imagePath);
      request.files.add(multipartFile);
      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);
      var jsonResponse = jsonDecode(response.body);
      print("Done");
      if (response.statusCode == 200) {
        return jsonResponse;
      } else if (response.statusCode == 500) {
        return null;
      }
    } catch (e) {
      return null;
    }
  }
}
